param location string = resourceGroup().location
param containerAppName string = 'message-service'
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
        targetPort: 5006
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
          image: '${registryName}.azurecr.io/message-service:latest'
          env: [
            {
              name: 'PYTHONUNBUFFERED'
              value: '1'
            }
            {
              name: 'LOG_LEVEL'
              value: 'INFO'
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
          probes: [
            {
              type: 'liveness'
              httpGet: {
                path: '/health'
                port: 5006
              }
              initialDelaySeconds: 15
              periodSeconds: 30
            }
            {
              type: 'readiness'
              httpGet: {
                path: '/health'
                port: 5006
              }
              initialDelaySeconds: 5
              periodSeconds: 10
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
        rules: [
          {
            name: 'http-rule'
            http: {
              metadata: {
                concurrentRequests: '50'
              }
            }
          }
        ]
      }
    }
  }
}

output containerAppFQDN string = containerApp.properties.configuration.ingress.fqdn
