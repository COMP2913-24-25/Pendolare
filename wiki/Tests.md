# Testing Overview

Each service, where possible, has a high degree of unit test coverage. In addition to this, functional, manual tests were carried out iteratively on the system as a whole.

## Contents
- [Unit Tests](#unit-tests)
  - [Pendo.ApiGateway](#pendoapigateway)
  - [Pendo.BookingService](#pendobookingservice)
  - [Pendo.IdentityService](#pendoidentityservice)
  - [Pendo.JourneyService](#pendojourneyservice)
  - [Pendo.MessageService](#pendomessageservice)
  - [Pendo.PaymentService](#pendopaymentservice)
- [Functional Tests](#functional-tests)

## Unit Tests
**User responsible for section: James Kinley**

This section serves to document all unit tests within the project. This will be updated automatically when unit tests run via GitHub actions.

### Pendo.AdminService
| Location | Test Name | Passing |
|----------|-----------|:------:|
| `test_discounts` | `test_create_discount` | ✅ |
| `test_discounts` | `test_create_discount_exception` | ✅ |
| `test_discounts` | `test_delete_discount` | ✅ |
| `test_discounts` | `test_delete_discount_exception` | ✅ |
| `test_discounts` | `test_delete_discount_not_found` | ✅ |
| `test_discounts` | `test_get_discounts` | ✅ |
| `test_get_booking_fee` | `test_get_booking_fee_exception` | ✅ |
| `test_get_booking_fee` | `test_get_booking_fee_success` | ✅ |
| `test_get_weekly_revenue` | `test_execute_exception` | ✅ |
| `test_get_weekly_revenue` | `test_execute_same_week` | ✅ |
| `test_get_weekly_revenue` | `test_execute_success` | ✅ |
| `test_journey_analytics` | `test_error_handling` | ✅ |
| `test_journey_analytics` | `test_journeys_with_available_only` | ✅ |
| `test_journey_analytics` | `test_journeys_with_mixed_bookings` | ✅ |
| `test_journey_analytics` | `test_journeys_with_only_booked_future_bookings` | ✅ |
| `test_journey_analytics` | `test_journeys_with_only_cancelled_bookings` | ✅ |
| `test_journey_analytics` | `test_journeys_with_only_past_bookings` | ✅ |
| `test_journey_analytics` | `test_no_journeys` | ✅ |
| `test_update_booking_fee` | `test_update_booking_fee_exception` | ✅ |
| `test_update_booking_fee` | `test_update_booking_fee_invalid_fee_margin_too_high` | ✅ |
| `test_update_booking_fee` | `test_update_booking_fee_invalid_fee_margin_too_low` | ✅ |
| `test_update_booking_fee` | `test_update_booking_fee_success` | ✅ |

### Pendo.ApiGateway
| Location | Test Name | Passing |
|----------|-----------|:------:|
| `jwt-custom-claims` | `test_mock_run` | ✅ |

### Pendo.BookingService
| Location | Test Name | Passing |
|----------|-----------|:------:|
| `test_add_booking_ammendment` | `test_add_booking_ammendment_booking_not_found` | ✅ |
| `test_add_booking_ammendment` | `test_add_booking_ammendment_success` | ✅ |
| `test_approve_booking` | `test_approve_booking_exception` | ✅ |
| `test_approve_booking` | `test_approve_booking_success` | ✅ |
| `test_approve_booking` | `test_approve_booking_with_ammendments` | ✅ |
| `test_approve_booking_ammendment` | `test_booking_ammendment_not_found` | ✅ |
| `test_approve_booking_ammendment` | `test_driver_approval` | ✅ |
| `test_approve_booking_ammendment` | `test_driver_only_approval` | ✅ |
| `test_approve_booking_ammendment` | `test_full_approval` | ✅ |
| `test_approve_booking_ammendment` | `test_full_approval_cancellation` | ✅ |
| `test_approve_booking_ammendment` | `test_not_authorised` | ✅ |
| `test_approve_booking_ammendment` | `test_passenger_approval` | ✅ |
| `test_approve_booking_ammendment` | `test_passenger_only_approval` | ✅ |
| `test_booking_complete` | `test_booking_not_found` | ✅ |
| `test_booking_complete` | `test_driver_booking_not_confirmed` | ✅ |
| `test_booking_complete` | `test_driver_pending_completion_success` | ✅ |
| `test_booking_complete` | `test_exception_handling` | ✅ |
| `test_booking_complete` | `test_passenger_completed_failure` | ✅ |
| `test_booking_complete` | `test_passenger_completed_success` | ✅ |
| `test_booking_complete` | `test_passenger_not_completed` | ✅ |
| `test_booking_complete` | `test_unauthorized_user` | ✅ |
| `test_booking_complete` | `test_user_not_found` | ✅ |
| `test_booking_repository` | `test_add_booking_ammendment` | ✅ |
| `test_booking_repository` | `test_approve_booking` | ✅ |
| `test_booking_repository` | `test_calculate_driver_rating_driver_not_found` | ✅ |
| `test_booking_repository` | `test_calculate_driver_rating_mixed_bookings` | ✅ |
| `test_booking_repository` | `test_calculate_driver_rating_no_bookings` | ✅ |
| `test_booking_repository` | `test_calculate_driver_rating_only_completed` | ✅ |
| `test_booking_repository` | `test_calculate_driver_rating_only_pending` | ✅ |
| `test_booking_repository` | `test_create_booking` | ✅ |
| `test_booking_repository` | `test_get_booking_ammendment` | ✅ |
| `test_booking_repository` | `test_get_booking_by_id` | ✅ |
| `test_booking_repository` | `test_get_bookings_for_user_multiple_ammendments` | ✅ |
| `test_booking_repository` | `test_get_bookings_for_user_no_ammendment` | ✅ |
| `test_booking_repository` | `test_get_bookings_for_user_single_ammendment` | ✅ |
| `test_booking_repository` | `test_get_existing_booking` | ✅ |
| `test_booking_repository` | `test_get_journey` | ✅ |
| `test_booking_repository` | `test_get_user` | ✅ |
| `test_booking_repository` | `test_update_booking_status` | ✅ |
| `test_confirm_at_pickup` | `test_booking_not_confirmed` | ✅ |
| `test_confirm_at_pickup` | `test_booking_not_found` | ✅ |
| `test_confirm_at_pickup` | `test_exception_handling` | ✅ |
| `test_confirm_at_pickup` | `test_journey_not_found` | ✅ |
| `test_confirm_at_pickup` | `test_successful_confirm_at_pickup` | ✅ |
| `test_confirm_at_pickup` | `test_user_not_authorised` | ✅ |
| `test_create_booking` | `test_create_booking_already_exists` | ✅ |
| `test_create_booking` | `test_create_booking_commuter_no_recurrence` | ✅ |
| `test_create_booking` | `test_create_booking_fee_margin_not_found` | ✅ |
| `test_create_booking` | `test_create_booking_get_bookings_for_user` | ✅ |
| `test_create_booking` | `test_create_booking_in_the_past` | ✅ |
| `test_create_booking` | `test_create_booking_journey_not_found` | ✅ |
| `test_create_booking` | `test_create_booking_success` | ✅ |
| `test_create_booking` | `test_create_booking_user_not_found` | ✅ |
| `test_cron_checker` | `test_check_time_invalid` | ✅ |
| `test_cron_checker` | `test_check_time_invalid_cron_expression` | ✅ |
| `test_cron_checker` | `test_check_time_valid` | ✅ |
| `test_dvla_api` | `test_get_vehicle_details_api_error` | ✅ |
| `test_dvla_api` | `test_get_vehicle_details_no_colour` | ✅ |
| `test_dvla_api` | `test_get_vehicle_details_success` | ✅ |
| `test_dvla_api` | `test_get_vehicle_details_vehicle_not_found` | ✅ |
| `test_get_bookings` | `test_get_bookings_no_bookings` | ✅ |
| `test_get_bookings` | `test_get_bookings_none` | ✅ |
| `test_get_bookings` | `test_get_bookings_success` | ✅ |
| `test_payment_service_api` | `test_completed_booking_request_error` | ✅ |
| `test_payment_service_api` | `test_completed_booking_request_success` | ✅ |
| `test_payment_service_api` | `test_pending_booking_request_success` | ✅ |
| `test_payment_service_api` | `test_refund_request_insufficient_balance` | ✅ |
| `test_payment_service_api` | `test_refund_request_success` | ✅ |

### Pendo.IdentityService
| Location | Test Name | Passing |
|----------|-----------|:------:|
| `Identity.Tests.Commands.GetUserRequestHandlerTests` | `Handle_UserFound_NullNames_DefaultsToEmptyString` | ✅ |
| `Identity.Tests.Commands.GetUserRequestHandlerTests` | `Handle_UserFound_ReturnsUserDetailsSuccessfully` | ✅ |
| `Identity.Tests.Commands.GetUserRequestHandlerTests` | `Handle_UserNotFound_ReturnsFailureResponse` | ✅ |
| `Identity.Tests.Commands.OtpRequestHandlerTests` | `Handle_CreatesNewUserAndSendsOtpSuccessfully("manager@test.com",2)` | ✅ |
| `Identity.Tests.Commands.OtpRequestHandlerTests` | `Handle_CreatesNewUserAndSendsOtpSuccessfully("mundrayj@gmail.com",1)` | ✅ |
| `Identity.Tests.Commands.OtpRequestHandlerTests` | `Handle_WhenEmailFails_ReturnsFalse` | ✅ |
| `Identity.Tests.Commands.OtpRequestHandlerTests` | `Handle_WhenUserExists_UsesExistingUser` | ✅ |
| `Identity.Tests.Commands.UpdateUserRequestHandlerTests` | `Handle_UserFound_UpdateOnlyNonEmptyValues` | ✅ |
| `Identity.Tests.Commands.UpdateUserRequestHandlerTests` | `Handle_UserFound_UpdatesFirstAndLastNameSuccessfully` | ✅ |
| `Identity.Tests.Commands.UpdateUserRequestHandlerTests` | `Handle_UserNotFound_ReturnsFailureResponse` | ✅ |
| `Identity.Tests.Commands.VerifyOtpRequestHandlerTests` | `Handle_WhenMultipleUsersExist_ReturnsFalse` | ✅ |
| `Identity.Tests.Commands.VerifyOtpRequestHandlerTests` | `Handle_WhenOtpExpired_ReturnsFalse` | ✅ |
| `Identity.Tests.Commands.VerifyOtpRequestHandlerTests` | `Handle_WhenOtpInvalid_ReturnsFalse` | ✅ |
| `Identity.Tests.Commands.VerifyOtpRequestHandlerTests` | `Handle_WhenOtpLoginNotFound_ReturnsFalse` | ✅ |
| `Identity.Tests.Commands.VerifyOtpRequestHandlerTests` | `Handle_WhenOtpValid_ReturnsTrueAndJwt` | ✅ |
| `Identity.Tests.Commands.VerifyOtpRequestHandlerTests` | `Handle_WhenUserDoesNotExist_ReturnsFalse` | ✅ |
| `Identity.Tests.DataAccess.RepositoryFactoryTests` | `Create_ReturnsModelOfCorrectType` | ✅ |
| `Identity.Tests.DataAccess.RepositoryTests` | `Create_AddsNewEntity` | ✅ |
| `Identity.Tests.DataAccess.RepositoryTests` | `Delete_RemovesExistingEntity` | ✅ |
| `Identity.Tests.DataAccess.RepositoryTests` | `Read_Should_Return_Filtered_Entities` | ✅ |
| `Identity.Tests.DataAccess.RepositoryTests` | `Read_WithNullFilter_ReturnsAllEntities` | ✅ |
| `Identity.Tests.DataAccess.RepositoryTests` | `Update_ModifiesExistingEntity` | ✅ |
| `Identity.Tests.Util.DateTimeProviderTests` | `UtcNow_ReturnsTime` | ✅ |
| `Identity.Tests.Util.JwtGeneratorTests` | `GenerateJwt_ShouldContainCorrectClaims` | ✅ |
| `Identity.Tests.Util.JwtGeneratorTests` | `GenerateJwt_ShouldReturnValidToken` | ✅ |
| `Identity.Tests.Util.NumericOtpGeneratorTests` | `GenerateToken_OfSetLength_ReturnsNumericCode(1)` | ✅ |
| `Identity.Tests.Util.NumericOtpGeneratorTests` | `GenerateToken_OfSetLength_ReturnsNumericCode(100)` | ✅ |
| `Identity.Tests.Util.NumericOtpGeneratorTests` | `GenerateToken_OfSetLength_ReturnsNumericCode(20)` | ✅ |
| `Identity.Tests.Util.NumericOtpGeneratorTests` | `GenerateToken_OfSetLength_ReturnsNumericCode(6)` | ✅ |
| `Identity.Tests.Util.OtpHasherTests` | `Hash_ShouldReturnValidHashAndSalt` | ✅ |
| `Identity.Tests.Util.OtpHasherTests` | `VerifyHash_WithCorrectOtp_ReturnsTrue` | ✅ |
| `Identity.Tests.Util.OtpHasherTests` | `VerifyHash_WithIncorrectOtp_ReturnsFalse` | ✅ |
| `Identity.Tests.Util.OtpHasherTests` | `VerifyHash_WithModifiedHash_ReturnsFalse` | ✅ |
| `Identity.Tests.Util.OtpHasherTests` | `VerifyHash_WithModifiedSalt_ReturnsFalse` | ✅ |

### Pendo.JourneyService
| Location | Test Name | Passing |
|----------|-----------|:------:|
| `test_check_journey` | `test_check_inputs_journey_type_1_sets_repeat_until` | ✅ |
| `test_check_journey` | `test_check_inputs_journey_type_2_missing_fields` | ✅ |
| `test_check_journey` | `test_check_inputs_missing_required_field` | ✅ |
| `test_check_journey` | `test_check_inputs_success` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_boot_height` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_boot_width` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_end_location` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_journey_status` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_journey_type` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_max_price` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_num_passengers` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_start_date` | ✅ |
| `test_filter_journeys` | `test_filter_journeys_start_location` | ✅ |
| `test_journey_repo` | `test_adjust_journey_invalid_price` | ✅ |
| `test_journey_repo` | `test_adjust_journey_not_found` | ✅ |
| `test_journey_repo` | `test_adjust_journey_success` | ✅ |
| `test_journey_repo` | `test_create_journey` | ✅ |
| `test_journey_repo` | `test_get_journeys` | ✅ |
| `test_journey_repo` | `test_lock_journey_already_locked` | ✅ |
| `test_journey_repo` | `test_lock_journey_not_found` | ✅ |
| `test_journey_repo` | `test_lock_journey_success` | ✅ |

### Pendo.MessageService
| Location | Test Name | Passing |
|----------|-----------|:------:|
| `TestHttpEndpoints` | `test_create_conversation_handler` | ✅ |
| `TestHttpEndpoints` | `test_health_check` | ✅ |
| `TestHttpEndpoints` | `test_invalid_participants_in_create_conversation` | ✅ |
| `TestHttpEndpoints` | `test_missing_fields_in_create_conversation` | ✅ |
| `TestHttpEndpoints` | `test_root_handler` | ✅ |
| `TestHttpEndpoints` | `test_user_conversations_handler` | ✅ |
| `test_app` | `test_health_check` | ✅ |
| `test_app` | `test_root_handler` | ✅ |
| `test_app` | `test_setup_http_server` | ✅ |
| `test_app` | `test_setup_ws_server` | ✅ |
| `test_app` | `test_websocket_handler_welcome_message` | ✅ |
| `test_message_handler` | `test_broadcast_to_conversation` | ✅ |
| `test_message_handler` | `test_handle_chat_message` | ✅ |
| `test_message_handler` | `test_handle_history_request` | ✅ |
| `test_message_handler` | `test_handle_join_conversation` | ✅ |
| `test_message_handler` | `test_register_user` | ✅ |
| `test_message_handler` | `test_remove_user` | ✅ |
| `test_message_repository` | `test_add_user_to_conversation` | ✅ |
| `test_message_repository` | `test_create_conversation` | ✅ |
| `test_message_repository` | `test_create_conversation_with_participants` | ✅ |
| `test_message_repository` | `test_get_conversation_by_id` | ✅ |
| `test_message_repository` | `test_get_messages_by_conversation_id` | ✅ |
| `test_message_repository` | `test_get_user_by_id` | ✅ |
| `test_message_repository` | `test_get_user_conversations` | ✅ |
| `test_message_repository` | `test_save_message` | ✅ |
| `test_websocket` | `test_chat_message_exchange` | ✅ |
| `test_websocket` | `test_join_conversation` | ✅ |
| `test_websocket` | `test_request_message_history` | ✅ |
| `test_websocket` | `test_user_registration` | ✅ |
| `test_websocket` | `test_websocket_connection` | ✅ |

### Pendo.PaymentService
| Location | Test Name | Passing |
|----------|-----------|:------:|
| `test_CompletedBookingCmd` | `test_completed_booking_booking_not_found` | ✅ |
| `test_CompletedBookingCmd` | `test_completed_booking_constructor` | ✅ |
| `test_CompletedBookingCmd` | `test_completed_booking_exception` | ✅ |
| `test_CompletedBookingCmd` | `test_completed_booking_margin_calculation` | ✅ |
| `test_CompletedBookingCmd` | `test_completed_booking_success` | ✅ |
| `test_CompletedBookingCmd` | `test_completed_booking_transaction_creation` | ✅ |
| `test_CreatePayoutCmd` | `test_create_payout_constructor` | ✅ |
| `test_CreatePayoutCmd` | `test_create_payout_database_error` | ✅ |
| `test_CreatePayoutCmd` | `test_create_payout_email_sending` | ✅ |
| `test_CreatePayoutCmd` | `test_create_payout_no_balance_sheet` | ✅ |
| `test_CreatePayoutCmd` | `test_create_payout_success` | ✅ |
| `test_CreatePayoutCmd` | `test_create_payout_transaction_creation` | ✅ |
| `test_CreatePayoutCmd` | `test_create_payout_user_not_found` | ✅ |
| `test_PaymentMethodsCmd` | `test_payment_methods_empty` | ✅ |
| `test_PaymentMethodsCmd` | `test_payment_methods_exception` | ✅ |
| `test_PaymentMethodsCmd` | `test_payment_methods_missing_card_data` | ✅ |
| `test_PaymentMethodsCmd` | `test_payment_methods_mixed_payment_types` | ✅ |
| `test_PaymentMethodsCmd` | `test_payment_methods_sets_api_key` | ✅ |
| `test_PaymentMethodsCmd` | `test_payment_methods_success` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_constructor` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_create_booker_balance` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_create_driver_balance` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_driver_not_found` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_incorrect_status` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_insufficient_balance` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_not_found` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_passenger_not_found` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_success` | ✅ |
| `test_PendingBookingCmd` | `test_pending_booking_update_pending_exception` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_balance_update_failure` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_booking_not_found` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_constructor` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_driver_refund` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_invalid_user_type` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_no_driver_approval` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_passenger_early_cancellation` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_passenger_late_cancellation` | ✅ |
| `test_RefundPaymentCmd` | `test_refund_payment_passenger_success` | ✅ |
| `test_StripeWebhookCmd` | `test_webhook_complete_flow_with_new_balance` | ✅ |
| `test_StripeWebhookCmd` | `test_webhook_constructor` | ✅ |
| `test_StripeWebhookCmd` | `test_webhook_no_user_balance` | ✅ |
| `test_StripeWebhookCmd` | `test_webhook_success` | ✅ |
| `test_StripeWebhookCmd` | `test_webhook_transaction_not_found` | ✅ |
| `test_StripeWebhookCmd` | `test_webhook_update_failure` | ✅ |
| `test_StripeWebhookCmd` | `test_webhook_user_not_found` | ✅ |
| `test_ViewBalanceCmd` | `test_view_balance_constructor` | ✅ |
| `test_ViewBalanceCmd` | `test_view_balance_create_balance_failure` | ✅ |
| `test_ViewBalanceCmd` | `test_view_balance_get_balance_after_create_failure` | ✅ |
| `test_ViewBalanceCmd` | `test_view_balance_no_balance_sheet` | ✅ |
| `test_ViewBalanceCmd` | `test_view_balance_repository_exception` | ✅ |
| `test_ViewBalanceCmd` | `test_view_balance_success` | ✅ |
| `test_ViewBalanceCmd` | `test_view_balance_user_not_found` | ✅ |

## Functional Tests

Test ID | Description | Expected Results | Actual Results
--------| ----------- | ---------------- | ---------------
1.1 | Navigate to the sign-in page. Enter valid email address. Submit form. | User should receive OTP email notification that will allow them to give account details (Name) and sign in. | User received OTP email notification. They were able to enter their first and last name and successfully signed in.
1.2 | Navigate to the sign-in page. Enter invalid email address: no @ character; no .com/.uk ending. | User receives an error message. Message explains the reason for the error. | An error message was displayed. No OTP was sent.
1.3 | Navigate to the login page. Enter valid email address. Click “Login” to verify and access the app. | User should receive OTP email notification that contains a code. User enters code on the app and is logged in. | User received the OTP email, entered the code in the app, and successfully logged in.
2.1 | Navigate to Top Up Balance page in account settings. Choose account to top up. Add valid card details. | Card details are securely stored for when the user wants to top up their card. | User entered valid card details, which were securely saved for future top-ups.
2.2 | Select stored card during checkout. Complete transaction. | Payment is successfully carried out. | Stored card was available at checkout. The user completed the transaction successfully, and stored cards were visible in account settings.
4.1 | Navigate to the one-time journey section. Set the search criteria. | Available one-time journeys are displayed. User is able to look through them. | Available one-time journeys are displayed. User was able to browse through them.
4.2 | Navigate to the commuter journeys section. Set the search criteria. | Available commuter journeys are displayed. User is able to look through them. | Option to view commuter journeys appeared. When selected, available commuter journeys were displayed.
4.3 | Click on a journey listing. | Journey details (date, time, cost, pick-up and end-point locations) are shown. | Journey details including name, driver rating, price, pick-up, and destination were displayed as expected.
5.1 | Enter search criteria. Execute search. | Journeys matching criteria are displayed. | Journeys matching the search criteria were displayed correctly.
5.2 | Open list view. | Journeys are displayed visually in list format. | Journeys were presented clearly in list format.
6.1 | Choose a journey. Confirm booking. | User is sent a confirmation message stating that booking is successful. | The app displayed a confirmation notification.
7.1 | Enter payment details. Confirm transaction. | Payment is processed successfully. Booking confirmation email is evidence of successful transaction. | An email was sent to the user confirming the payment had been processed and the booking was pending.
7.2 | Use card with insufficient funds. | Payment is declined with an appropriate error message. | Error is shown on checkout page stating that the user’s balance is insufficient and providing information on the required funds needed to book the journey.
8.1 | Complete booking. Check registered email. | Confirmation email is received. | Confirmation email was successfully received.
9.1 | Complete booking. Navigate to Upcoming Journeys page. | Booking details are stored and accessible to the user. | Booking details were available on the Upcoming Journeys page, with an option to contact the driver.
10.1 | Set cost, time, location, number of passengers, extras. | Settings are saved correctly. | All configured settings were saved correctly and visible under the advertised tab on the “My Listings” page.
11.1 | Book a journey through the booking service. | Journey no longer appears in available listings. | Once booked, the journey was hidden from the list of available journeys.
12.1 | Save a recurring commute. Rebook with one click. | Journey is rebooked easily. Confirmation email sent. | Recurring commuter journeys were rebooked successfully.
13.1 | Cancel 15 min before journey time. | Cancellation follows the policy. Cancellation is at no cost to user. | Cancellation follows policy: free cancellation within 15 minutes.
13.2 | Cancel with less than 15 min left before journey time. | Cancellation follows the policy. The user that cancelled is charged for 75% of the agreed journey cost. | Cancellation follows policy: user is charged 75% of journey cost when cancelled with less than 15 minutes remaining.
14.1 | User (driver) arrives at designated pick-up location. Sends a message to user. | Other user (passenger) receives the message and knows the driver is at pick-up location. | Passenger receives a notification when driver arrives at pick-up location.
15.1 | Check booking details. Open map. | Map displays the location. | The map correctly displays the pick-up and drop-off locations on the map. The pick-up location is marked by a green marker while the drop-off location is marked by a red marker.
16.1 | Complete journey. Leave a rating. | Option to confirm or deny that a ride was completed. Rating is recorded on driver account. | User can confirm ride completion and leave a rating successfully.
17.1 | Edit details before confirmation. | User and Driver negotiate changes. Changes are applied to journey details. Changes reflected in bookings section. | User and driver can negotiate and apply booking changes; updates reflected in booking details.
18.1 | Navigate to “My Listings” area. | Bookings are displayed correctly. | Upcoming displayed correctly. Cancelled journeys not displayed.
19.1 | View weekly income for driver. | Earnings are shown. | This feature was not implemented.
20.1 | View weekly income for driver. | Weekly earnings are plotted graphically. | This feature was not implemented.
21.1 | Update booking fee percentage. | Success message that the booking fee has been updated. | Admin dashboard displayed a success message confirming the update of the booking fee.
22.1 | Access reports on Manager website. | Weekly income (0.5% of bookings) is displayed. | Weekly income is shown on the dashboard as a graph.
23.1 | View financial report graph. | Income is displayed visually. | Weekly revenue since the start of that week is shown.
24.1 | Driver sets unavailable dates. | Commute is disabled, and users are notified. | This was not implemented.
25.1 | Book > 4 trips in a week. | Discount is automatically applied. | Discount was correctly applied to qualifying commuter bookings. Savings were shown during checkout.
26.1 | Open messaging service. Report issue. | Management receives message. | Management receives message from the user and is able to communicate with them.
26.2 | Open messaging service. Communicate with other user(s). | Other user(s) send and receive messages. | Users can send and receive messages successfully.
