param location string = resourceGroup().location
param containerAppName string = 'message-service'
param containerAppEnvironmentName string = 'pendo-env-dev'
param registryName string = 'pendocontainerregistry'
param registryUsername string
@secure()
param registryPassword string
param kongGatewayFqdn string = ''

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
      activeRevisionsMode: 'Single' // Only keep one active revision
      secrets: [
        {
          name: 'registry-password'
          value: registryPassword
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
        targetPort: 5006  // Make sure this is correct for WebSockets
        transport: 'auto'  // This ensures WebSocket support
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
              name: 'PYTHONUNBUFFERED'
              value: '1'  // Ensure Python logs are unbuffered
            }
            {
              name: 'KONG_GATEWAY_URL'  
              value: !empty(kongGatewayFqdn) ? 'https://${kongGatewayFqdn}' : ''
            }
            {
              name: 'LOG_LEVEL'          // Reduced logging level
              value: 'WARNING'           // Changed from DEBUG to WARNING
            }
            {
              name: 'WEBSOCKET_PING_INTERVAL' // Reduce WebSocket ping frequency
              value: '60'                     // Ping every 60 seconds instead of more frequently
            }
            {
              name: 'MAX_CONCURRENT_CONNECTIONS' // Limit concurrent connections
              value: '50'
            }
          ]
          resources: {
            cpu: json('0.25')  // Reduced from 0.5
            memory: '0.5Gi'    // Reduced from 1.0Gi
          }
          // Very infrequent health probes
          probes: [
            {
              type: 'Startup'
              httpGet: {
                path: '/health'
                port: 5006
              }
              initialDelaySeconds: 10
              failureThreshold: 3
            }
            {
              type: 'Liveness'
              httpGet: {
                path: '/health'
                port: 5006
              }
              initialDelaySeconds: 60
              periodSeconds: 180     // Check every 3 minutes
              failureThreshold: 3
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1        // No auto-scaling to reduce API calls
      }
    }
  }
}

output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
