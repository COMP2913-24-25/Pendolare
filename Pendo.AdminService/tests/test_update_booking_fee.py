from app.update_booking_fee import UpdateBookingFeeCommand
from app.conftest import *
from fastapi import status

def test_update_booking_fee_success(db_session_mock, request_mock, response_mock, configuration_provider_mock, logger_mock):
    request_mock.FeeMargin = 0.05  

    command = UpdateBookingFeeCommand(db_session_mock, request_mock, response_mock, configuration_provider_mock, logger_mock)

    result = command.Execute()

    assert result == {"Status": "Booking fee margin updated successfully"}
    configuration_provider_mock.UpdateValue.assert_called_once_with(db_session_mock, "Booking.FeeMargin", "0.05")
    db_session_mock.commit.assert_called_once()
    response_mock.assert_not_called()  

def test_update_booking_fee_invalid_fee_margin_too_low(db_session_mock, request_mock, response_mock, configuration_provider_mock, logger_mock):
    request_mock.FeeMargin = -0.01  

    command = UpdateBookingFeeCommand(db_session_mock, request_mock, response_mock, configuration_provider_mock, logger_mock)

    result = command.Execute()


    assert result == {"Error": "Fee margin must be between 0.00 and 0.99"}
    assert response_mock.status_code == status.HTTP_400_BAD_REQUEST
    configuration_provider_mock.UpdateValue.assert_not_called()
    db_session_mock.commit.assert_not_called()
    db_session_mock.rollback.assert_not_called()


def test_update_booking_fee_invalid_fee_margin_too_high(db_session_mock, request_mock, response_mock, configuration_provider_mock, logger_mock):

    request_mock.FeeMargin = 1.00  

    command = UpdateBookingFeeCommand(db_session_mock, request_mock, response_mock, configuration_provider_mock, logger_mock)

    result = command.Execute()

    assert result == {"Error": "Fee margin must be between 0.00 and 0.99"}
    assert response_mock.status_code == status.HTTP_400_BAD_REQUEST
    configuration_provider_mock.UpdateValue.assert_not_called()
    db_session_mock.commit.assert_not_called()
    db_session_mock.rollback.assert_not_called()

def test_update_booking_fee_exception(db_session_mock, request_mock, response_mock, configuration_provider_mock, logger_mock):
   
    request_mock.FeeMargin = 0.05
    configuration_provider_mock.UpdateValue.side_effect = Exception("Database update failed")

    command = UpdateBookingFeeCommand(db_session_mock, request_mock, response_mock, configuration_provider_mock, logger_mock)

    result = command.Execute()

    assert result == {"Error": "Database update failed"}
    assert response_mock.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    db_session_mock.rollback.assert_called_once()
    db_session_mock.commit.assert_not_called()