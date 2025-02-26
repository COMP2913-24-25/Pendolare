# PowerShell script to check Kong's configuration

$kongFqdn = "kong-gateway.greensand-8499b34e.uksouth.azurecontainerapps.io"

Write-Host "Getting Kong services..."
$services = Invoke-RestMethod -Method GET -Uri "https://$kongFqdn/admin-api/services"
Write-Host "Services: $($services | ConvertTo-Json -Depth 1)"

Write-Host "Getting message-service details..."
$messageService = Invoke-RestMethod -Method GET -Uri "https://$kongFqdn/admin-api/services/message-service"
Write-Host "Message Service: $($messageService | ConvertTo-Json -Depth 1)"

Write-Host "Getting routes for message-service..."
$routes = Invoke-RestMethod -Method GET -Uri "https://$kongFqdn/admin-api/services/message-service/routes"
Write-Host "Routes: $($routes | ConvertTo-Json -Depth 3)"
