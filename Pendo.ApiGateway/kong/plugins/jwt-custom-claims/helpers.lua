local _M = {}

-- Helper function to check if a path is in the array of public paths
function _M.is_public_path(path, public_paths)
  for _, public_path in ipairs(public_paths) do
    if path:find("^" .. public_path) then
      return true
    end
  end
  return false
end

-- Helper function to extract user ID from claims
function _M.get_user_id_from_claims(claims)
  return claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"]
end

-- Helper function to extract user email from claims
function _M.get_user_email_from_claims(claims)
  return claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"]
end

return _M
