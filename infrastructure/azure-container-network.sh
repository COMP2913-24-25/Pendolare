#!/bin/bash
# Script to configure internal networking between Kong Gateway and Message Service

# Set up environment variables
RESOURCE_GROUP="dev"
KONG_APP="kong-gateway"
MESSAGE_APP="message-service"

# Get FQDNs for both services
KONG_FQDN=$(az containerapp show --name $KONG_APP --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)
MESSAGE_FQDN=$(az containerapp show --name $MESSAGE_APP --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv)

echo "Kong Gateway FQDN: $KONG_FQDN"
echo "Message Service FQDN: $MESSAGE_FQDN"

# Update environment variables for Message Service to know about Kong
echo "Updating Message Service environment variables..."
az containerapp update \
  --name $MESSAGE_APP \
  --resource-group $RESOURCE_GROUP \
  --set-env-vars "KONG_GATEWAY_URL=https://$KONG_FQDN"

# Check if services are in the same environment
KONG_ENV=$(az containerapp show --name $KONG_APP --resource-group $RESOURCE_GROUP --query properties.managedEnvironmentId -o tsv)
MESSAGE_ENV=$(az containerapp show --name $MESSAGE_APP --resource-group $RESOURCE_GROUP --query properties.managedEnvironmentId -o tsv)

if [ "$KONG_ENV" == "$MESSAGE_ENV" ]; then
  echo "Services are in the same Container App Environment. Internal networking is available."
  echo "Message Service can reach Kong at: http://$KONG_APP:8000"
  echo "Kong can reach Message Service at: http://$MESSAGE_APP:5006"
else
  echo "WARNING: Services are in different environments. Internal networking won't work correctly."
  echo "You should deploy both services to the same Container App Environment."
fi

echo "Setup complete! Message Service should now be able to communicate with Kong Gateway."
