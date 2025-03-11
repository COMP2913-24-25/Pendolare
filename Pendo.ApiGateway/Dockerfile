FROM kong:3.4.0-ubuntu

USER root

# Install dependencies needed for plugin
RUN apt-get update && \
    apt-get install -y git unzip curl lua5.1 luarocks && \
    apt-get clean

RUN mkdir -p /usr/local/kong/declarative /usr/local/kong/templates /usr/local/kong/scripts /usr/local/kong/plugins/jwt-custom-claims /tmp/jwt-custom-claims

COPY ./kong/declarative/kong.yml /usr/local/kong/declarative/
COPY ./kong/declarative/custom-plugins.yml /usr/local/kong/declarative/

COPY ./kong/plugins/jwt-custom-claims /usr/local/kong/plugins/jwt-custom-claims/
COPY ./kong/plugins/jwt-custom-claims /tmp/jwt-custom-claims/

COPY ./kong/plugins/jwt-custom-claims-1.0.0-1.rockspec /tmp/

RUN cd /tmp && luarocks make jwt-custom-claims-1.0.0-1.rockspec

RUN chmod 644 /usr/local/kong/declarative/* /usr/local/kong/plugins/jwt-custom-claims/* \
    && chown -R kong:kong /usr/local/kong/plugins \
    && chown -R kong:kong /usr/local/kong

USER kong

# Configure Kong
ENV KONG_DATABASE=off
ENV KONG_DECLARATIVE_CONFIG=/usr/local/kong/declarative/kong.yml
ENV KONG_PROXY_ACCESS_LOG=/dev/stdout
ENV KONG_ADMIN_ACCESS_LOG=/dev/stdout
ENV KONG_PROXY_ERROR_LOG=/dev/stderr
ENV KONG_ADMIN_ERROR_LOG=/dev/stderr
ENV KONG_ADMIN_LISTEN=0.0.0.0:9001
ENV KONG_PROXY_LISTEN="0.0.0.0:9000, 0.0.0.0:8443 ssl http2"
ENV KONG_LOG_LEVEL=debug
ENV KONG_PLUGINS="bundled,jwt-custom-claims"
ENV KONG_LUA_PACKAGE_PATH="/usr/local/share/lua/5.1/?.lua;/usr/local/share/lua/5.1/?/init.lua;/usr/local/kong/plugins/?.lua;/usr/local/kong/plugins/?/init.lua;;"

# Expose Kong ports
EXPOSE 9000 9001 8443 8444

# Start Kong
CMD ["kong", "docker-start"]
