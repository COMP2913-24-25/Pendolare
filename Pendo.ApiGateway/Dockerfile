FROM kong:3.4

# Set environment variables for WebSocket timeouts
ENV KONG_NGINX_PROXY_READ_TIMEOUT=3600s
ENV KONG_NGINX_PROXY_SEND_TIMEOUT=3600s
ENV KONG_NGINX_PROXY_CONNECT_TIMEOUT=60s
ENV KONG_NGINX_PROXY_WEBSOCKET_TIMEOUT=3600s
ENV KONG_NGINX_PROXY_WEBSOCKET_PING_INTERVAL=30s
ENV KONG_NGINX_UPSTREAM_KEEPALIVE_TIMEOUT=60s

# Create directories with proper permissions first
USER root
RUN mkdir -p /usr/local/kong/declarative /usr/local/kong/templates

# Copy the declarative configs and templates
COPY ./kong/declarative/kong-azure.yml /usr/local/kong/declarative/
COPY ./kong/declarative/kong.yml /usr/local/kong/declarative/
COPY ./kong/custom_nginx.template /usr/local/kong/templates/nginx.conf

# Set proper permissions
RUN chmod 644 /usr/local/kong/declarative/* \
    && chmod 644 /usr/local/kong/templates/nginx.conf \
    && chown -R kong:kong /usr/local/kong

# Switch back to kong user for security
USER kong

# Configure Kong
ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/usr/local/kong/declarative/kong-azure.yml
ENV KONG_PROXY_ACCESS_LOG=/dev/stdout
ENV KONG_ADMIN_ACCESS_LOG=/dev/stdout
ENV KONG_PROXY_ERROR_LOG=/dev/stderr
ENV KONG_ADMIN_ERROR_LOG=/dev/stderr
ENV KONG_ADMIN_LISTEN=0.0.0.0:8001
ENV KONG_LOG_LEVEL=debug

# Use the custom Nginx template
ENV KONG_NGINX_CONF=/usr/local/kong/templates/nginx.conf

# Add external DNS resolver for Azure
ENV KONG_NGINX_RESOLVER=8.8.8.8

# Set WebSocket specific options
ENV KONG_NGINX_HTTP_MAP="$http_upgrade $connection_upgrade { default upgrade; '' close; }"

# Health check to ensure Kong is running
HEALTHCHECK --interval=10s --timeout=10s --retries=5 CMD kong health

# The port Kong listens on
EXPOSE 8000 8001 8443 8444

# Start Kong
CMD ["kong", "docker-start"]
