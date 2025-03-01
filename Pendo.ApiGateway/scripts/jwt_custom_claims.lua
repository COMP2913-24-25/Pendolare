local _M = {}

function _M.execute(conf)
  local jwt_token = ngx.ctx.authenticated_jwt_token
  if not jwt_token then
    return kong.response.exit(403, { message = "Access forbidden: No valid JWT token found" })
  end

  -- For analytics service, verify the user is admin
  local service_name = kong.router.get_service().name
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

return _M
