param location string = resourceGroup().location
param containerAppName string = 'pendo-identity-service'
param containerAppEnvironmentName string = 'pendo-env-dev'
param registryName string = 'pendocontainerregistry'
param registryUsername string
@secure()
param registryPassword string
param kongGatewayFqdn string = ''

// Add a parameter for the database connection string
@secure()
param dbConnectionString string = 'Server=172.17.0.2,1433;Database=Pendo.Database;User Id=sa;Password=YourPassword123;Trust Server Certificate=True;'

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
          ]
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
}

output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
