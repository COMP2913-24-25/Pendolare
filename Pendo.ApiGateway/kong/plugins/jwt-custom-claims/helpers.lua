-- Helper functions for JWT custom claims plugin
local _M = {}

function _M.extract_email(jwt_claims)
  -- Extract email from standard claim names
  local email_claim_names = {
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name",
    "email",
    "sub"
  }
  
  for _, claim_name in ipairs(email_claim_names) do
    local value = jwt_claims[claim_name]
    if value then
      return value
    end
  end
  
  return nil
end

return _M
