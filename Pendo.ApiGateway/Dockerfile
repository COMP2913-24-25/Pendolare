FROM kong:3.3

# Copy the declarative config
COPY kong/declarative/kong.yml /usr/local/kong/declarative/kong.yml

# Copy custom Nginx template for WebSocket support
COPY kong/custom_nginx.template /usr/local/kong/custom_nginx.template

# Configure Kong
ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/usr/local/kong/declarative/kong.yml
ENV KONG_PROXY_ACCESS_LOG=/dev/stdout
ENV KONG_ADMIN_ACCESS_LOG=/dev/stdout
ENV KONG_PROXY_ERROR_LOG=/dev/stderr
ENV KONG_ADMIN_ERROR_LOG=/dev/stderr
ENV KONG_ADMIN_LISTEN=0.0.0.0:8001
ENV KONG_LOG_LEVEL=debug

# Remove timeout ENV variables that cause "read_timeout" to be injected.
ENV KONG_NGINX_CONF=/usr/local/kong/custom_nginx.template

EXPOSE 8000 8443 8001 8444
