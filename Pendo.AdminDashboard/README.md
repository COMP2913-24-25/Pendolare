# Admin Dashboard

The Admin Dashboard is a web interface for managers to configure booking fees, view revenue analytics, manage discount offers, and respond to support requests in real time.

## Overview

The Admin Dashboard provides the following core functionalities:
- Secure admin authentication and session management.
- Real-time booking fee configuration and analytics.
- Management of discount offers.
- Integrated support chat for quick response to user issues.
- Session monitoring with automatic logout on inactivity.

## Features

- **Booking Fee Management:** Update and view booking fees instantly.
- **Revenue Analytics:** Display revenue for the past 7 days and weekly trends for the past 5 weeks.
- **Discount Control:** Create, update, and delete promotional discounts.
- **Support Chat:** Real-time messaging for handling support requests.
- **Session Timeout:** Automatic logout after inactivity for enhanced security.

## Tech Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Real-time Communication:** WebSocket for chat functionality
- **Testing:** Pytest

## Prerequisites

- Python 3.x
- Active database connection
- Properly configured `appsettings.{environment}.json`
- Required environment variables set appropriately

## Getting Started

### Installation

```bash
# Navigate to the admin dashboard directory
cd /Pendo.AdminDashboard

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Copy the configuration template or adjust the existing `appsettings.{environment}.json` file.
2. Verify that the `[shared].[Configuration]` table in your database is up-to-date.
3. Update any environment-specific variables as needed.

### Running the App

```bash
# For development mode
flask run --debug

# For production mode
flask run
```

## Deployment

- Deploy using a production-ready WSGI server such as Gunicorn.
- Ensure all environment variables and configuration files are set correctly.
- Follow best practices for deploying Flask applications.

## Testing

- Run tests using Pytest: `pytest`

## Monitoring and Logging

- Integrated logging for real-time error and activity tracking.
- Performance metrics and system logs are collected for monitoring.