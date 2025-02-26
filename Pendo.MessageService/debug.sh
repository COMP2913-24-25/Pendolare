#!/bin/bash
# WebSocket debugging script for Azure Container Apps

echo "WebSocket Connection Debugging Tool"
echo "=================================="

# Check if deployed in Azure
if [ -z "$CONTAINER_APP_ENV" ]; then
  echo "Not running in Azure Container Apps environment"
  echo "Please set the following environment variables:"
  echo "  MESSAGE_SERVICE_FQDN - FQDN of the message service"
  echo "  KONG_GATEWAY_URL - URL of the Kong Gateway"
  echo ""
  
  # Use environment variables if set, otherwise prompt for input
  if [ -z "$MESSAGE_SERVICE_FQDN" ]; then
    read -p "Enter message service FQDN: " MESSAGE_SERVICE_FQDN
    export MESSAGE_SERVICE_FQDN
  fi
  
  if [ -z "$KONG_GATEWAY_URL" ]; then
    read -p "Enter Kong Gateway URL: " KONG_GATEWAY_URL
    export KONG_GATEWAY_URL
  fi
else
  echo "Running in Azure Container Apps environment: $CONTAINER_APP_ENV"
fi

echo ""
echo "Testing direct connection to message service..."
python -m src.debug

echo ""
echo "Testing connection through Kong Gateway..."
python -m src.debug kong

echo ""
echo "Complete connection diagnostic information:"
echo "----------------------------------------"
echo "Message Service FQDN: $MESSAGE_SERVICE_FQDN"
echo "Kong Gateway URL: $KONG_GATEWAY_URL"
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"

# Try a simple curl test for HTTP endpoints
echo ""
echo "Testing HTTP endpoints..."
if command -v curl &> /dev/null; then
  echo "Testing direct health endpoint:"
  curl -v https://$MESSAGE_SERVICE_FQDN/health 2>&1 | grep -E '(< HTTP|< Content-Type|^{)'
  
  echo ""
  echo "Testing Kong routing:"
  curl -v https://$KONG_GATEWAY_URL/status 2>&1 | grep -E '(< HTTP|< Content-Type|^{)'
else
  echo "curl command not found, skipping HTTP tests"
fi
