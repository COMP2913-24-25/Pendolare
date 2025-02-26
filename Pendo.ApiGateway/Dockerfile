FROM kong:3.4

# Set environment variables for WebSocket timeouts
ENV KONG_NGINX_PROXY_READ_TIMEOUT=3600
ENV KONG_NGINX_PROXY_SEND_TIMEOUT=3600
ENV KONG_NGINX_PROXY_WEBSOCKET_TIMEOUT=3600
ENV KONG_NGINX_PROXY_WEBSOCKET_PING_INTERVAL=30

# Copy the declarative config
COPY ./kong/declarative /usr/local/kong/declarative/

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

# Remove invalid timeout env vars; use custom Nginx template instead.
ENV KONG_NGINX_CONF=/usr/local/kong/custom_nginx.template

# Add external DNS resolver for Azure
ENV KONG_NGINX_RESOLVER=8.8.8.8

# Health check to ensure Kong is running
HEALTHCHECK --interval=10s --timeout=10s --retries=3 CMD kong health

# The port Kong listens on
EXPOSE 8000 8001 8443 8444

# Start Kong
CMD ["kong", "start"]
