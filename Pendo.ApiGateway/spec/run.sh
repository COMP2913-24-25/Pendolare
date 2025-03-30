#!/bin/bash
# Run unit tests for Kong plugins

# Set up environment
KONG_PREFIX=$(mktemp -d)
export KONG_PREFIX

# Run the tests using busted
busted -v --pattern="spec" ./kong/plugins/jwt-custom-claims

# Clean up
rm -rf $KONG_PREFIX
