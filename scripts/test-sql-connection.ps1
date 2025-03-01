[CmdletBinding()]
param (
    [Parameter(Mandatory = $false)]
    [string]$Server = "pendolare.database.windows.net",

    [Parameter(Mandatory = $false)]
    [string]$Database = "Pendolare.Database",

    [Parameter(Mandatory = $true)]
    [string]$Username,

    [Parameter(Mandatory = $true)]
    [string]$Password,

    [Parameter(Mandatory = $false)]
    [switch]$TrustServerCertificate = $true
)

# Build connection string
$connectionString = "Server=$Server;Database=$Database;User Id=$Username;Password=$Password;"

if ($TrustServerCertificate) {
    $connectionString += "TrustServerCertificate=True;"
}

Write-Host "Testing SQL connection to $Server..." -ForegroundColor Cyan

try {
    # Create SQL connection
    $sqlConnection = New-Object System.Data.SqlClient.SqlConnection
    $sqlConnection.ConnectionString = $connectionString

    Write-Host "Connecting to database..." -ForegroundColor Cyan
    $sqlConnection.Open()

    Write-Host "Connection successful!" -ForegroundColor Green

    # Test a simple query
    $command = $sqlConnection.CreateCommand()
    $command.CommandText = "SELECT @@VERSION AS SqlVersion"
    
    $adapter = New-Object System.Data.SqlClient.SqlDataAdapter($command)
    $dataset = New-Object System.Data.DataSet
    $adapter.Fill($dataset) | Out-Null
    
    $sqlVersion = $dataset.Tables[0].Rows[0]["SqlVersion"]
    
    Write-Host "SQL Server Version:" -ForegroundColor Cyan
    Write-Host $sqlVersion -ForegroundColor White

    # Close the connection
    $sqlConnection.Close()
    
    Write-Host "Connection test succeeded." -ForegroundColor Green
}
catch {
    Write-Host "Connection failed with error:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Verify server name, database name, username and password." -ForegroundColor Yellow
    Write-Host "2. Check if your IP address is allowed in the SQL Server firewall rules." -ForegroundColor Yellow
    Write-Host "3. Check if 'Allow Azure services and resources to access this server' is enabled." -ForegroundColor Yellow
    Write-Host "4. If using Azure AD authentication, ensure you have proper permissions." -ForegroundColor Yellow
    
    exit 1
}
