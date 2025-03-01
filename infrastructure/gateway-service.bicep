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
            {
              // Add keepalive interval configuration to reduce overhead
              name: 'KONG_NGINX_HTTP_KEEPALIVE_TIMEOUT'
              value: '300s' // Longer keepalive timeout (5 minutes)
            }
            {
              name: 'KONG_NGINX_WORKER_PROCESSES'
              value: '1'    // Reduce number of worker processes for student plan
            }
            {
              name: 'KONG_NGINX_WORKER_CONNECTIONS'
              value: '512'  // Reduce number of connections
            }
            {
              name: 'KONG_NGINX_PROXY_CONNECT_TIMEOUT'  // Proper timeout format (no ms suffix)
              value: '60'                               // Value in seconds
            }
            {
              name: 'KONG_NGINX_PROXY_SEND_TIMEOUT'     // Proper timeout format (no ms suffix)
              value: '60'                               // Value in seconds
            }
            {
              name: 'KONG_NGINX_PROXY_READ_TIMEOUT'     // Proper timeout format (no ms suffix)
              value: '60'                               // Value in seconds
            }
          ]
          resources: {
            // Reduced resources for student plan
            cpu: json('0.25')  // Reduced from 0.5
            memory: '0.5Gi'    // Reduced from 1.0Gi
          }
          // Extremely infrequent health checks to prevent rate limits
          probes: [
            {
              type: 'Startup'
              httpGet: {
                path: '/'     // Changed from '/status' to '/' which should exist
                port: 8000
              }
              initialDelaySeconds: 30
              failureThreshold: 5
              timeoutSeconds: 5
            }
            {
              type: 'Liveness' 
              httpGet: {
                path: '/'     // Changed from '/status' to '/' which should exist
                port: 8000
              }
              initialDelaySeconds: 60
              periodSeconds: 240     // Changed from 300 to 240 (maximum allowed)
              timeoutSeconds: 10
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
