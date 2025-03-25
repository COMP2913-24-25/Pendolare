# Pendo.AdminService

The Pendo Admin Service provides administrative functionalities for the Pendolare system, including managing discounts, retrieving journey analytics, and configuring booking fees.

## Overview

This service handles key administrative tasks such as:
- Managing discount configurations for users.
- Providing analytics for journeys.
- Configuring and updating booking fees.
  
### Features
- Discount management: Create, retrieve, and delete discounts.
- Journey analytics: Retrieve data on available, booked, and cancelled journeys.
- Booking fee configuration: Retrieve and update the booking fee margin.
- Weekly revenue reporting: Generate weekly revenue reports for management.
- Frequent user analytics: Identify users with frequent bookings.

## Tech Stack
- Language/Framework: Python, FastAPI
- Database: MSSQL (Production), SQLite (Testing)
- ORM: SQLAlchemy, Pydantic for configuration
- Testing Framework: Pytest

## Prerequisites
- Python 3.12 or higher
- Docker (for deployment)
- MSSQL Server (for production)
- `requirements.txt` dependencies

## Getting Started

### Installation
```bash
# Switch to service directory
cd Pendo.AdminService

# Create a virtual environment
python.exe -m venv .venv-admin

# Activate the venv
source .venv-admin/Scripts/activate #(or windows equivalent if not using bash)

# Install dependencies (First time setup only)
pip install -r requirements.txt
```

### Configuration
Configuration is managed through appsettings.development.json for development and environment variables for production. Database connection information is retrieved from this JSON file or environment variables.

### Running the Service
```bash
# Debug Mode
fastapi run --reload

# Production
docker run <imgname/>
```

### Testing
```bash
# Run tests
pytest
```

## API Documentation

### Endpoints
- `GET /HealthCheck` - Returns the service's health status.
- `PATCH /UpdateBookingFee` -  Updates the booking fee margin. Requires UpdateBookingFeeRequest in the request body.
- `GET /GetBookingFee` - Retrieves the current booking fee margin.
- `GET /GetWeeklyRevenue` - Retrieves weekly revenue data. Requires GetWeeklyRevenueQuery parameters in the query string (StartDate, EndDate).
- `GET /JourneyAnalytics` - Retrieves analytics on available, booked, and cancelled journeys.
- `GET /FrequentUsers` - Retrieves a list of users with frequent bookings.
- `POST /CreateDiscount` - Creates a new discount. Requires CreateDiscountRequest in the request body (WeeklyJourneys, DiscountPercentage).
- `GET /Discounts` - Retrieves all discounts.
- `DELETE /Discounts/{discount_id}` - Deletes a discount rule by its ID.

## Monitoring and Logging
The service logs critical events and metrics. Container logs can be accessed through

```bash
docker logs Pendo.AdminService
```

## Deployment
Deploy the service using Docker with the provided Dockerfile and shell scripts:

./runDatabase.sh for the database.
./runAdminService.sh for the application.
- Ensure MSSQL Server is running and accessible.

## Contact
- User responsible: Lara Glenn @sc23lfg
