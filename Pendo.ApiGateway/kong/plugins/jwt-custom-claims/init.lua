-- Init file for jwt-custom-claims plugin
local jwt_custom_claims = require("kong.plugins.jwt-custom-claims.handler")

return {
  PRIORITY = 1005,  -- Plugin execution order (higher means it runs earlier)
  VERSION = "1.0.0",
  handler = jwt_custom_claims
}
