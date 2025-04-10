local PLUGIN_NAME = "jwt-custom-claims"
local helpers = require "spec.helpers"
local cjson = require "cjson"
local jwt_parser = require "kong.plugins.jwt.jwt_parser"

--[[
  This test suite is designed to validate the functionality of the JWT Custom Claims plugin.
  It includes tests for JWT claims processing, user info header addition, and ACL mapping.
  
  Derived from: https://docs.konghq.com/gateway/latest/plugin-development/tests/ & https://github.com/Kong/busted-1
  
--]]
local function jwt_encoder(claims, key, alg)
  local jwt = jwt_parser.encode({
    iss = "Pendo.IdentityService",
    exp = os.time() + 3600,
    ["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"] = claims.user_id or "user-123",
    ["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"] = claims.email or "test@example.com",
    UserType = claims.user_type or "User"
     -- Randomly generated key for testing, not used in production
  }, key or "7a3fd8625dbc03b9f08faa02eecbf90ab92c857a301bbfc1a8536bbdfcb5c1e7 ", alg or "HS256")
  return jwt
end

describe("Plugin: " .. PLUGIN_NAME, function()
  local client

  setup(function()
    local bp = helpers.get_db_utils()

    -- Setup test service and route
    local service = bp.services:insert({
      name = "test-service",
      url = "http://httpbin.org/anything"
    })

    local route_normal = bp.routes:insert({
      name = "test-route",
      paths = { "/test" },
      service = service
    })
    
    local route_admin = bp.routes:insert({
      name = "admin-route",
      paths = { "/admin" },
      service = service
    })
    
    local route_public = bp.routes:insert({
      name = "public-route",
      paths = { "/api/Identity/Ping" },
      service = service
    })

    -- Add the plugin to the route
    bp.plugins:insert({
      name = PLUGIN_NAME,
      route = route_normal,
      config = {
        require_admin_for_analytics = true,
        add_user_info_headers = true,
        map_user_type_to_acl = true
      }
    })
    
    bp.plugins:insert({
      name = PLUGIN_NAME,
      route = route_admin,
      config = {
        require_admin_for_analytics = true,
        add_user_info_headers = true,
        map_user_type_to_acl = true
      }
    })
    
    bp.plugins:insert({
      name = PLUGIN_NAME,
      route = route_public,
      config = {
        require_admin_for_analytics = true,
        add_user_info_headers = true,
        map_user_type_to_acl = true
      }
    })

    -- Start Kong
    assert(helpers.start_kong({
      plugins = "bundled," .. PLUGIN_NAME,
      nginx_conf = "spec/fixtures/custom_nginx.template"
    }))
    
    client = helpers.proxy_client()
  end)

  teardown(function()
    if client then client:close() end
    helpers.stop_kong()
  end)

  describe("JWT claims processing", function()
    it("adds user info headers for normal user", function()
      local token = jwt_encoder({
        user_id = "user-123",
        email = "user@example.com",
        user_type = "User"
      })
      
      local r = client:get("/test", {
        headers = {
          ["Authorization"] = "Bearer " .. token,
          ["Content-Type"] = "application/json"
        }
      })
      
      local body = cjson.decode(r.body)
      assert.equal(200, r.status)
      assert.equal("user@example.com", body.headers["X-User-Email"])
      assert.equal("User", body.headers["X-User-Type"])
      assert.equal("authenticated", body.headers["X-Consumer-Groups"])
    end)
    
    it("adds manager ACL for manager user type", function()
      local token = jwt_encoder({
        user_id = "manager-123",
        email = "manager@example.com",
        user_type = "Manager"
      })
      
      local r = client:get("/test", {
        headers = {
          ["Authorization"] = "Bearer " .. token,
          ["Content-Type"] = "application/json"
        }
      })
      
      local body = cjson.decode(r.body)
      assert.equal(200, r.status)
      assert.equal("manager", body.headers["X-Consumer-Groups"])
    end)
    
    it("skips processing for public paths", function()
      local r = client:get("/api/Identity/Ping", {
        headers = {
          ["Content-Type"] = "application/json"
        }
      })
      
      assert.equal(200, r.status)
    end)
    
    it("adds UserId to request body", function()
      local token = jwt_encoder({
        user_id = "user-456",
        email = "test@example.com",
        user_type = "User"
      })
      
      local r = client:post("/test", {
        headers = {
          ["Authorization"] = "Bearer " .. token,
          ["Content-Type"] = "application/json"
        },
        body = {
          data = "test"
        }
      })
      
      local body = cjson.decode(r.body)
      assert.equal(200, r.status)
      assert.equal("user-456", body.json.UserId)
      assert.equal("test", body.json.data)
    end)
    
    it("enforces manager access for admin routes when required", function()
      -- Test with a regular user
      local token = jwt_encoder({
        user_id = "user-123",
        email = "user@example.com",
        user_type = "User"
      })
      
      local r = client:get("/admin", {
        headers = {
          ["Authorization"] = "Bearer " .. token,
          ["Content-Type"] = "application/json"
        }
      })
      
      assert.equal(403, r.status)
      
      -- Test with a manager
      token = jwt_encoder({
        user_id = "manager-123",
        email = "manager@example.com",
        user_type = "Manager"
      })
      
      r = client:get("/admin", {
        headers = {
          ["Authorization"] = "Bearer " .. token,
          ["Content-Type"] = "application/json"
        }
      })
      
      assert.equal(200, r.status)
    end)
  end)
end)
