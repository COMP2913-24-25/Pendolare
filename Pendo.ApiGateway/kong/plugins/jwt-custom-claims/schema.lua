local typedefs = require "kong.db.schema.typedefs"

return {
  name   = "jwt-custom-claims",
  fields = {
    { consumer  = typedefs.no_consumer },
    { protocols = typedefs.protocols_http },
    { config = {
        type   = "record",
        fields = {
          { add_user_info_headers = { type = "boolean", default = true  } },
          { map_user_type_to_acl  = { type = "boolean", default = true  } },
        },
      },
    },
  },
}