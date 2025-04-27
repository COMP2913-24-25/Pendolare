#!/bin/bash
# Run unit tests for Kong plugins

# Set up environment
KONG_PREFIX=$(mktemp -d)
export KONG_PREFIX

# Run the tests using busted with JUnit output directly
busted -v --output=junit --junit_output_file=apigateway_test_results.xml ./kong/plugins/jwt-custom-claims/spec

# Clean up
rm -rf $KONG_PREFIX
