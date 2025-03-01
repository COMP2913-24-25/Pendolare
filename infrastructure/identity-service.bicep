param location string = resourceGroup().location
param containerAppName string = 'identity-service'
param containerAppEnvironmentName string = 'pendo-env-dev'
param registryName string = 'pendocontainerregistry'
param registryUsername string
@secure()
param registryPassword string
param kongGatewayFqdn string = ''
@secure()
param dbConnectionString string = ''

// Reference existing environment
resource containerAppEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' existing = {
  name: containerAppEnvironmentName
}

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: containerAppName
  location: location
  properties: {
    managedEnvironmentId: containerAppEnvironment.id
    configuration: {
      secrets: [
        {
          name: 'registry-password'
          value: registryPassword
        }
        {
          name: 'db-connection-string'
          value: dbConnectionString
        }
      ]
      registries: [
        {
          server: '${registryName}.azurecr.io'
          username: registryUsername
          passwordSecretRef: 'registry-password'
        }
      ]
      ingress: {
        external: true
        targetPort: 8080
        transport: 'auto'
        allowInsecure: false
        traffic: [
          {
            latestRevision: true
            weight: 100
          }
        ]
      }
      activeRevisionsMode: 'Single'
    }
    template: {
      containers: [
        {
          name: containerAppName
          image: '${registryName}.azurecr.io/${containerAppName}:latest'
          env: [
            {
              name: 'ASPNETCORE_ENVIRONMENT'
              value: 'Production'
            }
            {
              name: 'IdentityConfiguration__ConnectionString'
              secretRef: 'db-connection-string'
            }
            {
              name: 'KONG_GATEWAY_URL'
              value: !empty(kongGatewayFqdn) ? 'https://${kongGatewayFqdn}' : ''
            }
            {
              name: 'SQL_SERVER_NAME'
              value: 'pendolare'
            }
            {
              name: 'SQL_DATABASE_NAME'
              value: 'Pendolare.Database'
            }
            {
              name: 'ENABLE_RETRY_POLICY'  // Enable retry policy for database connections
              value: 'true'
            }
          ]
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
    identity: {
      type: 'SystemAssigned'  // Enable system-assigned managed identity for database access
    }
  }
}

output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
output principalId string = containerApp.identity.principalId  // Output the principal ID for role assignments
