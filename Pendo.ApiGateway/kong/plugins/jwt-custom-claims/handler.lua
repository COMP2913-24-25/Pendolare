local jwt_decoder = require "kong.plugins.jwt.jwt_parser"
local helpers = require "kong.plugins.jwt-custom-claims.helpers"
local kong = kong

-- Define the plugin
local JwtCustomClaimsHandler = {
  PRIORITY = 1005,
  VERSION = "1.0.0"
}

function JwtCustomClaimsHandler:access(conf)
  -- Get the JWT token from the request
  local jwt_token = kong.ctx.shared.authenticated_jwt_token
  if not jwt_token then
    return kong.response.exit(403, { message = "Access forbidden: No valid JWT token found" })
  end

  -- For analytics service, verify the user is admin
  local service_name = kong.router.get_service() and kong.router.get_service().name
  if service_name == "analytics-service" then
    local user_type = jwt_token.claims["UserType"]
    if not user_type or user_type ~= "admin" then
      return kong.response.exit(403, { message = "Access forbidden: Admin privileges required" })
    end
  end
  
  -- Add the username to headers for downstream services
  if jwt_token.claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"] then
    kong.service.request.set_header("X-User-Email", jwt_token.claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"])
  end
  
  kong.service.request.set_header("X-User-Type", jwt_token.claims["UserType"] or "")
end

return JwtCustomClaimsHandler
