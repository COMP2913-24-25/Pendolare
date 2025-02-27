FROM kong:3.4

# Create directories with proper permissions first
USER root
RUN mkdir -p /usr/local/kong/declarative /usr/local/kong/templates

# Copy the declarative configs and templates
COPY ./kong/declarative/kong-azure.yml /usr/local/kong/declarative/
COPY ./kong/declarative/kong.yml /usr/local/kong/declarative/

# Set proper permissions
RUN chmod 644 /usr/local/kong/declarative/* \
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

# Health check to ensure Kong is running
HEALTHCHECK --interval=10s --timeout=10s --retries=5 CMD kong health

# The port Kong listens on
EXPOSE 8000 8001 8443 8444

# Start Kong
CMD ["kong", "docker-start"]
