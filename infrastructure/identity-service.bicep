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
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    managedEnvironmentId: containerAppEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single' // Only keep one active revision to reduce resource usage
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
            {
              name: 'SQL_SERVER_NAME'
              value: 'pendolare'
            }
            {
              name: 'SQL_DATABASE_NAME'
              value: 'Pendolare.Database'
            }
            {
              name: 'ENABLE_RETRY_POLICY'
              value: 'true'
            }
            {
              name: 'ENABLE_CONNECTION_POOLING'  // Enable connection pooling to reduce DB connections
              value: 'true'
            }
            {
              name: 'CONNECTION_POOL_SIZE'       // Limit connection pool size
              value: '5'
            }
            {
              name: 'Logging__LogLevel__Default' // Reduce logging in production
              value: 'Warning'
            }
            {
              name: 'Logging__LogLevel__Microsoft' 
              value: 'Warning'
            }
          ]
          resources: {
            cpu: json('0.25')  // Reduced from 0.5
            memory: '0.5Gi'    // Reduced from 1.0Gi
          }
          // Very infrequent health probes to reduce API calls
          probes: [
            {
              type: 'Startup'
              httpGet: {
                path: '/api/ping'
                port: 8080
              }
              initialDelaySeconds: 10
              failureThreshold: 3
              timeoutSeconds: 5
              periodSeconds: 20
            }
            {
              type: 'Liveness'
              httpGet: {
                path: '/api/ping'
                port: 8080
              }
              initialDelaySeconds: 60
              periodSeconds: 180     // Only check every 3 minutes
              timeoutSeconds: 5
              failureThreshold: 3
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1  // Prevent auto-scaling that causes more API calls
      }
    }
  }
}

output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
output principalId string = containerApp.identity.principalId
