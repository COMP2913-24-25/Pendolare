local typedefs = require "kong.db.schema.typedefs"

-- Define the schema for the plugin configuration
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
          { map_user_type_to_acl = { type = "boolean", default = true } },
        },
      },
    },
  },
}
