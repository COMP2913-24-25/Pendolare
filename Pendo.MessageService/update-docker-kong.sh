#!/bin/bash

echo "Stopping and removing existing containers..."
docker-compose -f docker-compose.message-kong.yml down

echo "Building containers..."
docker-compose -f docker-compose.message-kong.yml build --no-cache

echo "Starting containers..."
docker-compose -f docker-compose.message-kong.yml up -d

echo "Containers started. Access the test client at: http://localhost:5007/test-client"
