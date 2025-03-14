-- Init file for jwt-custom-claims plugin
local jwt_custom_claims = require("kong.plugins.jwt-custom-claims.handler")

return {
  PRIORITY = 1010,  -- Must run before ACL (which is 950)
  VERSION = "1.0.0",
  handler = jwt_custom_claims
}
