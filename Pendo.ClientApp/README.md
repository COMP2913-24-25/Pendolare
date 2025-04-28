# Pendolare Client App

Pendolare is a mobile ride-sharing application that connects passengers with drivers for convenient, affordable journeys. This client app is built using React Native and Expo, providing a seamless experience across platforms.

## Overview

The Pendolare Client App provides the following core functionalities:
- User authentication via email OTP
- Browse and book available rides
- Create and advertise your own journeys
- Real-time chat between passengers, drivers, and support
- Secure payments via Stripe integration
- Account management with balance top-up and payouts
- Commuter rides for recurring travel needs
- Ride confirmations and completion tracking
- Dark/light theme customisation

## Features

- **Authentication:** Secure OTP-based email authentication system
- **Journey Management:**
  - Browse available journeys with filtering options
  - Book rides based on location and preferences
  - Advertise your own journeys as a driver
  - Manage commuter (recurring) journeys
  - Track upcoming, past, and canceled journeys
- **Real-time Chat:** Communicate with drivers, passengers, and support via WebSocket
- **Payment System:**
  - Top up account balance via Stripe
  - Request payouts for earnings
  - Manage payment methods
  - Track earnings and revenue
- **Location Services:**
  - Interactive maps for journey visualisation
  - Location search and selection
  - Route calculation between pickup and dropoff points
- **Profile Management:**
  - View and update profile information
  - Track driver ratings
  - Manage personal details
- **Theming:** Support for dark/light mode based on system preferences or user selection

## Tech Stack

- **Framework:** React Native with Expo
- **Language:** TypeScript
- **Navigation:** Expo Router
- **State Management:** React Context API
- **Styling:** Tailwind CSS & NativeWind
- **Payments:** Stripe React Native SDK
- **Location:** Maps integration with geolocation services
- **Real-time Communication:** WebSockets
- **Data Storage:** AsyncStorage and SecureStore
- **API Communication:** Custom API client with JWT authentication

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI
- A supported mobile device or simulator

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/COMP2913/software-engineering-project-team-2.git

# Navigate to the project directory
cd software-engineering-project-team-2/Pendo.ClientApp

# Install dependencies
npm install
```

### Configuration

1. Create an `.env` file based on `.env.example` with the following variables:
   - `EXPO_PUBLIC_STRIPE_PUBLISHABLE_KEY` - Your Stripe publishable key
   - `EXPO_PUBLIC_OSR_KEY` - OpenRouteService API key
   - `EXPO_PUBLIC_DVLA_KEY` - DVLA API key (for UK vehicle registration validation)
   - API base URLs for services

### Running the App

```bash
# Start the development server
npm start

# Run with tunnel for external device testing
npm run start-tunnel
```

## Project Structure

- `/app` - Main application screens and navigation
- `/components` - Reusable UI components
- `/constants` - Application constants and configuration
- `/context` - React Context providers
- `/hooks` - Custom React hooks
- `/services` - API services and external integrations
- `/utils` - Utility functions and helpers

## Key Services

- **Authentication Service:** Handles user login, registration, and session management
- **Booking Service:** Manages ride bookings, confirmations, and completions
- **Journey Service:** Provides journey creation and discovery functionality
- **Message Service:** Real-time chat functionality via WebSockets
- **Payment Service:** Integrates with Stripe for financial transactions
- **Location Service:** Manages location search and route calculations

## Development Notes

- Uses Expo's managed workflow for easier development and deployment
- Implements JWT-based authentication with secure token storage
- Features responsive design for various device sizes
- Supports both light and dark themes via context
