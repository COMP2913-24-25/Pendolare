# Booking Service

The Booking Service is responsible for handling all booking-related operations. It handles the booking, alterations to and cancelling of a chosen journey.

## Overview

Core responsibilities:
 - Create booking
 - Update booking
 - Cancel booking
 - View bookings

## Service Flowchart

```mermaid
flowchart TD
    Start(["Start Booking Request"])
    SelectJourney["Select Journey"]
    ChoosePriceOption{"Book at Advertised Price or Negotiate?"}
    AdvertisedPrice["Book at Advertised Price"]
    HagglePrice["User Negotiates Price"]
    PriceAgreement{"Price Agreed?"}
    PriceDenied["Notify User: Price Not Agreed"]
    ConfirmDetails["Confirm Booking Details"]
    SendToPayment["Send Payment Request to Payment Service"]
    PaymentConfirmed["Receive Payment Confirmation"]
    StoreBooking["Store Booking in Database"]
    UpdateSeats["Update Journey Availability"]
    Notify["Send Confirmation to User & Driver"]
    End(["Booking Complete"])

    UpdateStart(["User Requests to Update Booking"])
    CheckUpdate{"Update Allowed?"}
    UpdateDenied["Notify User: Update Not Allowed"]
    ApplyUpdate["Modify Booking Details"]
    UpdateSeats2["Update Journey Availability"]
    NotifyUpdate["Send Update Confirmation"]

    CancelStart(["User Requests to Cancel Booking"])
    CheckCancel{"Cancellation Allowed?"}
    CancelDenied["Notify User: Cancellation Not Allowed"]
    ProcessRefund["Request Refund from Payment Service"]
    RemoveBooking["Remove Booking from Database"]
    UpdateSeats3["Update Journey Availability"]
    NotifyCancel["Send Cancellation Confirmation"]

    Start --> SelectJourney
    SelectJourney --> ChoosePriceOption
    ChoosePriceOption -->|"Book at Advertised Price"| AdvertisedPrice
    AdvertisedPrice --> ConfirmDetails
    ChoosePriceOption -->|"Negotiate Price"| HagglePrice
    HagglePrice --> PriceAgreement
    PriceAgreement -->|"No"| PriceDenied
    PriceAgreement -->|"Yes"| ConfirmDetails
    ConfirmDetails --> SendToPayment
    SendToPayment --> PaymentConfirmed
    PaymentConfirmed --> StoreBooking
    StoreBooking --> UpdateSeats
    UpdateSeats --> Notify
    Notify --> End

    UpdateStart --> CheckUpdate
    CheckUpdate -->|"No"| UpdateDenied
    CheckUpdate -->|"Yes"| ApplyUpdate
    ApplyUpdate --> UpdateSeats2
    UpdateSeats2 --> NotifyUpdate
    NotifyUpdate --> End

    CancelStart --> CheckCancel
    CheckCancel -->|"No"| CancelDenied
    CheckCancel -->|"Yes"| ProcessRefund
    ProcessRefund --> RemoveBooking
    RemoveBooking --> UpdateSeats3
    UpdateSeats3 --> NotifyCancel
    NotifyCancel --> End
```

### Features
- **Journey Booking:** users can book seats in available journeys.
- **Booking Modification:** Users can negotiate the price with the driver prior to booking
- **Cancellation System:** Allows users to cancel their booking before the journey starts.
- **Payment Integration:** Interfaces with the Payment Service to manage transactions.
- **Notifications:** Sends booking confirmation

## Tech Stack
- Backend: Python (FastAPI)
- Database: SQLAlchemy
- Testing Framework: Pytest

## Prerequisites
- Deployed database

## Getting Started

### Installation
```bash
# Navigate to service directory
cd Pendo.BookingService

# Install dependencies
pip install -r requirements.txt
```

### Configuration
1. Set DB connection values in `appsettings.{environment}.json`
2. Ensure DB configuration is correct (`[shared].[Configuration]` table!)

### Running the Service
```bash
# Development mode
fastapi run --reload  # or equivalent command

# Production mode
fastapi run  # or equivalent command
```

### Testing
```bash
# Run tests
pytest
```

## API Documentation

### Endpoints
Will be automatically populated.

## Monitoring and Logging
- Metrics collection
- Log locations
- Monitoring tools used

## Deployment
- Deployment process
- Required environment variables
- Infrastructure dependencies


## Contact
- User responsible: [Leeds Username]
