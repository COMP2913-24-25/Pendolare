# API Gateway

## Overview

The API Gateway serves as a central entry point for all client requests to backend microservices. It uses Kong, a lightweight cloud-native API gateway. The gateway handles routing, authentication, rate limiting, and provides an additional security layer by decoupling client applications from underlying service implementations.

### Features
- Request routing and load balancing
- Authentication and authorisation
- Rate limiting and throttling
- Request/response transformation
- Declarative configuration using YAML
- Health checks and monitoring

## Tech Stack
- API Gateway: Kong 3.3
- Configuration: YAML-based declarative config
- Containerisation: Docker
- Networking: Custom Kong network

## Prerequisites
- Docker Engine v20.10.0 or higher
- Docker Compose v2.0.0 or higher
- Network ports 8000, 8001, 8002, and 8443 available on host machine
- Kong network created in Docker

## Getting Started

### Installation
```bash
# Clone the repository
git clone https://github.com/COMP2913-24-25/software-engineering-project-team-2.git

# Navigate to service directory
cd Pendo.ApiGateway

# Create Kong network if it doesn't exist
docker network create kong-net

# Create docker container
docker-compose up -d
```

### Configuration
1. The Kong API Gateway uses declarative configuration via the `kong.yml` file located at `kong/declarative/kong.yml`.
2. To modify routes, services, or plugins, update this file and restart the container.
3. Kong Admin API is accessible at http://localhost:8001 and Admin GUI at http://localhost:8002.
4. API Gateway proxies requests through http://localhost:8000 (HTTP) and https://localhost:8443 (HTTPS).

## API Endpoints
The gateway exposes the following base endpoints:
- `http://localhost:8000` - API Gateway HTTP proxy
- `https://localhost:8443` - API Gateway HTTPS proxy
- `http://localhost:8001` - Kong Admin API
- `http://localhost:8002` - Kong Admin GUI

## Monitoring and Logging
- Kong logs are streamed to stdout/stderr and can be viewed using `docker logs kong`
- Health checks are configured to run every 10 seconds
- Kong Admin API provides detailed metrics at `/status` and `/metrics` endpoints
- Integration with Prometheus and Grafana is possible for advanced monitoring

## Deployment
- Environment variables can be modified in docker-compose.yml or through a .env file

## Troubleshooting
- If the container fails to start, check for port conflicts
- Verify the kong-net network exists: `docker network ls`
- Check container logs: `docker logs kong`
- Test Kong is running: `curl http://localhost:8001/status`

## Contact
- User responsible: Josh Mundray (@sc232jm)
