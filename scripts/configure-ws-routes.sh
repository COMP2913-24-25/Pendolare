#!/bin/bash

# Get the Azure Container App FQDN
MESSAGE_FQDN=$(az containerapp show --name message-service --resource-group dev --query properties.configuration.ingress.fqdn -o tsv)
KONG_FQDN=$(az containerapp show --name kong-gateway --resource-group dev --query properties.configuration.ingress.fqdn -o tsv)

echo "Message Service: $MESSAGE_FQDN"
echo "Kong Gateway: $KONG_FQDN"

# Update Kong Gateway to route WebSocket connections
echo "Configuring WebSocket route in Kong..."
curl -i -X POST https://$KONG_FQDN/admin-api/services/message-service/routes \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"message-ws-direct\",
    \"paths\": [\"/ws\"],
    \"protocols\": [\"http\",\"https\"],
    \"headers\": {\"Upgrade\": [\"websocket\"], \"Connection\": [\"Upgrade\"]},
    \"strip_path\": false
  }"

# List the routes to confirm
echo "Verifying routes..."
curl https://$KONG_FQDN/admin-api/services/message-service/routes

echo "Testing direct WebSocket connection to Message Service..."
echo "wss://$MESSAGE_FQDN/ws"
