# Pendo.IdentityService

The Identity Service serves to create, update and login users.

## Overview

The Identity Service creates and authenticates users via the `Auth/RequestOtp` and `Auth/VerifyOtp` endpoints. This is a passwordless model, whereby 'one-time-passcodes' are sent to users via email, and then verified. If no account is found with the provided email, one will be created.

Manager accounts are created if, and only if, the given email is contained within the 'Identity.ManagerConfiguration.Whitelist' object (in the configuration table in DB!).

Users can also be updated via this service, restricted to updating First and Last name only.

### Features
- Request OTP (and create account if necessary!).
- Verify OTP (and provide JWT for continued auth).
- Update user details.

## Tech Stack
- C# (ASP.NET 8.0 Web API)
- Entity Framework Core (ORM)
- Docker

## Prerequisites
- Deployed database
- Docker
- .NET 8.0 runtime (running tests only)

## Getting Started

### Installation
```bash
# Clone the repository
git clone [repository-url]

# Navigate to service directory
cd ./Pendo.IdentityService/

# Ensure appsettings.json has relevant connection string

# Build docker image
docker build -f ./Pendo.IdentityService.Api/Dockerfile -t pendo.identityservice.deploy .
```

### Configuration
1. Ensure DB is deployed
2. Ensure connection string in `appsettings.json` is set.

### Running the Service
```bash
# Run container
docker run pendo.identityservice.deploy -p {port}:8080

# Test by pinging
curl http://localhost:{port}/api/Ping #(or navigate to in browser!)
```

### Testing
```bash
# Requires .NET 8.0 runtime + CLI
dotnet test Pendo.IdentityService.sln
```

## API Documentation

### Endpoints
- to be populated from OpenAPI spec

## Monitoring and Logging
- Logs to file + console

## Deployment
- Deploy via docker (push to ACR.)
- Ensure `appsettings.json` (production one) has correct connection string.


## Contact
- User responsible: sc23jk2