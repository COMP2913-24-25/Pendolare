# Azure Cloud Shell Compatible SQL Database Connection Setup Script
# This script can be pasted directly into Azure Cloud Shell

# Variables - modify these as needed
$ResourceGroup = "dev"
$SqlServerName = "pendolare"
$SqlDatabaseName = "Pendolare.Database" 
$ContainerAppName = "identity-service"
$ContainerAppEnvName = "pendo-env-dev"

# Banner
Write-Host "===== SQL Database Connection Setup for Azure Container Apps =====" -ForegroundColor Cyan
Write-Host "This script will configure SQL Server access for $ContainerAppName" -ForegroundColor Cyan

# Step 1: Check if resources exist
Write-Host "`nChecking if Container App exists..." -ForegroundColor Yellow
$containerApp = az containerapp show --name $ContainerAppName --resource-group $ResourceGroup | ConvertFrom-Json
if (-not $containerApp) {
    Write-Host "Container App $ContainerAppName not found. Cannot continue." -ForegroundColor Red
    return
}
Write-Host "Container App $ContainerAppName found ✓" -ForegroundColor Green

Write-Host "`nChecking if SQL Server exists..." -ForegroundColor Yellow
$sqlServer = az sql server show --name $SqlServerName --resource-group $ResourceGroup | ConvertFrom-Json
if (-not $sqlServer) {
    Write-Host "SQL Server $SqlServerName not found. Cannot continue." -ForegroundColor Red
    return
}
Write-Host "SQL Server $SqlServerName found: $($sqlServer.fullyQualifiedDomainName) ✓" -ForegroundColor Green

Write-Host "`nChecking if SQL Database exists..." -ForegroundColor Yellow
$sqlDb = az sql db show --name $SqlDatabaseName --server $SqlServerName --resource-group $ResourceGroup | ConvertFrom-Json
if (-not $sqlDb) {
    Write-Host "SQL Database $SqlDatabaseName not found. Cannot continue." -ForegroundColor Red
    return
}
Write-Host "SQL Database $SqlDatabaseName found ✓" -ForegroundColor Green

# Step 2: Configure SQL Server Firewall Rules
Write-Host "`nSetting up SQL Server firewall rules..." -ForegroundColor Yellow
Write-Host "Adding 'Allow Azure Services' rule..." -ForegroundColor Cyan
az sql server firewall-rule create --resource-group $ResourceGroup --server $SqlServerName --name "AllowAllWindowsAzureIps" --start-ip-address 0.0.0.0 --end-ip-address 0.0.0.0 | Out-Null

# Step 3: Get Container App Environment outbound IP
Write-Host "`nGetting Container App Environment outbound IP..." -ForegroundColor Yellow
$outboundIp = az containerapp env show --name $ContainerAppEnvName --resource-group $ResourceGroup --query properties.staticIp -o tsv

if ($outboundIp) {
    Write-Host "Container App Environment outbound IP: $outboundIp" -ForegroundColor Green
    Write-Host "Adding outbound IP to SQL firewall rules..." -ForegroundColor Cyan
    az sql server firewall-rule create --resource-group $ResourceGroup --server $SqlServerName --name "ContainerAppOutbound" --start-ip-address $outboundIp --end-ip-address $outboundIp | Out-Null
} else {
    Write-Host "Could not determine Container App Environment outbound IP. Will rely on 'Allow Azure Services' rule." -ForegroundColor Yellow
}

# Step 4: Check Container App Managed Identity
Write-Host "`nChecking Container App managed identity..." -ForegroundColor Yellow
$identity = $containerApp.identity

if ($identity -and $identity.type -eq "SystemAssigned") {
    Write-Host "Container App has system-assigned managed identity ✓" -ForegroundColor Green
    $principalId = $identity.principalId
    Write-Host "Principal ID: $principalId" -ForegroundColor Cyan
} else {
    Write-Host "Container App does not have system-assigned managed identity. Adding it now..." -ForegroundColor Yellow
    
    # Add system-assigned managed identity
    $result = az containerapp identity assign --name $ContainerAppName --resource-group $ResourceGroup --system-assigned | ConvertFrom-Json
    
    if ($result -and $result.identity -and $result.identity.principalId) {
        Write-Host "System-assigned managed identity added successfully ✓" -ForegroundColor Green
        $principalId = $result.identity.principalId
        Write-Host "Principal ID: $principalId" -ForegroundColor Cyan
    } else {
        Write-Host "Failed to add system-assigned managed identity." -ForegroundColor Red
        Write-Host "Will continue with connection string approach only." -ForegroundColor Yellow
    }
}

# Step 5: Generate SQL commands for granting database access
Write-Host "`nGenerating SQL commands for database permissions..." -ForegroundColor Yellow

Write-Host "`n=== SQL SCRIPT TO RUN IN YOUR SQL DATABASE ===" -ForegroundColor Magenta
Write-Host "-- This script grants necessary permissions to the Container App's managed identity" -ForegroundColor White
Write-Host "-- Run this in your $SqlDatabaseName database" -ForegroundColor White
Write-Host "IF NOT EXISTS (SELECT * FROM sys.database_principals WHERE name = N'$ContainerAppName')" -ForegroundColor White
Write-Host "BEGIN" -ForegroundColor White
Write-Host "    CREATE USER [$ContainerAppName] FROM EXTERNAL PROVIDER;" -ForegroundColor White
Write-Host "    PRINT 'User [$ContainerAppName] created from external identity.';" -ForegroundColor White
Write-Host "END" -ForegroundColor White
Write-Host "ELSE" -ForegroundColor White
Write-Host "BEGIN" -ForegroundColor White
Write-Host "    PRINT 'User [$ContainerAppName] already exists.';" -ForegroundColor White
Write-Host "END" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "-- Grant data read permission" -ForegroundColor White
Write-Host "ALTER ROLE db_datareader ADD MEMBER [$ContainerAppName];" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "-- Grant data write permission" -ForegroundColor White
Write-Host "ALTER ROLE db_datawriter ADD MEMBER [$ContainerAppName];" -ForegroundColor White
Write-Host "" -ForegroundColor White
Write-Host "-- Optional: Grant schema modification permission (for EF Core migrations)" -ForegroundColor White
Write-Host "ALTER ROLE db_ddladmin ADD MEMBER [$ContainerAppName];" -ForegroundColor White
Write-Host "=== END OF SQL SCRIPT ===" -ForegroundColor Magenta

# Step 6: Ask if the user wants to update the connection string
Write-Host "`nDo you want to update the connection string in the Container App? (Y/N)" -ForegroundColor Yellow
$updateConnectionString = Read-Host
if ($updateConnectionString -eq "Y" -or $updateConnectionString -eq "y") {
    Write-Host "Please enter the connection string (it won't be displayed as you type):" -ForegroundColor Cyan
    $connectionString = Read-Host -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($connectionString)
    $connectionStringText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    
    if ($connectionStringText) {
        # Create a temporary file with the connection string in the current directory
        $tempFile = "./connection-string-temp.txt"
        [System.IO.File]::WriteAllText($tempFile, $connectionStringText)
        
        Write-Host "Updating Container App with connection string..." -ForegroundColor Cyan
        az containerapp secret set --name $ContainerAppName --resource-group $ResourceGroup --secrets "db-connection-string=$tempFile" | Out-Null
        
        # Remove the temporary file
        Remove-Item -Path $tempFile -Force
        Write-Host "Connection string updated in Container App secrets ✓" -ForegroundColor Green
    }
}

# Step 7: Ask if the user wants to restart the Container App
Write-Host "`nDo you want to restart the Container App to apply changes? (Y/N)" -ForegroundColor Yellow
$restartApp = Read-Host
if ($restartApp -eq "Y" -or $restartApp -eq "y") {
    Write-Host "Restarting Container App to apply changes..." -ForegroundColor Cyan
    az containerapp restart --name $ContainerAppName --resource-group $ResourceGroup | Out-Null
    Write-Host "Container App restarted ✓" -ForegroundColor Green
}

# Step 8: Instructions for next steps
Write-Host "`n===== Next Steps =====" -ForegroundColor Yellow
Write-Host "1. Run the SQL commands shown above in your SQL Database to grant permissions" -ForegroundColor White
Write-Host "   - You can use the Azure Portal SQL Query Editor" -ForegroundColor White
Write-Host "   - Connect to server: $($sqlServer.fullyQualifiedDomainName)" -ForegroundColor White
Write-Host "   - Database: $SqlDatabaseName" -ForegroundColor White

Write-Host "`n2. Verify connectivity by checking Container App logs:" -ForegroundColor White
Write-Host "   az containerapp logs show --name $ContainerAppName --resource-group $ResourceGroup --tail 50" -ForegroundColor Cyan

Write-Host "`n===== Setup Complete =====" -ForegroundColor Green
Write-Host "Allow a few minutes for all changes to propagate." -ForegroundColor Cyan
