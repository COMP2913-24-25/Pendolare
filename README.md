<div align="center">
  <h1>Pendolare</h1>
  <p>A microservices-based platform for ride sharing</p>
  <p>University of Leeds Software Engineering Project - Team 2</p>
</div>

<div align="center">

## Service Status

| Service | Tests Status | Deployment Status |
|:-------:|:------------:|:-----------------:|
| Identity Service | [![Pendo-IdentityService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.IdentityService.yml/badge.svg)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.IdentityService.yml) | ![Identity Status](https://pendo-status.clsolutions.dev/api/badge/2/status) |
| Booking Service | [![Pendo-BookingService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.BookingService.yml/badge.svg)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.BookingService.yml) | ![Booking Status](https://pendo-status.clsolutions.dev/api/badge/6/status) |
| Journey Service | [![Pendo-JourneyService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.JourneyService.yml/badge.svg)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.JourneyService.yml) | ![Journey Status](https://pendo-status.clsolutions.dev/api/badge/7/status) |
| Payment Service | [![Pendo-PaymentService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.PaymentService.yml/badge.svg)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.PaymentService.yml) | ![Payment Status](https://pendo-status.clsolutions.dev/api/badge/3/status) |
| Message Service | [![Pendo-MessageService](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.MessageService.yml/badge.svg)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.MessageService.yml) | ![Message Status](https://pendo-status.clsolutions.dev/api/badge/4/status) |
| API Gateway | [![Pendo-ApiGateway](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.ApiGateway.yml/badge.svg)](https://github.com/COMP2913-24-25/software-engineering-project-team-2/actions/workflows/Pendo.ApiGateway.yml) | ![Gateway Status](https://pendo-status.clsolutions.dev/api/badge/1/status) |

</div>

## Table of Contents
- [Overview](#overview)
- [User Features](#user-features)
- [Management Features](#management-features)
- [Architecture](#architecture)
- [Project Backlog](#project-backlog)
- [Getting Started](#getting-started)
- [Contributors](#contributors)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview

Pendolare is a comprehensive journey sharing platform built using a microservices architecture. The platform enables users to create, book, and manage journeys whilst facilitating real-time communication between passengers and drivers. It features a secure authentication system, payment processing integration, and a robust booking management system.

## User Features
- Account creation: Users can create and manage their accounts
- Journey searching: Users can search for available car-share journeys based on location, date and other specifications
- Booking journeys: Users can book available journeys, negotiate times, pick-up locations and costs with the driver
- Payment handling: Users can make payments for booked journeys (simulated for the project)
- Journey ratings: Users can rate the journey and driver after the journey has been completed
- Journey history: Users can view past and upcoming journeys

## Management Features
- Journey data overview: Managers can view journey details, including booked, cancelled, and available journeys
- Revenue tracking: Managers can track weekly and overall income from bookings
- Fee configuration: Managers can modify the booking fee
- Discount creation: Managers can create, view and delete discounts for users
- User support: Managers can provide customer support for users facing issues with their bookings using the in-app messaging service 

## Architecture

The system consists of six core microservices:

- **[Identity Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.IdentityService)**: Manages user authentication and account management using a passwordless OTP system
- **[Journey Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.JourneyService)**: Handles journey creation, viewing, and management
- **[Booking Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.BookingService)**: Facilitates the booking process, including price negotiation and cancellations
- **[Payment Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.PaymentService)**: Processes transactions securely via Stripe integration
- **[Message Service](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.MessageService)**: Enables real-time communication via WebSockets
- **[API Gateway](https://github.com/COMP2913-24-25/software-engineering-project-team-2/wiki/Pendo.ApiGateway)**: Provides a unified entry point to all services using Kong

All services are containerised using Docker and communicate through RESTful APIs orchestrated by the API Gateway.

## Project Backlog 
The following backlog outlines all features and requirements for the Pendolare project. All items have been successfully implemented and completed.
| **ID** | **Description** | **Type** | **Priority** | **Status** |
|--------|---------------|----------|-------------|------------|
| **1** | Support user accounts and user login | Functional | High (1) | ✅ Completed |
| **2** | Option to store customer's card details for quicker bookings | Functional | Low (2) | ✅ Completed |
| **3** | If ID 2: Ensure good security for stored user accounts | Non-Functional | Low (2) | ✅ Completed |
| **4** | View available journeys (commuting & one-time) with details | Functional | High (1) | ✅ Completed |
| **5** | Display journeys visually (calendar view) and allow search | Functional | Low (2) | ✅ Completed |
| **6** | Select and book a journey | Functional | High (1) | ✅ Completed |
| **7** | Handle card payments for booking (simulated) | Functional | High (1) | ✅ Completed |
| **8** | Send booking confirmation via email | Functional | Low (2) | ✅ Completed |
| **9** | Store booking confirmation and display on demand | Functional | High (1) | ✅ Completed |
| **10** | Allow users to set journey details (cost, time, location, etc.) | Functional | Low (2) | ✅ Completed |
| **11** | Change journey status to hidden once booked | Functional | Low (2) | ✅ Completed |
| **12** | Enable rebooking for recurring commutes | Functional | Low (2) | ✅ Completed |
| **13** | Cancellation rules (free before 15 min, 75% charge after) | Functional | High (1) | ✅ Completed |
| **14** | Alert users when others have arrived at pickup location | Functional | Low (2) | ✅ Completed |
| **15** | Display map of the start point for a booking | Functional | Low (2) | ✅ Completed |
| **16** | Allow users to rate journeys after completion | Functional | Low (2) | ✅ Completed |
| **17** | Enable users to adjust booking details before confirmation | Functional | High (1) | ✅ Completed |
| **18** | Track active and past bookings | Functional | Low (2) | ✅ Completed |
| **19** | Allow users to view their weekly income (99.5% of earnings) | Functional | Low (2) | ✅ Completed |
| **20** | Plot earnings graphically | Functional | Low (2) | ✅ Completed |
| **21** | Allow management to configure booking fees | Functional | Low (2) | ✅ Completed |
| **22** | Allow management to view weekly income (0.5% fee) | Functional | High (1) | ✅ Completed |
| **23** | Plot management earnings graphically | Functional | Low (2) | ✅ Completed |
| **24** | Enable temporary deactivation of journeys (illness/holiday) | Functional | Low (2) | ❎ Not Completed |
| **25** | Provide discounts for frequent users (>4 trips per week) | Functional | Low (2) | ✅ Completed |
| **26** | Allow communication between users and management | Functional | Low (2) | ✅ Completed |
| **27** | Support simultaneous multi-client usage | Functional | Low (2) | ✅ Completed |
| **28** | Ensure responsive user interface | Non-Functional | Low (2) | ✅ Completed |
| **29** | Improve accessibility (color contrast, fonts, etc.) | Non-Functional | Low (2) | ✅ Completed |

## Getting Started

For detailed setup instructions and documentation for each service, please visit the corresponding wiki pages linked in the Architecture section above.

## Contributors

- Alexander McCall (@sc23am3) - Payment Service & Client App
- Catherine Weightman (@sc23c2w) - Journey Service & Payment Service
- James Kinley (@jameskinley) - Identity Service, Booking Service & Client App
- Josh Mundray (@sc232jm) - API Gateway, Message Service & Client App
- Lara Glenn (@lara-glenn) - Admin Service
- Shay O'Donnell (@shayodonnell) - Admin Service, Admin Dashboard

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project was developed as part of the Software Engineering module at the University of Leeds.
