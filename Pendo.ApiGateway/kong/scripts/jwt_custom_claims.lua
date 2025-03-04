-- This is a helper script for JWT custom claims processing
-- It can be used to extend functionality of the jwt-custom-claims plugin

local _M = {}

-- Function to extract user type from JWT claims
function _M.extract_user_type(jwt_claims)
  return jwt_claims and jwt_claims["UserType"] or "user"
end

-- Function to check if user is admin
function _M.is_admin(jwt_claims)
  local user_type = _M.extract_user_type(jwt_claims)
  return user_type == "admin"
end

return _M
