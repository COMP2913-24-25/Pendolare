# Testing Overview

Each service, where possible, has a high degree of unit test coverage. In addition to this, functional, manual tests were carried out iteratively on the system as a whole.

## Contents
- [Unit Tests](#unit-tests)
- [Functional Tests](#functional-tests)

## Unit Tests
**User responsible for section: James Kinley**

This section serves to document all unit tests within the project. This will be updated automatically when unit tests run via GitHub actions.

### Pendo.AdminService

### Pendo.ApiGateway

### Pendo.BookingService

### Pendo.IdentityService

### Pendo.JourneyService

### Pendo.MessageService

### Pendo.PaymentService

## Functional Tests
**User responsible for section: Lara Glenn**

This section serves to document all manual functional tests within the project. The 'actual results' column of the table represents the most recent run through of the tests.

| **Test ID** | **Description** | **Expected Result** | **Actual Result** |
|-------------|------------------|----------------------|-------------------|
| 1.1 | User account creation | User receives OTP email notification that allows account details entry and login | User received OTP email notification. They were able to enter their first and last name and successfully signed in. |
| 1.2 | User account creation (Bad email) | User receives an error message. Message explains the reason for the error. | An error message was displayed. No OTP was sent. |
| 1.3 | User Login | User should receive OTP email and log in with code | User received the OTP email, entered the code, and successfully logged in. |
| 2.1 | Store card details | Card details are securely stored | User entered valid card details, which were securely saved for future top-ups. |
| 2.2 | Use stored card for purchases | Payment is successfully carried out | Stored card was available at checkout. The user completed the transaction successfully. |
| 4.1 | View available one-time journeys | One-time journeys are displayed | Available one-time journeys are displayed. User was able to browse through them. |
| 4.2 | View available commuting journeys | Commuter journeys are displayed | Option to view commuter journeys appeared. When selected, available commuter journeys were displayed. |
| 4.3 | View journey details | Journey details are shown | Journey details including name, driver rating, price, pick-up, and destination were displayed as expected. |
| 5.1 | Search through journeys | Matching journeys are displayed | Journeys matching the search criteria were displayed correctly |
| 5.2 | View journeys in list format | Journeys are displayed in list format | Journeys were presented clearly in list format |
| 6.1 | Select and book a journey | Confirmation message is sent | Confirmation message was emailed and shown in-app |
| 7.1 | Handle payment for booking | Payment is processed successfully | Email was sent confirming successful payment and pending booking |
| 7.2 | Invalid payment attempt | Payment declined with error message | Error shown: insufficient funds and required top-up amount |
| 8.1 | Booking confirmation email | Confirmation email is received | Confirmation email was successfully received. |
| 9.1 | Store booking details | Booking details are accessible | Booking details were available on Upcoming Journeys page |
| 10.1 | Configure journey settings | Settings saved correctly | All settings were saved and visible in ‘My Listings’ |
| 11.1 | Hide booked journey | Journey hidden from listings | Journey was hidden after being booked |
| 12.1 | Save commute for rebooking | Journey is rebooked easily with confirmation email | Recurring commuter journeys were rebooked successfully |
| 13.1 | Cancel booking (15 min before) | Cancellation is free |  |
| 13.2 | Cancel booking (<15 min) | 75% charge applied |  |
| 14.1 | Notify user at pick-up | Passenger is notified |  |
| 15.1 | View pick-up location on map | Map displays location | Map showed pick-up in green, drop-off in red |
| 16.1 | Rate the driver | Rating recorded |  |
| 17.1 | Modify booking before acceptance | Changes applied and visible |  |
| 18.1 | Track past, cancelled, upcoming bookings | Bookings displayed correctly | Upcoming displayed; cancelled not shown |
| 19.1 | View weekly income | Earnings shown | Weekly earnings were correctly displayed on dashboard |
| 20.1 | Graphical income view | Weekly income shown as graph | Weekly income was accurately visualized |
| 21.1 | Configure booking fee | Success message shown | Admin dashboard confirmed fee update |
| 22.1 | View management income | Income (0.5%) shown | Weekly income shown on dashboard graph |
| 23.1 | Manager income graph | Income is visualized | Weekly earnings displayed by week on a graph |
| 24.1 | Temporarily disable commute | Commute disabled, users notified |  |
| 25.1 | Frequent user discount (>4 trips) | Discount automatically applied | Discount correctly applied and shown at checkout |
| 26.1 | Contact management | Management receives message |  |
| 26.2 | Contact other users | Messages are sent and received |  |
