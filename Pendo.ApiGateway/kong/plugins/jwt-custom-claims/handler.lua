local jwt_parser = require "kong.plugins.jwt.jwt_parser"
local cjson      = require "cjson.safe"
local kong       = kong

local JwtCustomClaimsHandler = {
  PRIORITY = 1010,
  VERSION  = "1.0.0",
}

local JWT_SECRET = "d8d5304c4624d4ee3461edde3a7df1d2a2a7aec0aaa689b7ef6ca563ae3a67bb"
local JWT_ALGORITHM = "HS256"

local public_paths = {
  "/api/Identity/RequestOtp",
  "/api/Identity/VerifyOtp",
  "/api/Identity/Ping",
  "/api/Booking/HealthCheck",
  "/api/Admin/HealthCheck",
  "/api/Message/HealthCheck",
  "/api/Journey/HealthCheck",
  "/api/PaymentService/HealthCheck",
  "/api/PaymentService/StripeWebhook",
}

local user_type_to_acl = {
  ["Manager"] = "manager",
  ["User"]    = "authenticated",
}

function JwtCustomClaimsHandler:access(conf)
  local path = kong.request.get_path()

  -- skip JWT for public endpoints
  for _, p in ipairs(public_paths) do
    if path:find("^" .. p) then
      kong.log.debug("[jwt-custom-claims] skipping JWT for: ", path)
      ngx.ctx.authenticated_consumer = {
        id       = "anonymous-consumer-id",
        username = "anonymous",
      }
      ngx.ctx.authenticated_groups = { "anonymous" }
      kong.client.authenticate(ngx.ctx.authenticated_consumer)
      return
    end
  end

  -- require Authorization header
  local auth = kong.request.get_header("Authorization")
  if not auth then
    kong.log.debug("[jwt-custom-claims] no Authorization header")
    ngx.ctx.authenticated_consumer = {
      id       = "anonymous-consumer-id",
      username = "anonymous",
    }
    ngx.ctx.authenticated_groups = { "anonymous" }
    kong.client.authenticate(ngx.ctx.authenticated_consumer)
    return
  end

  -- parse JWT
  local token = auth:gsub("^[Bb]earer%s+", "")
  local jwt, err = jwt_parser:new(token)
  if err then
    kong.log.err("[jwt-custom-claims] parse error: ", err)
    return kong.response.exit(401, { message = "Invalid or malformed token" })
  end

  -- verify signature
  local ok, sig_err = jwt:verify_signature(JWT_SECRET)
  if not ok then
    kong.log.err("[jwt-custom-claims] signature failed: ", sig_err)
    return kong.response.exit(401, { message = "Invalid token signature" })
  end
  
  -- check expiration separately
  if jwt.claims.exp and jwt.claims.exp < ngx.time() then
    kong.log.err("[jwt-custom-claims] token expired")
    return kong.response.exit(401, { message = "Expired token" })
  end

  
  local claims = jwt.claims
  kong.log.debug("[jwt-custom-claims] claims: ", cjson.encode(claims))

  -- optional headers
  if conf.add_user_info_headers then
    local email = claims.email
               or claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"]
    if email then
      kong.service.request.set_header("X-User-Email", email)
    end
    kong.service.request.set_header("X-User-Type", claims.UserType or "")
  end

  -- map to consumer + ACL
  local user_type = claims.UserType
  local group     = user_type_to_acl[user_type] or "authenticated"
  local cid       = claims.sub
                 or claims.NameIdentifier
                 or claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"]
                 or "jwt-user-id"
  local cun       = claims.preferred_username
                 or claims.email
                 or claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"]
                 or "jwt-user"

  ngx.ctx.authenticated_consumer = {
    id       = cid,
    username = cun,
  }
  ngx.ctx.authenticated_groups = { group }
  kong.client.authenticate(ngx.ctx.authenticated_consumer)

  if conf.map_user_type_to_acl then
    kong.service.request.set_header("X-Consumer-Groups", group)
    kong.service.request.set_header("X-Consumer-Username", cun)
  end

  -- inject UserId into JSON bodies on write methods
  local method = kong.request.get_method()
  if cid and (method == "POST" or method == "PUT" or method == "PATCH") then
    local ok, err = pcall(function()
      local raw     = kong.request.get_raw_body() or ""
      local content = kong.request.get_header("Content-Type") or ""
      local tbl     = {}

      if raw:len() > 0 and content:find("application/json") then
        local decoded, dec_err = cjson.decode(raw)
        if decoded then
          tbl = decoded
        else
          kong.log.warn("[jwt-custom-claims] JSON decode failed: ", dec_err)
        end
      end

      tbl.UserId = cid
      local new_body = cjson.encode(tbl)
      kong.service.request.set_raw_body(new_body)
      kong.service.request.set_header("Content-Type", "application/json")
      kong.service.request.set_header("Content-Length", #new_body)
    end)
    if not ok then
      kong.log.err("[jwt-custom-claims] body inject error: ", err)
    end
  end

  kong.log.debug("[jwt-custom-claims] access complete for: ", path)
end

return JwtCustomClaimsHandler