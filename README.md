<div align="center">
  <h1>Pendolare</h1>
  <p>A microservices-based platform for ride sharing</p>
  <p>University of Leeds Software Engineering Project - Team 2</p>
</div>

<div align="center">

## Service Status

| Service | Tests Status | Deployment Status |
|:-------:|:------------:|:-----------------:|
| Identity Service | [![Pendo-IdentityService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.IdentityService.yml/badge.svg?branch=main&event=workflow_run)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.IdentityService.yml) | ![Identity Status](https://pendo-status.clsolutions.dev/api/badge/2/status) |
| Booking Service | [![Pendo-BookingService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.BookingService.yml/badge.svg?branch=main&event=workflow_run)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.BookingService.yml) | ![Booking Status](https://pendo-status.clsolutions.dev/api/badge/6/status) |
| Journey Service | [![Pendo-JourneyService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.JourneyService.yml/badge.svg?branch=main&event=workflow_run)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.JourneyService.yml) | ![Journey Status](https://pendo-status.clsolutions.dev/api/badge/7/status) |
| Payment Service | [![Pendo-PaymentService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.PaymentService.yml/badge.svg?branch=main&event=workflow_run)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.PaymentService.yml) | ![Payment Status](https://pendo-status.clsolutions.dev/api/badge/3/status) |
| Message Service | [![Pendo-MessageService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.MessageService.yml/badge.svg?branch=main&event=workflow_run)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.MessageService.yml) | ![Message Status](https://pendo-status.clsolutions.dev/api/badge/4/status) |
| API Gateway | [![Pendo-ApiGateway](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.ApiGateway.yml/badge.svg?branch=main&event=workflow_run)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.ApiGateway.yml) | ![Gateway Status](https://pendo-status.clsolutions.dev/api/badge/1/status) |

</div>

## Overview

Pendolare is a comprehensive journey sharing platform built using a microservices architecture. The platform enables users to create, book, and manage journeys whilst facilitating real-time communication between passengers and drivers. It features a secure authentication system, payment processing integration, and a robust booking management system.

## Architecture

The system consists of six core microservices:

- **[Identity Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.IdentityService)**: Manages user authentication and account management using a passwordless OTP system
- **[Journey Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.JourneyService)**: Handles journey creation, viewing, and management
- **[Booking Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.BookingService)**: Facilitates the booking process, including price negotiation and cancellations
- **[Payment Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.PaymentService)**: Processes transactions securely via Stripe integration
- **[Message Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.MessageService)**: Enables real-time communication via WebSockets
- **[API Gateway](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.ApiGateway)**: Provides a unified entry point to all services using Kong

All services are containerised using Docker and communicate through RESTful APIs orchestrated by the API Gateway.

## Getting Started

For detailed setup instructions and documentation for each service, please visit the corresponding wiki pages linked in the Architecture section above.

## Contributors

- Alexander McCall (@sc23am3) - Payment Service & Client App
- Catherine Weightman (@sc23c2w) - Journey Service  
- James Kinley (@jameskinley) - Identity Service, Booking Service & Client App
- Josh Mundray (@sc232jm) - API Gateway, Message Service & Client App
- Lara Glenn (@lara-glenn) - Admin Service
- Shay O'Donnell (@shayodonnell) - Admin Service, Admin Dashboard

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project was developed as part of the Software Engineering module at the University of Leeds.
