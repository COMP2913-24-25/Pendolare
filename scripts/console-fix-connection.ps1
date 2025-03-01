# One-liner to set these parameters in the console
$ResourceGroup = "dev"; $ContainerAppName = "identity-service"; $ConnectionString = "Server=tcp:pendolare.database.windows.net,1433;Initial Catalog=Pendolare.Database;Persist Security Info=False;User ID=comp2913;Password=Securepassword123;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=True;Connection Timeout=30;ConnectRetryCount=5;ConnectRetryInterval=10;"

Write-Host "===== Identity Service Connection String Quick Fix =====" -ForegroundColor Cyan
Write-Host "Fixing connection string for $ContainerAppName in resource group $ResourceGroup" -ForegroundColor Yellow

# Display modified connection string with password hidden
$displayString = $ConnectionString -replace "Password=[^;]*", "Password=*****"
Write-Host "Setting connection string (password hidden):" -ForegroundColor Green
Write-Host $displayString -ForegroundColor White

# Create a temporary file in memory
$tempFilePath = [System.IO.Path]::GetTempFileName()
Set-Content -Path $tempFilePath -Value $ConnectionString -NoNewline

try {
    # Set the secret in the container app
    Write-Host "`nUpdating Container App with new connection string..." -ForegroundColor Cyan
    az containerapp secret set --name $ContainerAppName --resource-group $ResourceGroup --secrets "db-connection-string=$tempFilePath"

    # Get current image to restart the app
    Write-Host "`nRestarting Container App to apply changes..." -ForegroundColor Cyan
    $image = az containerapp show --name $ContainerAppName --resource-group $ResourceGroup --query "properties.template.containers[0].image" -o tsv
    az containerapp update --name $ContainerAppName --resource-group $ResourceGroup --image $image

    Write-Host "`nWaiting 10 seconds for app to restart..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10

    Write-Host "`nConnection string updated and app restarted!" -ForegroundColor Green
    Write-Host "Check logs with: az containerapp logs show --name $ContainerAppName --resource-group $ResourceGroup --tail 20" -ForegroundColor White
}
finally {
    # Clean up temp file
    if (Test-Path $tempFilePath) {
        Remove-Item -Path $tempFilePath -Force
    }
}
