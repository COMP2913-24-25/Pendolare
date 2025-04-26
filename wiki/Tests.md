# Testing Overview

Each service, where possible, has a high degree of unit test coverage. In addition to this, functional, manual tests were carried out iteratively on the system as a whole.

## Contents
- [Unit Tests](#unit-tests)
- [Functional Tests](#functional-tests)

## Unit Tests
**User responsible for section: James Kinley**

This section serves to document all unit tests within the project. This will be updated automatically when unit tests run via GitHub actions.

### Pendo.AdminService
| Test Name | Passing |
|-----------|:------:|
| `test_create_discount` | ✅ |
| `test_get_discounts` | ✅ |
| `test_delete_discount` | ✅ |
| `test_delete_discount_not_found` | ✅ |
| `test_create_discount_exception` | ✅ |
| `test_delete_discount_exception` | ✅ |
| `test_get_booking_fee_success` | ✅ |
| `test_get_booking_fee_exception` | ✅ |
| `test_execute_success` | ✅ |
| `test_execute_same_week` | ✅ |
| `test_execute_exception` | ✅ |
| `test_no_journeys` | ✅ |
| `test_journeys_with_available_only` | ✅ |
| `test_journeys_with_only_cancelled_bookings` | ✅ |
| `test_journeys_with_only_booked_future_bookings` | ✅ |
| `test_journeys_with_only_past_bookings` | ✅ |
| `test_journeys_with_mixed_bookings` | ✅ |
| `test_error_handling` | ✅ |
| `test_update_booking_fee_success` | ✅ |
| `test_update_booking_fee_invalid_fee_margin_too_low` | ✅ |
| `test_update_booking_fee_invalid_fee_margin_too_high` | ✅ |
| `test_update_booking_fee_exception` | ✅ |

### Pendo.ApiGateway
| Test Name | Passing |
|-----------|:------:|

### Pendo.BookingService
| Test Name | Passing |
|-----------|:------:|
| `test_add_booking_ammendment_success` | ✅ |
| `test_add_booking_ammendment_booking_not_found` | ✅ |
| `test_approve_booking_success` | ✅ |
| `test_approve_booking_with_ammendments` | ✅ |
| `test_approve_booking_exception` | ✅ |
| `test_driver_approval` | ✅ |
| `test_passenger_approval` | ✅ |
| `test_full_approval` | ✅ |
| `test_full_approval_cancellation` | ✅ |
| `test_not_authorised` | ✅ |
| `test_booking_ammendment_not_found` | ✅ |
| `test_driver_only_approval` | ✅ |
| `test_passenger_only_approval` | ✅ |
| `test_user_not_found` | ✅ |
| `test_booking_not_found` | ✅ |
| `test_driver_pending_completion_success` | ✅ |
| `test_driver_booking_not_confirmed` | ✅ |
| `test_passenger_completed_success` | ✅ |
| `test_passenger_completed_failure` | ✅ |
| `test_passenger_not_completed` | ✅ |
| `test_unauthorized_user` | ✅ |
| `test_exception_handling` | ✅ |
| `test_get_bookings_for_user_no_ammendment` | ❌ |
| `test_get_bookings_for_user_single_ammendment` | ❌ |
| `test_get_bookings_for_user_multiple_ammendments` | ❌ |
| `test_get_user` | ✅ |
| `test_get_journey` | ✅ |
| `test_get_booking_by_id` | ✅ |
| `test_get_existing_booking` | ✅ |
| `test_create_booking` | ✅ |
| `test_approve_booking` | ✅ |
| `test_update_booking_status` | ✅ |
| `test_add_booking_ammendment` | ✅ |
| `test_get_booking_ammendment` | ✅ |
| `test_calculate_driver_rating_no_bookings` | ✅ |
| `test_calculate_driver_rating_only_pending` | ✅ |
| `test_calculate_driver_rating_only_completed` | ✅ |
| `test_calculate_driver_rating_mixed_bookings` | ✅ |
| `test_calculate_driver_rating_driver_not_found` | ✅ |
| `test_booking_not_found` | ✅ |
| `test_booking_not_confirmed` | ✅ |
| `test_journey_not_found` | ✅ |
| `test_user_not_authorised` | ✅ |
| `test_successful_confirm_at_pickup` | ✅ |
| `test_exception_handling` | ✅ |
| `test_create_booking_success` | ✅ |
| `test_create_booking_user_not_found` | ✅ |
| `test_create_booking_journey_not_found` | ✅ |
| `test_create_booking_already_exists` | ✅ |
| `test_create_booking_fee_margin_not_found` | ✅ |
| `test_create_booking_in_the_past` | ✅ |
| `test_create_booking_commuter_no_recurrence` | ✅ |
| `test_create_booking_get_bookings_for_user` | ✅ |
| `test_check_time_valid` | ✅ |
| `test_check_time_invalid` | ✅ |
| `test_check_time_invalid_cron_expression` | ✅ |
| `test_get_vehicle_details_success` | ✅ |
| `test_get_vehicle_details_no_colour` | ✅ |
| `test_get_vehicle_details_vehicle_not_found` | ✅ |
| `test_get_vehicle_details_api_error` | ✅ |
| `test_get_bookings_success` | ✅ |
| `test_get_bookings_no_bookings` | ✅ |
| `test_get_bookings_none` | ✅ |
| `test_pending_booking_request_success` | ✅ |
| `test_completed_booking_request_success` | ✅ |
| `test_completed_booking_request_error` | ✅ |
| `test_refund_request_success` | ✅ |
| `test_refund_request_insufficient_balance` | ✅ |

### Pendo.IdentityService

### Pendo.JourneyService

### Pendo.MessageService
| Test Name | Passing |
|-----------|:------:|
| `test_create_conversation_handler` | ✅ |
| `test_health_check` | ✅ |
| `test_invalid_participants_in_create_conversation` | ✅ |
| `test_missing_fields_in_create_conversation` | ✅ |
| `test_root_handler` | ✅ |
| `test_user_conversations_handler` | ✅ |
| `test_websocket_connection` | ✅ |
| `test_user_registration` | ✅ |
| `test_chat_message_exchange` | ✅ |
| `test_join_conversation` | ✅ |
| `test_request_message_history` | ✅ |
| `test_health_check` | ✅ |
| `test_root_handler` | ✅ |
| `test_websocket_handler_welcome_message` | ✅ |
| `test_setup_http_server` | ✅ |
| `test_setup_ws_server` | ✅ |
| `test_register_user` | ✅ |
| `test_remove_user` | ✅ |
| `test_handle_chat_message` | ✅ |
| `test_handle_join_conversation` | ✅ |
| `test_handle_history_request` | ❌ |

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
