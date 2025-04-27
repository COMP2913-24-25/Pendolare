#!/bin/bash
# Run unit tests for Kong plugins

# Set up environment
KONG_PREFIX=$(mktemp -d)
export KONG_PREFIX

# Download Kong source for test helpers if not present
if [ ! -d "./spec/kong-spec" ]; then
  git clone --depth 1 --branch 3.4.0 https://github.com/Kong/kong.git ./spec/kong-spec
fi

# Set LUA_PATH to include Kong's spec helpers
export LUA_PATH="./spec/kong-spec/spec/?.lua;;$LUA_PATH"

# Run the tests using busted with JUnit output redirected to a file
busted -v --output=junit ./kong/plugins/jwt-custom-claims/spec 2> apigateway_test_results.xml

# Clean up
rm -rf $KONG_PREFIX
