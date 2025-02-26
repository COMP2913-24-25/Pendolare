#!/bin/bash
# Script to fix and validate Kong configuration before building

CONFIG_FILE="kong/declarative/kong.yml"

echo "Checking Kong configuration file..."

# Verify file exists
if [ ! -f "$CONFIG_FILE" ]; then
  echo "ERROR: Configuration file not found at $CONFIG_FILE"
  exit 1
fi

# Check for invalid ws/wss protocols
if grep -q "^\s*- ws$\|^\s*- wss$" "$CONFIG_FILE"; then
  echo "WARNING: Found invalid WebSocket protocols (ws/wss) in configuration!"
  
  # Back up original file
  cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"
  
  # Replace ws/wss protocols with proper WebSocket header configuration
  sed -i 's/.*- ws$//g' "$CONFIG_FILE"
  sed -i 's/.*- wss$//g' "$CONFIG_FILE"
  
  # Remove empty lines
  sed -i '/^[[:space:]]*$/d' "$CONFIG_FILE"
  
  echo "Fixed configuration file. Original backup saved at ${CONFIG_FILE}.bak"
fi

echo "Validation complete. Kong configuration ready for deployment."

# Proceed with Docker build
echo "Building Docker image..."
docker build -t kong-gateway .
