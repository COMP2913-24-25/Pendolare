local jwt_decoder = require "kong.plugins.jwt.jwt_parser"
local helpers = require "kong.plugins.jwt-custom-claims.helpers"
local cjson = require "cjson.safe"
local kong = kong

-- Define the plugin
local JwtCustomClaimsHandler = {
  PRIORITY = 1005,
  VERSION = "1.0.0"
}

-- List of public paths using prefix matching
local public_paths = { "/api/Identity/RequestOtp", "/api/Identity/VerifyOtp", "/api/Identity/ping" }

function JwtCustomClaimsHandler:access(conf)
  local request_path = kong.request.get_path()
  -- Check if the path starts with one of the public prefixes
  for _, public_path in ipairs(public_paths) do
    if request_path:find("^" .. public_path) then
      kong.log.debug("Skipping JWT claims verification for public path: ", request_path)
      return  -- bypass authentication
    end
  end

  -- Get the JWT token from the request
  local token_header = kong.request.get_header("Authorization")
  if not token_header then
    kong.log.debug("No Authorization header found")
    return -- Let the JWT plugin handle this case
  end
  
  -- Remove "Bearer " if present
  local jwt_token_str = token_header:gsub("^[Bb]earer%s+", "")
  
  -- Parse the JWT token
  local jwt_obj, err = jwt_decoder:new(jwt_token_str)
  if err then
    kong.log.err("Failed to parse JWT: ", err)
    return -- Let the JWT plugin handle this case
  end
  
  local jwt_claims = jwt_obj.claims
  kong.log.debug("JWT claims: ", kong.tools.table_to_string(jwt_claims))

  -- For analytics service, verify the user is admin
  local service_name = kong.router.get_service() and kong.router.get_service().name
  if service_name == "analytics-service" and conf.require_admin_for_analytics then
    local user_type = jwt_claims["UserType"]
    if not user_type or user_type ~= "admin" then
      return kong.response.exit(403, { message = "Access forbidden: Admin privileges required" })
    end
  end
  
  -- Add user info to headers for downstream services if configured
  if conf.add_user_info_headers then
    -- Add the username to headers for downstream services
    if jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"] then
      kong.service.request.set_header("X-User-Email", jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"])
    end
    
    kong.service.request.set_header("X-User-Type", jwt_claims["UserType"] or "")
  end
  
  -- Extract user ID from jti claim and append to request body
  local user_id = jwt_claims["jti"]
  if user_id then
    -- Read the request body
    local body, err = kong.request.get_body()
    local content_type = kong.request.get_header("content-type")
    local is_json = content_type and content_type:find("application/json", 1, true)
    
    if not body then
      body = {}
    end
    
    if is_json or type(body) == "table" then
      -- Add UserId to the body
      body["UserId"] = user_id
      
      -- Set the modified body back to the request
      local new_body, err = cjson.encode(body)
      if err then
        kong.log.err("Failed to encode modified body: ", err)
      else
        kong.service.request.set_body(new_body)
        
        -- Update content-length header
        kong.service.request.set_header("Content-Length", #new_body)
        
        -- Ensure content-type is set to application/json
        if not is_json then
          kong.service.request.set_header("Content-Type", "application/json")
        end
      end
    else
      kong.log.debug("Cannot modify non-JSON body to add UserId")
    end
  else
    kong.log.debug("No jti claim found in JWT token")
  end
end

return JwtCustomClaimsHandler
