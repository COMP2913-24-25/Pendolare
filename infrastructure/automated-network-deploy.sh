#!/bin/bash
# Automated script to deploy and configure networking between Kong and Message Service

# Required parameters
RESOURCE_GROUP=${1:-"dev"}
MESSAGE_SERVICE_NAME=${2:-"message-service"}
KONG_GATEWAY_NAME=${3:-"kong-gateway"}
CONTAINER_APP_ENV=${4:-"pendo-env-dev"}

# Verify prerequisites
echo "Checking if Azure CLI is installed..."
if ! command -v az &> /dev/null; then
    echo "Azure CLI could not be found. Please install it first."
    exit 1
fi

# Verify login status
echo "Checking Azure login status..."
ACCOUNT=$(az account show --query name -o tsv 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "Not logged in to Azure. Please run 'az login' first."
    exit 1
fi

echo "Logged in as: $ACCOUNT"
echo "Using resource group: $RESOURCE_GROUP"

# Setup network configuration
echo "Setting up network configuration..."

# 1. Verify the Container App Environment exists
ENV_ID=$(az containerapp env show --name $CONTAINER_APP_ENV --resource-group $RESOURCE_GROUP --query id -o tsv 2>/dev/null)
if [ $? -ne 0 ]; then
    echo "Container App Environment '$CONTAINER_APP_ENV' not found. Creating..."
    az containerapp env create --name $CONTAINER_APP_ENV --resource-group $RESOURCE_GROUP --location uksouth
    ENV_ID=$(az containerapp env show --name $CONTAINER_APP_ENV --resource-group $RESOURCE_GROUP --query id -o tsv)
fi

echo "Using Container App Environment: $ENV_ID"

# 2. Get Kong Gateway and Message Service FQDNs
echo "Getting service endpoints..."
KONG_FQDN=$(az containerapp show --name $KONG_GATEWAY_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv 2>/dev/null)
KONG_STATUS=$?

MESSAGE_FQDN=$(az containerapp show --name $MESSAGE_SERVICE_NAME --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn -o tsv 2>/dev/null)
MESSAGE_STATUS=$?

# 3. Verify both services exist
if [ $KONG_STATUS -ne 0 ]; then
    echo "Kong Gateway '$KONG_GATEWAY_NAME' not found. Please deploy it first."
    exit 1
fi

if [ $MESSAGE_STATUS -ne 0 ]; then
    echo "Message Service '$MESSAGE_SERVICE_NAME' not found. Please deploy it first."
    exit 1
fi

echo "Kong Gateway FQDN: $KONG_FQDN"
echo "Message Service FQDN: $MESSAGE_FQDN"

# 4. Update environment variables to establish communication
echo "Configuring service communication..."

# Add Kong Gateway URL to Message Service environment
az containerapp update \
    --name $MESSAGE_SERVICE_NAME \
    --resource-group $RESOURCE_GROUP \
    --set-env-vars "KONG_GATEWAY_URL=https://$KONG_FQDN" \
    --set-env-vars "SERVICE_NAME=$MESSAGE_SERVICE_NAME" \
    --set-env-vars "CONTAINER_APP_ENV=$CONTAINER_APP_ENV"

echo "Environment variables updated."

# 5. Output confirmation of successful setup
echo "Network configuration completed successfully!"
echo ""
echo "Your services are now set up for internal communication:"
echo "- Kong Gateway: $KONG_GATEWAY_NAME"
echo "- Message Service: $MESSAGE_SERVICE_NAME"
echo "- Environment: $CONTAINER_APP_ENV"
echo ""
echo "To test the connection, access the Kong Gateway at: https://$KONG_FQDN/ws"
