local typedefs = require "kong.db.schema.typedefs"

return {
  name = "jwt-custom-claims",
  fields = {
    { consumer = typedefs.no_consumer },
    { protocols = typedefs.protocols_http },
    { config = {
        type = "record",
        fields = {
          { require_admin_for_analytics = { type = "boolean", default = true } },
          { add_user_info_headers = { type = "boolean", default = true } },
        },
      },
    },
  },
}
