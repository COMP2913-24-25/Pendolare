#!/bin/bash
# Script to set up networking between Kong Gateway and Message Service in Azure Container Apps

# Environment variables
RESOURCE_GROUP="dev"
CONTAINER_APP_ENV="pendo-env-dev"
KONG_GATEWAY_NAME="kong-gateway"
MESSAGE_SERVICE_NAME="message-service"

# 1. Get Container App Environment details
echo "Getting Container App Environment details..."
ENV_ID=$(az containerapp env show --name $CONTAINER_APP_ENV --resource-group $RESOURCE_GROUP --query id -o tsv)

echo "Container App Environment ID: $ENV_ID"

# 2. Create a connection between Kong Gateway and Message Service
echo "Configuring internal networking..."

# Get Kong Gateway and Message Service internal URIs
KONG_INTERNAL_URI=$(az containerapp show --name $KONG_GATEWAY_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)
MESSAGE_INTERNAL_URI=$(az containerapp show --name $MESSAGE_SERVICE_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)

echo "Kong Gateway internal URI: $KONG_INTERNAL_URI"
echo "Message Service internal URI: $MESSAGE_INTERNAL_URI"

# 3. Update Kong Gateway configuration to include Message Service route
echo "Updating Kong Gateway configuration..."

# Create a temporary Kong configuration update file
cat > kong-config-update.json << EOF
{
  "services": [
    {
      "name": "message-service",
      "url": "http://$MESSAGE_INTERNAL_URI",
      "routes": [
        {
          "name": "message-websocket-route",
          "paths": ["/messages"],
          "protocols": ["http", "https"],
          "headers": {
            "Upgrade": ["websocket"],
            "Connection": ["Upgrade"]
          },
          "strip_path": false
        }
      ]
    }
  ]
}
EOF

# You would need to use kubectl or direct API calls to update Kong's configuration
# This is a placeholder for the actual update method
echo "Kong configuration update prepared - please apply it to your Kong Gateway instance"

# 4. Update Message Service to communicate with Kong Gateway
echo "Setting environment variables for Message Service..."

# Set environment variables for Message Service
az containerapp update --name $MESSAGE_SERVICE_NAME --resource-group $RESOURCE_GROUP \
  --set-env-vars "KONG_GATEWAY_HOST=$KONG_INTERNAL_URI"

echo "Network setup complete!"
