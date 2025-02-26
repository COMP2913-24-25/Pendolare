#!/bin/bash
# Script to prepare and build Kong Gateway Docker image

echo "Checking directory structure..."
ls -la

# Ensure the proper directory structure exists
if [ -f "kong/declarative/kong.yml" ]; then
  echo "Found kong.yml at the expected location"
elif [ -d "kong/declarative" ]; then
  echo "Directory exists but kong.yml not found"
else
  echo "Creating necessary directories..."
  mkdir -p kong/declarative
  
  # If kong.yml exists in another location, copy it
  if [ -f "kong.yml" ]; then
    cp kong.yml kong/declarative/
  else
    echo "ERROR: kong.yml not found"
    exit 1
  fi
fi

# Proceed with the Docker build
echo "Building Docker image..."
docker build -t kong-gateway .
