local jwt_decoder = require "kong.plugins.jwt.jwt_parser"
local helpers = require "kong.plugins.jwt-custom-claims.helpers"
local kong = kong

-- Define the plugin
local JwtCustomClaimsHandler = {
  PRIORITY = 1005,
  VERSION = "1.0.0"
}

-- List of paths that shouldn't require authentication
local public_paths = {
  ["/api/auth/request-otp"] = true,
  ["/api/auth/verify-otp"] = true,
  ["/api/ping"] = true
}

function JwtCustomClaimsHandler:access(conf)
  -- Check if the current path is a public path that doesn't need authentication
  local request_path = kong.request.get_path()
  if public_paths[request_path] then
    kong.log.debug("Skipping JWT claims verification for public path: ", request_path)
    return
  end

  -- Get the JWT token from the request
  local jwt_token = kong.ctx.shared.authenticated_jwt_token
  if not jwt_token then
    return
  end

  -- For analytics service, verify the user is admin
  local service_name = kong.router.get_service() and kong.router.get_service().name
  if service_name == "analytics-service" then
    local user_type = jwt_token.claims["UserType"]
    if not user_type or user_type ~= "admin" then
      return kong.response.exit(403, { message = "Access forbidden: Admin privileges required" })
    end
  end
  
  -- Add the username to headers for downstream services: https://www.w3schools.com/Xml/xml_soap.asp
  if jwt_token.claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"] then
    kong.service.request.set_header("X-User-Email", jwt_token.claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"])
  end
  
  kong.service.request.set_header("X-User-Type", jwt_token.claims["UserType"] or "")
end

return JwtCustomClaimsHandler
