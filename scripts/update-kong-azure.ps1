# PowerShell script to update Kong's configuration in Azure

# Set the FQDNs for your services
$kongFqdn = "kong-gateway.greensand-8499b34e.uksouth.azurecontainerapps.io"
$messageFqdn = "message-service.greensand-8499b34e.uksouth.azurecontainerapps.io"

Write-Host "Updating Kong config to use Message Service FQDN: $messageFqdn"

# Delete existing service if it exists (to ensure clean update)
Invoke-RestMethod -Method DELETE -Uri "https://$kongFqdn/admin-api/services/message-service" -ErrorAction SilentlyContinue

# Create message-service in Kong with correct HTTPS URL
$body = @{
    name = "message-service"
    url = "https://$messageFqdn"
} | ConvertTo-Json

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
