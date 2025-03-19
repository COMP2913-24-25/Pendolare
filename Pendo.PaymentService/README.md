# PaymentService

The payment service handles transactions and communication with Stripe for any payment operations required by the system.

## Overview

Description of the service's main responsibilities and core functionalities.

### Features
- Provide backend transaction handling for Stripe payments on the front end
- Manage a user's balance, updaing, viewing, etc
- Link transactions to bookings and their status

## Tech Stack
- Language/Framework: Python and FastAPI
- Importantly uses Stripe's Python SDK - to integrate with Stripe's React Native SDK
- Uses Docker containers for all parts
- Testing handled by Pytest

## Prerequisites
- Requirements.txt file
- Docker
- External service dependencies

## Getting Started

### Installation
```bash
# Clone the repository
git clone [repository-url]

# Navigate to service directory
cd [service-name]
```

### Configuration
1. Configure database connection route in ```appsetting.{enviroment}.json```
2. Ensure database post-deploy script has run.

### Running the Service
```bash
# If local DB required:
./runDatabase.sh
# Connect to and publish database + post deploy script

# To run service
./runPaymentService.sh # this runs tests on startup
```

## Monitoring and Logging
- All transactions are logged in the Transaction Table, along with their status
- Stripe takes logs of every customer and every transaction via their API


## Contact
- User responsible: Alexander McCall : sc23am3@leeds.ac.uk