[CmdletBinding()]
param(
    [Parameter()]
    [string]$ResourceGroup = "dev",
    
    [Parameter()]
    [string]$ContainerAppName = "identity-service",
    
    [Parameter()]
    [string]$ConnectionString = "Server=tcp:pendolare.database.windows.net,1433;Initial Catalog=Pendolare.Database;Persist Security Info=False;User ID=comp2913;Password=Securepassword123;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=True;Connection Timeout=30;"
)

# Ensure logged into Azure
$loginStatus = az account show 2>$null
if (-not $loginStatus) {
    Write-Host "Not logged in to Azure. Please login." -ForegroundColor Red
    az login
}

Write-Host "===== Identity Service Connection String Fix =====" -ForegroundColor Cyan

# Check if connection string needs modification
$modifiedConnectionString = $ConnectionString
if ($ConnectionString -match "TrustServerCertificate=False") {
    Write-Host "Changing TrustServerCertificate from False to True..." -ForegroundColor Yellow
    $modifiedConnectionString = $ConnectionString -replace "TrustServerCertificate=False", "TrustServerCertificate=True"
}

# Add retry logic if not already present
if (-not ($modifiedConnectionString -match "ConnectRetryCount=")) {
    Write-Host "Adding connection retry parameters..." -ForegroundColor Yellow
    $modifiedConnectionString = $modifiedConnectionString.TrimEnd(';') + ";ConnectRetryCount=5;ConnectRetryInterval=10;"
}

Write-Host "Modified connection string will be set (password hidden):" -ForegroundColor Green
$displayString = $modifiedConnectionString -replace "Password=[^;]*", "Password=*****"
Write-Host $displayString -ForegroundColor White

# Save connection string to a temp file
$tempFile = Join-Path $env:TEMP "connection-string.txt"
Set-Content -Path $tempFile -Value $modifiedConnectionString -NoNewline

# Set the secret in the container app
Write-Host "`nUpdating Container App with new connection string..." -ForegroundColor Cyan
$result = az containerapp secret set --name $ContainerAppName --resource-group $ResourceGroup --secrets "db-connection-string=$tempFile" 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Connection string secret updated successfully" -ForegroundColor Green
} else {
    Write-Host "× Failed to update connection string: $result" -ForegroundColor Red
}

# Clean up temp file
Remove-Item -Path $tempFile -Force

# Update the container app to apply changes
Write-Host "`nRestarting Container App to apply changes..." -ForegroundColor Cyan
$image = az containerapp show --name $ContainerAppName --resource-group $ResourceGroup --query "properties.template.containers[0].image" -o tsv

if ($image) {
    $result = az containerapp update --name $ContainerAppName --resource-group $ResourceGroup --image $image 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Container App updated successfully" -ForegroundColor Green
        
        # Check logs after a delay
        Write-Host "`nWaiting 30 seconds for app to restart before checking logs..." -ForegroundColor Yellow
        Start-Sleep -Seconds 30
        
        Write-Host "`nChecking logs for database connection issues..." -ForegroundColor Cyan
        $logs = az containerapp logs show --name $ContainerAppName --resource-group $ResourceGroup --tail 20 2>&1
        
        if ($logs -match "ConnectionString property has not been initialized") {
            Write-Host "× Connection string issue still detected in logs" -ForegroundColor Red
        } else {
            Write-Host "✓ No connection string errors found in recent logs" -ForegroundColor Green
        }
    } else {
        Write-Host "× Failed to update Container App: $result" -ForegroundColor Red
    }
} else {
    Write-Host "× Failed to get Container App image" -ForegroundColor Red
}

Write-Host "`n===== Connection String Fix Complete =====" -ForegroundColor Cyan
Write-Host "1. The connection string has been updated with TrustServerCertificate=True" -ForegroundColor White
Write-Host "2. Retry parameters have been added to the connection string" -ForegroundColor White
Write-Host "3. The Container App has been restarted" -ForegroundColor White
Write-Host "`nCheck logs to verify the connection is working:" -ForegroundColor White
Write-Host "az containerapp logs show --name $ContainerAppName --resource-group $ResourceGroup --tail 50" -ForegroundColor Yellow
