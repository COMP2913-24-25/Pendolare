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
| Test Name | Passing |
|-----------|:------:|
| `Update_ModifiesExistingEntity` | ✅ |
| `Create_ReturnsModelOfCorrectType` | ✅ |
| `Handle_UserNotFound_ReturnsFailureResponse` | ✅ |
| `VerifyHash_WithModifiedHash_ReturnsFalse` | ✅ |
| `VerifyHash_WithIncorrectOtp_ReturnsFalse` | ✅ |
| `Read_Should_Return_Filtered_Entities` | ✅ |
| `Handle_UserFound_ReturnsUserDetailsSuccessfully` | ✅ |
| `Handle_WhenOtpExpired_ReturnsFalse` | ✅ |
| `UtcNow_ReturnsTime` | ✅ |
| `Create_AddsNewEntity` | ✅ |
| `Read_WithNullFilter_ReturnsAllEntities` | ✅ |
| `Hash_ShouldReturnValidHashAndSalt` | ✅ |
| `GenerateToken_OfSetLength_ReturnsNumericCode(100)` | ✅ |
| `Handle_CreatesNewUserAndSendsOtpSuccessfully("manager@test.com",2)` | ✅ |
| `Handle_CreatesNewUserAndSendsOtpSuccessfully("mundrayj@gmail.com",1)` | ✅ |
| `Handle_WhenOtpValid_ReturnsTrueAndJwt` | ✅ |
| `Handle_WhenOtpInvalid_ReturnsFalse` | ✅ |
| `Handle_UserFound_NullNames_DefaultsToEmptyString` | ✅ |
| `GenerateToken_OfSetLength_ReturnsNumericCode(6)` | ✅ |
| `Handle_WhenOtpLoginNotFound_ReturnsFalse` | ✅ |
| `GenerateToken_OfSetLength_ReturnsNumericCode(20)` | ✅ |
| `Handle_WhenUserExists_UsesExistingUser` | ✅ |
| `GenerateToken_OfSetLength_ReturnsNumericCode(1)` | ✅ |
| `GenerateJwt_ShouldContainCorrectClaims` | ✅ |
| `Delete_RemovesExistingEntity` | ✅ |
| `GenerateJwt_ShouldReturnValidToken` | ✅ |
| `VerifyHash_WithCorrectOtp_ReturnsTrue` | ✅ |
| `VerifyHash_WithModifiedSalt_ReturnsFalse` | ✅ |
| `Handle_WhenMultipleUsersExist_ReturnsFalse` | ✅ |
| `Handle_UserFound_UpdateOnlyNonEmptyValues` | ✅ |
| `Handle_UserFound_UpdatesFirstAndLastNameSuccessfully` | ✅ |
| `Handle_WhenEmailFails_ReturnsFalse` | ✅ |
| `Handle_WhenUserDoesNotExist_ReturnsFalse` | ✅ |
| `Handle_UserNotFound_ReturnsFailureResponse` | ✅ |

### Pendo.JourneyService
| Test Name | Passing |
|-----------|:------:|
| `test_check_inputs_success` | ✅ |
| `test_check_inputs_missing_required_field` | ✅ |
| `test_check_inputs_journey_type_2_missing_fields` | ✅ |
| `test_check_inputs_journey_type_1_sets_repeat_until` | ✅ |
| `test_filter_journeys_max_price` | ✅ |
| `test_filter_journeys_boot_height` | ✅ |
| `test_filter_journeys_boot_width` | ✅ |
| `test_filter_journeys_journey_type` | ✅ |
| `test_filter_journeys_num_passengers` | ✅ |
| `test_filter_journeys_start_date` | ✅ |
| `test_filter_journeys_start_location` | ✅ |
| `test_filter_journeys_end_location` | ✅ |
| `test_filter_journeys_journey_status` | ✅ |
| `test_get_journeys` | ✅ |
| `test_lock_journey_success` | ✅ |
| `test_lock_journey_not_found` | ✅ |
| `test_lock_journey_already_locked` | ✅ |
| `test_create_journey` | ✅ |
| `test_adjust_journey_success` | ✅ |
| `test_adjust_journey_not_found` | ✅ |
| `test_adjust_journey_invalid_price` | ✅ |

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
| Test Name | Passing |
|-----------|:------:|
| `test_completed_booking_constructor` | ✅ |
| `test_completed_booking_success` | ✅ |
| `test_completed_booking_exception` | ✅ |
| `test_completed_booking_booking_not_found` | ✅ |
| `test_completed_booking_transaction_creation` | ✅ |
| `test_completed_booking_margin_calculation` | ✅ |
| `test_create_payout_success` | ✅ |
| `test_create_payout_user_not_found` | ✅ |
| `test_create_payout_no_balance_sheet` | ✅ |
| `test_create_payout_email_sending` | ✅ |
| `test_create_payout_transaction_creation` | ✅ |
| `test_create_payout_database_error` | ✅ |
| `test_create_payout_constructor` | ✅ |
| `test_payment_methods_success` | ✅ |
| `test_payment_methods_empty` | ✅ |
| `test_payment_methods_missing_card_data` | ✅ |
| `test_payment_methods_exception` | ✅ |
| `test_payment_methods_mixed_payment_types` | ✅ |
| `test_payment_methods_sets_api_key` | ✅ |
| `test_pending_booking_success` | ✅ |
| `test_pending_booking_not_found` | ✅ |
| `test_pending_booking_incorrect_status` | ✅ |
| `test_pending_booking_driver_not_found` | ✅ |
| `test_pending_booking_passenger_not_found` | ✅ |
| `test_pending_booking_create_driver_balance` | ✅ |
| `test_pending_booking_create_booker_balance` | ✅ |
| `test_pending_booking_insufficient_balance` | ✅ |
| `test_pending_booking_update_pending_exception` | ✅ |
| `test_pending_booking_constructor` | ✅ |
| `test_refund_payment_passenger_success` | ✅ |
| `test_refund_payment_driver_refund` | ✅ |
| `test_refund_payment_booking_not_found` | ✅ |
| `test_refund_payment_invalid_user_type` | ✅ |
| `test_refund_payment_no_driver_approval` | ✅ |
| `test_refund_payment_passenger_late_cancellation` | ✅ |
| `test_refund_payment_passenger_early_cancellation` | ✅ |
| `test_refund_payment_balance_update_failure` | ✅ |
| `test_refund_payment_constructor` | ✅ |
| `test_webhook_success` | ✅ |
| `test_webhook_user_not_found` | ✅ |
| `test_webhook_no_user_balance` | ✅ |
| `test_webhook_transaction_not_found` | ✅ |
| `test_webhook_update_failure` | ✅ |
| `test_webhook_constructor` | ✅ |
| `test_webhook_complete_flow_with_new_balance` | ✅ |
| `test_view_balance_success` | ✅ |
| `test_view_balance_user_not_found` | ✅ |
| `test_view_balance_no_balance_sheet` | ✅ |
| `test_view_balance_repository_exception` | ✅ |
| `test_view_balance_create_balance_failure` | ✅ |
| `test_view_balance_constructor` | ✅ |
| `test_view_balance_get_balance_after_create_failure` | ✅ |
