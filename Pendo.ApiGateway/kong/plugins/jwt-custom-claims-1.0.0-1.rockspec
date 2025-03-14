package = "jwt-custom-claims"
version = "1.0.0-1"

source = {
   url = "file:///tmp",
   dir = "jwt-custom-claims"
}

description = {
   summary = "A Kong plugin that extends JWT functionality with custom claims processing",
   detailed = [[
      This plugin extends the JWT authentication plugin by adding 
      custom claims processing functionality for the COMP2913 Software Engineering Project.
   ]],
   license = "MIT",
   homepage = "http://github.com/user/sc232jm/jwt-custom-claims"
}

dependencies = {
   "lua >= 5.1"
}

build = {
   type = "builtin",
   modules = {
      ["kong.plugins.jwt-custom-claims.handler"] = "jwt-custom-claims/handler.lua",
      ["kong.plugins.jwt-custom-claims.schema"] = "jwt-custom-claims/schema.lua",
      ["kong.plugins.jwt-custom-claims.init"] = "jwt-custom-claims/init.lua",
   }
}
