# Pendo Message Service

The Pendo Message Service facilitates real-time communication between users and support teams by leveraging WebSockets and robust API integration. It provides persistent chat history, conversation management, and health monitoring.

## Overview
The service is designed for scalable, real-time messaging. It handles:
- Real-time message broadcasting via WebSockets.
- Secure storage and retrieval of conversation history.
- Dynamic conversation management including join and leave operations.

### Features
- Real-time chat with WebSocket-based communication.
- Persistent message history using a database.
- Dynamic conversation creation and management.
- Health and logging endpoints for monitoring.

### Service Flowchart
![Flowchart](https://github.com/user-attachments/assets/1efb103d-632a-4d6b-ba48-9ed30ed76152)

## Tech Stack
- Language/Framework: Python, aiohttp, Websockets
- Database: MSSQL (production), SQLite (testing)
- ORM: SQLAlchemy, Pydantic for configuration

## Prerequisites
- Required software/tools (Python & Docker)
- Environment dependencies (Python packages listed in requirements.txt)
- External service dependencies (MSSQL for production)

## Getting Started

### Installation
```bash
# Clone the repository
git clone [repository-url]

# Navigate to service directory
cd [service-name]

# Install dependencies
pip install -r requirements.txt
```

### Configuration
1. Copy configuration 

### Running the Service
```bash
# Build the project container
docker build -t pendo-message .

# Run the container
docker run --name pendo-message -p PORT:PORT PORT:PORT pendo-message
```

## Testing
```bash
# Build the project container with testing utils
docker build -t pendo-message-test -f Dockerfile.tests .

# Run the testing container
docker run --name pendo-message-test pendo-message-test
```

## Monitoring and Logging
The service logs critical events and metrics. Container logs can be accessed through

```bash
docker logs pendo-message-test
```

## Deployment
Deploy the service using Docker with the provided Dockerfile and shell scripts:
- `Dockerfile` for the application.
  
## Contact
- User responsible: Josh Mundray @sc232jm
