# Simple Azure Cloud Shell script to set up SQL access
# Just copy and paste this entire script into Azure Cloud Shell

# Set your values here
$ResourceGroup = "dev"
$SqlServerName = "pendolare"
$SqlDatabaseName = "Pendolare.Database"
$ContainerAppName = "identity-service"
$ContainerAppEnvName = "pendo-env-dev"

# 1. Enable Azure services access to SQL
Write-Host "Adding 'Allow Azure Services' rule to SQL firewall..." -ForegroundColor Cyan
az sql server firewall-rule create `
    --resource-group $ResourceGroup `
    --server $SqlServerName `
    --name "AllowAllWindowsAzureIps" `
    --start-ip-address "0.0.0.0" `
    --end-ip-address "0.0.0.0"

# 2. Get Container App Environment outbound IP
Write-Host "Getting Container App outbound IP..." -ForegroundColor Cyan
$outboundIp = az containerapp env show `
    --name $ContainerAppEnvName `
    --resource-group $ResourceGroup `
    --query properties.staticIp -o tsv

# 3. Add Container App outbound IP to SQL firewall
if ($outboundIp) {
    Write-Host "Adding Container App IP $outboundIp to SQL firewall..." -ForegroundColor Cyan
    az sql server firewall-rule create `
        --resource-group $ResourceGroup `
        --server $SqlServerName `
        --name "ContainerAppOutbound" `
        --start-ip-address $outboundIp `
        --end-ip-address $outboundIp
}

# 4. Enable system-assigned managed identity for Container App
Write-Host "Enabling system-assigned managed identity for Container App..." -ForegroundColor Cyan
$result = az containerapp identity assign `
    --name $ContainerAppName `
    --resource-group $ResourceGroup `
    --system-assigned

# 5. Get the principal ID
$principalId = ($result | ConvertFrom-Json).identity.principalId
Write-Host "Container App managed identity principal ID: $principalId" -ForegroundColor Green

# 6. Show the SQL commands to run
Write-Host "`nRun these commands in your SQL database:" -ForegroundColor Yellow
Write-Host "CREATE USER [$ContainerAppName] FROM EXTERNAL PROVIDER;" -ForegroundColor White
Write-Host "ALTER ROLE db_datareader ADD MEMBER [$ContainerAppName];" -ForegroundColor White
Write-Host "ALTER ROLE db_datawriter ADD MEMBER [$ContainerAppName];" -ForegroundColor White
Write-Host "ALTER ROLE db_ddladmin ADD MEMBER [$ContainerAppName];" -ForegroundColor White

# 7. Restart the Container App
Write-Host "`nRestarting Container App..." -ForegroundColor Cyan
az containerapp restart --name $ContainerAppName --resource-group $ResourceGroup

Write-Host "`nSetup complete!" -ForegroundColor Green
