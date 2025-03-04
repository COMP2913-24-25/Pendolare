FROM kong:latest

USER root

# Create directories with proper permissions first
RUN mkdir -p /usr/local/kong/declarative /usr/local/kong/templates /usr/local/kong/scripts \
    /usr/local/share/lua/5.1/kong/plugins/jwt-custom-claims

# Copy the declarative configs and templates
COPY ./kong/declarative/kong-azure.yml /usr/local/kong/declarative/
COPY ./kong/declarative/kong.yml /usr/local/kong/declarative/
COPY ./kong/declarative/custom-plugins.yml /usr/local/kong/declarative/

# Copy custom Lua scripts
COPY ./kong/scripts/jwt_custom_claims.lua /usr/local/kong/scripts/

# Copy plugin files to the CORRECT Kong's plugin directory
COPY ./kong/plugins/jwt-custom-claims/handler.lua /usr/local/share/lua/5.1/kong/plugins/jwt-custom-claims/
COPY ./kong/plugins/jwt-custom-claims/schema.lua /usr/local/share/lua/5.1/kong/plugins/jwt-custom-claims/
COPY ./kong/plugins/jwt-custom-claims/init.lua /usr/local/share/lua/5.1/kong/plugins/jwt-custom-claims/
COPY ./kong/plugins/jwt-custom-claims/helpers.lua /usr/local/share/lua/5.1/kong/plugins/jwt-custom-claims/

# Set proper permissions
RUN chmod 644 /usr/local/kong/declarative/* /usr/local/kong/scripts/* \
    /usr/local/share/lua/5.1/kong/plugins/jwt-custom-claims/* \
    && chown -R kong:kong /usr/local/kong /usr/local/share/lua/5.1/kong/plugins/jwt-custom-claims

# Switch back to kong user for security
USER kong

# Configure Kong
ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/usr/local/kong/declarative/kong.yml
ENV KONG_PROXY_ACCESS_LOG=/dev/stdout
ENV KONG_ADMIN_ACCESS_LOG=/dev/stdout
ENV KONG_PROXY_ERROR_LOG=/dev/stderr
ENV KONG_ADMIN_ERROR_LOG=/dev/stderr
ENV KONG_ADMIN_LISTEN=0.0.0.0:8001
ENV KONG_LOG_LEVEL=debug
ENV KONG_PLUGINS="bundled,jwt-custom-claims"

# The port Kong listens on
EXPOSE 8000 8001 8443 8444

# Start Kong
CMD ["kong", "docker-start"]
