param location string = resourceGroup().location
param containerAppName string = 'kong-gateway'
param containerAppEnvironmentName string = 'pendo-env-dev'
param registryName string = 'pendocontainerregistry'
param registryUsername string
@secure()
param registryPassword string

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
      activeRevisionsMode: 'Single' // Only keep one active revision to reduce resource usage
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
        targetPort: 8000
        transport: 'auto'  // Ensures WebSocket support
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
              name: 'KONG_DATABASE'
              value: 'off'
            }
            {
              name: 'KONG_DECLARATIVE_CONFIG'
              value: '/usr/local/kong/declarative/kong.yml'  // Use standard config name
            }
            {
              name: 'KONG_PROXY_ACCESS_LOG'
              value: '/dev/stdout'
            }
            {
              name: 'KONG_ADMIN_ACCESS_LOG'
              value: '/dev/stdout'
            }
            {
              name: 'KONG_PROXY_ERROR_LOG'
              value: '/dev/stderr'
            }
            {
              name: 'KONG_ADMIN_ERROR_LOG'
              value: '/dev/stderr'
            }
            {
              name: 'KONG_ADMIN_LISTEN'
              value: '0.0.0.0:8001'
            }
            {
              name: 'KONG_PROXY_LISTEN'
              value: '0.0.0.0:8000'  // Simplified listen directive
            }
            {
              name: 'KONG_LOG_LEVEL'       // Less verbose logging to reduce API calls
              value: 'error'               // Changed from info/debug to error
            }
            {
              name: 'KONG_PLUGINS'
              value: 'bundled,cors'  // Minimal plugins
            }
          ]
          resources: {
            // Reduced resources for student plan
            cpu: json('0.5')  // Reduced from 0.5
            memory: '1.0Gi'    // Reduced from 1.0Gi
          }
          // Update health check probes to use Kong's health endpoint
          probes: [
            {
              type: 'Startup'
              httpGet: {
                path: '/status'   // Use Kong's status endpoint instead of root
                port: 8001        // Admin API port for status check
              }
              initialDelaySeconds: 60  // Increased delay to allow Kong time to initialize
              failureThreshold: 10     // More retries before failure
              timeoutSeconds: 10       // More time for the request to complete
            }
            {
              type: 'Liveness' 
              httpGet: {
                path: '/status'   // Use Kong's status endpoint instead of root
                port: 8001        // Admin API port for status check
              }
              initialDelaySeconds: 90
              periodSeconds: 240     
              timeoutSeconds: 20
              failureThreshold: 5
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1  // Limit to 1 replica
      }
    }
  }
}

output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
