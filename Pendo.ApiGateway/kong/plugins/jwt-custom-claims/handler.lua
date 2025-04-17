local jwt_decoder = require "kong.plugins.jwt.jwt_parser"
local cjson = require "cjson.safe"
local kong = kong

local JwtCustomClaimsHandler = {
  PRIORITY = 1010, -- Run before the ACL Plugin (default priority 1000)
  VERSION = "1.0.0"
}

-- List of public paths that bypass JWT verification entirely
local public_paths = {
  "/api/Identity/RequestOtp",
  "/api/Identity/VerifyOtp",
  "/api/Identity/Ping",
  "/api/Booking/HealthCheck",
  "/api/Admin/HealthCheck",
  "/api/Message/HealthCheck",
  "/api/Journey/HealthCheck",
  "/api/PaymentService/HealthCheck",
  "/api/PaymentService/StripeWebhook"
}

-- Define user type to ACL group mapping
local user_type_to_acl = {
  ["Manager"] = "manager",
  ["User"] = "authenticated"
  -- Default will be "authenticated" for any other user type or if UserType claim is missing
}


-- JWT Documentation at: https://konghq.com/blog/engineering/craft-and-sign-custom-jwt
-- Reference JWTClaim codebase: https://github.com/wshirey/kong-plugin-jwt-claims-validate/blob/master/handler.lua

function JwtCustomClaimsHandler:access(conf)
  local request_path = kong.request.get_path()

  -- Check if the path is public
  for _, public_path in ipairs(public_paths) do
    if request_path:find("^" .. public_path) then
      kong.log.debug("[jwt-custom-claims] Skipping JWT verification for public path: ", request_path)
      -- Set anonymous context ONLY if an ACL plugin might check this route later
      -- This ensures ACL allows 'anonymous' group if configured on the route
      ngx.ctx.authenticated_consumer = { id = "anonymous-consumer-id", username = "anonymous" }
      ngx.ctx.authenticated_groups = { "anonymous" }
      kong.client.authenticate(ngx.ctx.authenticated_consumer) -- Make context available to other plugins like ACL
      return -- Bypass JWT processing for public paths
    end
  end

  -- Get the JWT token from the Authorization header
  local token_header = kong.request.get_header("Authorization")
  if not token_header then
    kong.log.debug("[jwt-custom-claims] No Authorization header found for path: ", request_path, ". Treating as anonymous.")
    -- If no token, set context for anonymous access for ACL plugin
    ngx.ctx.authenticated_consumer = { id = "anonymous-consumer-id", username = "anonymous" }
    ngx.ctx.authenticated_groups = { "anonymous" }
    kong.client.authenticate(ngx.ctx.authenticated_consumer)
    return -- Allow anonymous access attempt (ACL plugin will verify route permissions)
  end

  -- Parse the JWT token
  local jwt_token_str = token_header:gsub("^[Bb]earer%s+", "")
  local jwt_obj, err = jwt_decoder:new(jwt_token_str)
  if err then
    kong.log.err("[jwt-custom-claims] Failed to parse JWT: ", err)
    return kong.response.exit(401, { message = "Invalid or malformed token" })
  end

  -- Verify the JWT signature
  local valid, err_msg = jwt_obj:verify_signature({})

  -- Check if the token is expired
  if not valid or jwt_obj:is_expired() then
    kong.log.err("[jwt-custom-claims] JWT verification failed: ", err_msg or "Token expired")
    return kong.response.exit(401, { message = "Invalid or expired token" })
  end

  -- Perform JWT claim checks
  local jwt_claims = jwt_obj.claims
  kong.log.debug("[jwt-custom-claims] JWT claims: ", cjson.encode(jwt_claims))

  -- Set user info headers if specified in the config
  if conf.add_user_info_headers then
    local user_email = jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"] or jwt_claims["email"]
    if user_email then
      kong.service.request.set_header("X-User-Email", user_email)
      kong.log.debug("[jwt-custom-claims] Set X-User-Email header.")
    end
    kong.service.request.set_header("X-User-Type", jwt_claims["UserType"] or "")
    kong.log.debug("[jwt-custom-claims] Set X-User-Type header.")
  end

  local user_type = jwt_claims["UserType"]
  local acl_group = user_type_to_acl[user_type] or "authenticated" -- Default to authenticated

  -- Extract identifiers, providing fallbacks
  local consumer_id = jwt_claims["NameIdentifier"]
                    or jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"]
                    or jwt_claims["sub"] -- Common JWT subject claim
                    or "jwt-user-id" -- Fallback ID
  local consumer_username = jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/name"]
                          or jwt_claims["preferred_username"] -- Common OIDC claim
                          or jwt_claims["email"] -- Common claim
                          or "jwt-user" -- Fallback username

  -- Set context for the ACL plugin
  ngx.ctx.authenticated_consumer = {
    id = consumer_id,
    username = consumer_username
  }
  ngx.ctx.authenticated_groups = { acl_group }

  kong.log.debug("[jwt-custom-claims] Mapped UserType '" .. (user_type or "nil") .. "' to ACL group: '" .. acl_group .. "' for consumer: '" .. consumer_username .. "'")

  -- Authenticate the consumer for Kong's context (makes it available to other plugins)
  kong.client.authenticate(ngx.ctx.authenticated_consumer)

  -- Set legacy headers if needed by ACL plugin (should use ngx.ctx primarily, but set for compatibility if unsure)
  if conf.map_user_type_to_acl then
      kong.service.request.set_header("X-Consumer-Groups", acl_group)
      kong.service.request.set_header("X-Consumer-Username", consumer_username)
      kong.log.debug("[jwt-custom-claims] Set X-Consumer-Groups and X-Consumer-Username headers.")
  end

  local user_id = jwt_claims["NameIdentifier"] or jwt_claims["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"]
  local http_method = kong.request.get_method()

  if user_id and (http_method == "POST" or http_method == "PUT" or http_method == "PATCH") then
    kong.log.debug("[jwt-custom-claims] Attempting to add UserId: " .. user_id .. " to request body for method " .. http_method)

    local success, err = pcall(function()
      local body_raw = kong.request.get_raw_body()
      local body = {}
      local content_type = kong.request.get_header("Content-Type") or ""

      -- Try to parse existing body only if it's JSON and not empty
      if body_raw and #body_raw > 0 then
        if content_type:find("application/json") then
          local decoded, decode_err = cjson.decode(body_raw)
          if decoded then
            body = decoded
          else
             kong.log.warn("[jwt-custom-claims] Failed to decode existing JSON body: ", decode_err, ". Proceeding cautiously.")
             -- If decoding fails but content-type is JSON, maybe it's just `null` or empty string.
             body = {} -- Reset body to ensure UserId is added to a valid table
          end
        else
           kong.log.warn("[jwt-custom-claims] Request body exists but is not application/json (Content-Type: ", content_type, "). Cannot inject UserId into body.")
           return -- Do not modify non-JSON body
        end
      end

      -- Add/overwrite UserId in the body table
      body["UserId"] = user_id

      -- Convert back to JSON
      local json_body = cjson.encode(body)

      -- Set the modified body back
      kong.service.request.set_raw_body(json_body)
      kong.service.request.set_header("Content-Type", "application/json")
      kong.service.request.set_header("Content-Length", #json_body)

      kong.log.debug("[jwt-custom-claims] Modified body: " .. json_body)
    end)

    if not success then
      kong.log.err("[jwt-custom-claims] Error modifying request body: " .. tostring(err))
    end
  elseif user_id then
     kong.log.debug("[jwt-custom-claims] UserId found but request method is ", http_method, ". Not modifying body.")
  else
    kong.log.debug("[jwt-custom-claims] No NameIdentifier claim found in JWT token. Not modifying body.")
  end

  kong.log.debug("[jwt-custom-claims] Access checks passed for path: ", request_path)

end

return JwtCustomClaimsHandler