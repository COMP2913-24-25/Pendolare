# Script to update Kong Gateway configuration with proper message service FQDN

param(
    [string]$ResourceGroup = "dev",
    [string]$KongAppName = "kong-gateway",
    [string]$MessageServiceAppName = "message-service"
)

Write-Host "Getting Container App FQDNs..."

# Get the FQDNs for the services
$kongFqdn = az containerapp show --name $KongAppName --resource-group $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv
$messageFqdn = az containerapp show --name $MessageServiceAppName --resource-group $ResourceGroup --query "properties.configuration.ingress.fqdn" -o tsv

Write-Host "Kong Gateway FQDN: $kongFqdn"
Write-Host "Message Service FQDN: $messageFqdn"

# Construct the service URL with HTTPS protocol
$messageServiceUrl = "https://$messageFqdn"

Write-Host "Updating Kong Gateway with Message Service URL: $messageServiceUrl"

# Update Kong Gateway through the Admin API
try {
    # First check if the service exists
    $result = az rest --method GET --uri "https://$kongFqdn/admin-api/services/message-service" 2>&1
    $serviceExists = $LASTEXITCODE -eq 0

    if ($serviceExists) {
        Write-Host "Updating existing message-service in Kong..."
        az rest --method PATCH --uri "https://$kongFqdn/admin-api/services/message-service" --body "{`"url`":`"$messageServiceUrl`"}" --headers "Content-Type=application/json"
    } else {
        Write-Host "Creating new message-service in Kong..."
        az rest --method POST --uri "https://$kongFqdn/admin-api/services" --body "{`"name`":`"message-service`",`"url`":`"$messageServiceUrl`"}" --headers "Content-Type=application/json"
    }

    # Now ensure the WebSocket route exists
    Write-Host "Configuring WebSocket route..."
    az rest --method POST --uri "https://$kongFqdn/admin-api/services/message-service/routes" --body "{`"name`":`"message-ws-route`",`"paths`":[`"/message/ws`"],`"protocols`":[`"http`",`"https`"],`"headers`":{`"Upgrade`":[`"websocket`"],`"Connection`":[`"Upgrade`"]},`"strip_path`":false}" --headers "Content-Type=application/json"

    Write-Host "Kong Gateway configuration updated successfully!"
} catch {
    Write-Error "Failed to update Kong Gateway configuration: $_"
    exit 1
}
