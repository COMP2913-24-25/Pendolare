# Pendolare Client App

Pendolare is a mobile client application allowing for interaction between the user and the various services. This client app is built using React Native and Expo, and leverages modern UI theming and a WebSocket-based messaging service to deliver real-time chat functionality.

## Overview

The Pendolare Client App provides the following core functionalities:
- View available journeys in real time.
- Create and manage their own journeys.
- Book rides on available journeys, enabling efficient shared transportation.
- Real-time chat between users, drivers, and support agents.
- Profile management with dynamic theming.
- Integration with in-house & external services via APIs.

## CURRENT Features

- **Real-time Messaging:** Communicate instantly via WebSocket with message delivery and status indicators.
- **Theming Support:** Automatic dark/light mode support based on user preferences.
- **Profile Management:** View and update your profile information.
- **Support Chat:** Easily contact support when you need help.
- **"Responsive" (WIP) Design:** Built with Tailwind CSS for consistent styling across devices.

## Tech Stack

- **Framework:** React Native with Expo
- **Navigation:** Expo Router
- **State Management:** React hooks and context API
- **Styling:** Tailwind CSS & NativeWind
- **Authentication:** Clerk
- **Real-time Communication:** WebSocket

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Expo CLI
- A supported mobile device or simulator

## Getting Started

### Installation

```bash
# Clone the repository
git clone [repository-url]

# Navigate to the project directory
cd Pendo.ClientApp

# Install dependencies
npm install
```

### Configuration

1. Copy the provided `.env` file or create your own based on `.env.example`.
2. Update environment variables:
   - `EXPO_PUBLIC_PUBLISH_KEY`
   - `EXPO_PUBLIC_OSR_KEY`
   - `CLERK_SECRET_KEY`
   - Additional configuration as required by your environment.

### Running the App

```bash
# For development mode
npm run start

# For tunnel mode (if required)
npm run start-tunnel
```

## Deployment

- Build the app using Expo build or EAS.
- Ensure all environment variables are set in the production environment.
- Monitor application logs and user feedback for iterative improvements.

## Testing

- N/A
  
## Monitoring and Logging

- Application metrics are collected and logged.
- For performance and error tracking, suitable monitoring tools are integrated.