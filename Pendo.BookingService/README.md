# Booking Service

The Booking Service is responsible for handling all booking-related operations. It handles the booking, alterations to and cancelling of a chosen journey.

## Overview

Core responsibilities:
 - Create booking
 - Update booking
 - Communicate with payment service

## Service Flowchart

```mermaid
flowchart TD
    Start(["Start Booking Request"])
    SelectJourney["Select Journey"]
    ChoosePriceOption{"Book at\nAdvertised Price\nor Negotiate?"}
    AdvertisedPrice["Book at Advertised Price"]
    HagglePrice["User Negotiates Price"]
    PriceAgreement{"Price Agreed?"}
    PriceDenied["Notify User:\nPrice Not Agreed"]
    ConfirmDetails["Confirm Booking Details"]
    SendToPayment["Send Payment Request"]
    PaymentConfirmed["Receive Payment\nConfirmation"]
    StoreBooking["Store Booking\nin Database"]
    UpdateSeats["Update Journey\nAvailability"]
    Notify["Send Confirmation to\nUser & Driver"]
    End(["Booking Complete"])

    UpdateStart(["Update Booking Request"])
    CheckUpdate{"Update Allowed?"}
    UpdateDenied["Notify User:\nUpdate Not Allowed"]
    ApplyUpdate["Modify Booking Details"]
    UpdateSeats2["Update Journey\nAvailability"]
    NotifyUpdate["Send Update\nConfirmation"]

    CancelStart(["Cancel Booking Request"])
    CheckCancel{"Cancellation\nAllowed?"}
    CancelDenied["Notify User:\nCancellation Not Allowed"]
    ProcessRefund["Request Refund"]
    RemoveBooking["Remove Booking\nfrom Database"]
    UpdateSeats3["Update Journey\nAvailability"]
    NotifyCancel["Send Cancellation\nConfirmation"]

    Start --> SelectJourney
    SelectJourney --> ChoosePriceOption
    ChoosePriceOption -->|"Advertised"| AdvertisedPrice
    AdvertisedPrice --> ConfirmDetails
    ChoosePriceOption -->|"Negotiate"| HagglePrice
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
- Backend: Python (Flask)
- Database: PostgreSQL
- Testing Framework: Pytest

## Prerequisites
- to be updated

## Getting Started

### Installation
```bash
# Clone the repository
git clone [repository-url]

# Navigate to service directory
cd [service-name]

# Install dependencies
npm install  # or equivalent command
```

### Configuration
1. Copy `.env.example` to `.env`
2. Update environment variables:
   - `DATABASE_URL`
   - `SERVICE_PORT`
   - `OTHER_REQUIRED_VARS`

### Running the Service
```bash
# Development mode
npm run dev  # or equivalent command

# Production mode
npm run start  # or equivalent command
```

### Testing
```bash
# Run unit tests
npm run test  # or equivalent command

# Run integration tests
npm run test:integration  # or equivalent command
```

## API Documentation

### Endpoints
- `GET /api/v1/resource` - Description
- `POST /api/v1/resource` - Description
- `PUT /api/v1/resource/:id` - Description
- `DELETE /api/v1/resource/:id` - Description

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
