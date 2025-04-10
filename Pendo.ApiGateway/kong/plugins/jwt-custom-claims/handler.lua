local jwt_decoder = require "kong.plugins.jwt.jwt_parser"
local helpers = require "kong.plugins.jwt-custom-claims.helpers"
local cjson = require "cjson.safe"
local kong = kong

local JwtCustomClaimsHandler = {
  PRIORITY = 1010, -- Run before the ACL Plugin
  VERSION = "1.0.0"
}

-- List of public paths
local public_paths = { "/api/Identity/RequestOtp", "/api/Identity/VerifyOtp", "/api/Identity/Ping", "/api/Booking/HealthCheck", "/api/Admin/HealthCheck", "/api/Message/HealthCheck" }

-- Define user type to ACL group mapping
local user_type_to_acl = {
  ["Manager"] = "manager", 
  ["User"] = "authenticated"
  -- Default will be "authenticated" for any other user type
}

-- JWT Docuemntation at: https://konghq.com/blog/engineering/craft-and-sign-custom-jwt
-- Reference JWTClaim codebase: https://github.com/wshirey/kong-plugin-jwt-claims-validate/blob/master/handler.lua

function JwtCustomClaimsHandler:access(conf)
  local request_path = kong.request.get_path()
  -- Check if the path starts with one of the public prefixes
  for _, public_path in ipairs(public_paths) do
    if request_path:find("^" .. public_path) then
      kong.log.debug("Skipping JWT claims verification for public path: ", request_path)
      return  -- Bypass authentication
      -- This is a fallback in case removing the auth headers in declarative doesn't work
    end
  end

  -- Get the JWT token from the request
  local token_header = kong.request.get_header("Authorization")
  if not token_header then
    kong.log.debug("No Authorisation header found")
    return
  end
  
  -- Remove "Bearer " if present
  local jwt_token_str = token_header:gsub("^[Bb]earer%s+", "")
  
  -- Parse the JWT token
  local jwt_obj, err = jwt_decoder:new(jwt_token_str)
  if err then
    kong.log.err("Failed to parse JWT: ", err)
    return
  end
  
  local jwt_claims = jwt_obj.claims
  kong.log.debug("JWT claims: ", cjson.encode(jwt_claims))

  -- For analytics service, verify the user is a manager
  local service_name = kong.router.get_service() and kong.router.get_service().name
  if service_name == "admin-service" and conf.require_admin_for_analytics then
    local user_type = jwt_claims["UserType"]
    if not user_type or user_type ~= "Manager" then
      return kong.response.exit(403, { message = "Access forbidden: Manager privileges required" })
    end
  end
  
  --[[
      Nginx context for request 
      Required to handle the deployment server's reverse proxy setup
  --]]

  -- Add user info to headers for downstream services
  if conf.add_user_info_headers then
    if jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"] then
      kong.service.request.set_header("X-User-Email", jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"])
    end
    
    kong.service.request.set_header("X-User-Type", jwt_claims["UserType"] or "")
  end
  
  -- Map user type to ACL group
  if conf.map_user_type_to_acl and jwt_claims["UserType"] then
    local user_type = jwt_claims["UserType"]
    local acl_group = user_type_to_acl[user_type] or "authenticated"
    
    -- Set both headers used by Kong ACL plugin
    kong.service.request.set_header("X-Consumer-Groups", acl_group)
    kong.service.request.set_header("X-Consumer-Username", jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"] or "jwt-user")
    
    -- Update the consumer in the context for ACL plugin
    ngx.ctx.authenticated_consumer = {
      id = jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"] or "jwt-user",
      username = jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"] or "jwt-user"
    }
    
    -- Associate the consumer with the appropriate group
    ngx.ctx.authenticated_groups = { acl_group }
    
    kong.log.debug("Mapped UserType '" .. user_type .. "' to ACL group: " .. acl_group)
    
    -- Register the consumer so downstream plugins recognise it
    kong.client.authenticate(ngx.ctx.authenticated_consumer)
  end

  -- NGINX context for request end --
  
  -- Extract user ID from NameIdentifier claim and append to request body
  local user_id = jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"]
  if user_id then
    kong.log.debug("Adding UserId: " .. user_id .. " to request body")
    
    local success, err = pcall(function()
      -- Get the original request body
      local body_raw = kong.request.get_raw_body()
      local body = {}
      
      -- Try to parse existing body if available
      if body_raw and #body_raw > 0 then
        local decoded = cjson.decode(body_raw)
        if decoded then
          body = decoded
        end
      end
      
      -- Add UserId to the body, preserving other fields
      body["UserId"] = user_id
      
      -- Convert back to JSON
      local json_body = cjson.encode(body)
      
      -- Set the modified body back
      kong.service.request.set_raw_body(json_body)
      kong.service.request.set_header("Content-Type", "application/json")
      kong.service.request.set_header("Content-Length", #json_body)
      
      kong.log.debug("Modified body: " .. json_body)
    end)
    
    if not success then
      kong.log.err("Error modifying request body: " .. tostring(err))
    end
  else
    kong.log.debug("No NameIdentifier claim found in JWT token")
  end
end

return JwtCustomClaimsHandler
