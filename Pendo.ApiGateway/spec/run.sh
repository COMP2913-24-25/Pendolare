#!/bin/bash
# Run unit tests for Kong plugins

# Set up environment
KONG_PREFIX=$(mktemp -d)
export KONG_PREFIX

# Run the tests using busted with JUnit output
busted -v --output=junit ./kong/plugins/jwt-custom-claims/spec > apigateway_test_results.xml

# Clean up
rm -rf $KONG_PREFIX
