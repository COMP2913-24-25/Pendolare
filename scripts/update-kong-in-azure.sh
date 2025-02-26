#!/bin/bash
# Script to update Kong Gateway configuration in Azure

# Get Kong Gateway FQDN
KONG_FQDN="kong-gateway.greensand-8499b34e.uksouth.azurecontainerapps.io"
MESSAGE_FQDN="message-service.greensand-8499b34e.uksouth.azurecontainerapps.io"

echo "Updating Kong Gateway with Message Service URL..."
echo "Kong Gateway FQDN: $KONG_FQDN"
echo "Message Service FQDN: $MESSAGE_FQDN"

# Update the message service configuration via Admin API
echo "Creating/updating Message Service in Kong..."
curl -i -X PUT https://$KONG_FQDN/admin-api/services/message-service \
  -H "Content-Type: application/json" \
  -d "{\"url\":\"https://$MESSAGE_FQDN\"}"

# Configure WebSocket route
echo "Configuring WebSocket route..."
curl -i -X PUT https://$KONG_FQDN/admin-api/services/message-service/routes/message-ws-route \
  -H "Content-Type: application/json" \
  -d '{
    "paths": ["/message/ws"],
    "protocols": ["http", "https"],
    "headers": {"Upgrade": ["websocket"], "Connection": ["Upgrade"]},
    "strip_path": false,
    "preserve_host": false
  }'

# Add CORS plugin specifically for this service
echo "Adding CORS plugin..."
curl -i -X POST https://$KONG_FQDN/admin-api/services/message-service/plugins \
  -H "Content-Type: application/json" \
  -d '{
    "name": "cors",
    "config": {
      "origins": ["*"],
      "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
      "headers": ["Accept", "Authorization", "Content-Type", "Upgrade", "Connection"],
      "exposed_headers": ["Authorization"],
      "credentials": true,
      "max_age": 3600
    }
  }'

echo "Kong Gateway configuration updated successfully!"
