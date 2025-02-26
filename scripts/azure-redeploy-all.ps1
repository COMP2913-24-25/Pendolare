# PowerShell script to update both Kong Gateway and Message Service in Azure

param(
    [string]$ResourceGroup = "dev",
    [string]$KongAppName = "kong-gateway",
    [string]$MessageServiceAppName = "message-service"
)

Write-Host "======================================================="
Write-Host "   Full Redeployment of Kong Gateway + Message Service"
Write-Host "======================================================="

# Get the FQDNs for the services
Write-Host "Getting Container App FQDNs..."
$kongFqdn = az containerapp show --name $KongAppName --resource-group $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv
$messageFqdn = az containerapp show --name $MessageServiceAppName --resource-group $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv

Write-Host "Kong Gateway FQDN: $kongFqdn"
Write-Host "Message Service FQDN: $messageFqdn"

# Update the kong-azure.yml configuration with the real FQDN
$kongYmlPath = "Pendo.ApiGateway/kong/declarative/kong-azure.yml"
Write-Host "Updating Kong Azure Config at $kongYmlPath..."

# Read and update the content
if (Test-Path $kongYmlPath) {
    $content = Get-Content $kongYmlPath -Raw
    $content = $content -replace "message-service.greensand-8499b34e.uksouth.azurecontainerapps.io", $messageFqdn
    Set-Content -Path $kongYmlPath -Value $content
    Write-Host "Updated Kong config with Message Service FQDN: $messageFqdn"
}
else {
    Write-Host "Warning: Could not find Kong Azure config at $kongYmlPath"
}

# Build and push Kong Gateway
Write-Host "Building and pushing Kong Gateway image..."
$acrUsername = az acr credential show -n pendocontainerregistry --query "username" -o tsv
$acrPassword = az acr credential show -n pendocontainerregistry --query "passwords[0].value" -o tsv

# Copy the Azure config in place of the regular config for the docker build
Copy-Item $kongYmlPath "Pendo.ApiGateway/kong/declarative/kong.yml" -Force
Write-Host "Copied Azure configuration to main Kong config path"

# Login to ACR
az acr login -n pendocontainerregistry

# Build and push Kong image
Set-Location Pendo.ApiGateway
docker build . -t pendocontainerregistry.azurecr.io/kong-gateway:latest
docker push pendocontainerregistry.azurecr.io/kong-gateway:latest

# Return to root directory
Set-Location ..

# Update Kong Gateway in Azure
Write-Host "Updating Kong Gateway in Azure..."
az deployment group create `
    --resource-group $ResourceGroup `
    --template-file infrastructure/gateway-service.bicep `
    --parameters `
        containerAppName=$KongAppName `
        containerAppEnvironmentName=pendo-env-dev `
        registryName=pendocontainerregistry `
        registryUsername=$acrUsername `
        registryPassword=$acrPassword

# Wait for Kong to become available
Write-Host "Waiting for Kong Gateway to become available..."
Start-Sleep -Seconds 30

# Update Kong's configuration through the Admin API
Write-Host "Updating Kong Gateway routes via Admin API..."

# Delete existing service if it exists (to ensure clean update)
try {
    Invoke-RestMethod -Method DELETE -Uri "https://$kongFqdn/admin-api/services/message-service" -ErrorAction SilentlyContinue
    Write-Host "Deleted existing message-service configuration"
} catch {
    Write-Host "No existing message-service to delete"
}

# Create message-service in Kong with correct HTTPS URL
$body = @{
    name = "message-service"
    url = "https://$messageFqdn"
} | ConvertTo-Json

try {
    $result = Invoke-RestMethod -Method POST -Uri "https://$kongFqdn/admin-api/services" -Body $body -ContentType "application/json"
    Write-Host "Service created: $($result | ConvertTo-Json -Depth 1)"

    # Configure the WebSocket route
    $routeBody = @{
        name = "message-ws-route"  
        paths = @("/message/ws")
        protocols = @("http", "https")
        headers = @{
            "Upgrade" = @("websocket")
            "Connection" = @("Upgrade")
        }
        strip_path = $false
        preserve_host = $false
    } | ConvertTo-Json -Depth 3

    $routeResult = Invoke-RestMethod -Method POST -Uri "https://$kongFqdn/admin-api/services/message-service/routes" -Body $routeBody -ContentType "application/json"
    Write-Host "Route created: $($routeResult | ConvertTo-Json -Depth 1)"

    Write-Host "Kong configuration updated successfully!"
} catch {
    Write-Host "Error updating Kong configuration: $_"
}

# Open the test client
Start-Process "https://message-service.greensand-8499b34e.uksouth.azurecontainerapps.io/test-client"

Write-Host "======================================================="
Write-Host "   Deployment Complete"
Write-Host "======================================================="
Write-Host "Kong Gateway: https://$kongFqdn"
Write-Host "Message Service: https://$messageFqdn"
Write-Host "WebSocket Endpoint: wss://$kongFqdn/message/ws"
Write-Host "Test Client: https://$messageFqdn/test-client"
