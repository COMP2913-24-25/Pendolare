param location string = resourceGroup().location
param containerAppName string = 'pendo-identity-service'
param containerAppEnvironmentName string = 'pendo-env-dev'
param registryName string = 'pendocontainerregistry'
param registryUsername string
@secure()
param registryPassword string
param kongGatewayFqdn string = ''
@secure()
param dbConnectionString string = ''  // Remove default value for secure parameter

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
            // Use free tier/student plan compatible values
            cpu: json('0.25')  // Reduced from 0.5 to fit student plan
            memory: '0.5Gi'    // Reduced from 1.0Gi to fit student plan
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 2  // Reduced from 3 to better fit student plan limits
      }
    }
  }
}

output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
