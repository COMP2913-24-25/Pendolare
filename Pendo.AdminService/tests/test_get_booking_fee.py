from unittest.mock import MagicMock
from app.get_booking_fee import GetBookingFeeCommand
from fastapi import status

def test_get_booking_fee_success():
    
    configuration_provider_mock = MagicMock()
    configuration_provider_mock.GetSingleValue.return_value = "0.05"  
    response_mock = MagicMock()
    db_session_mock = MagicMock()

    command = GetBookingFeeCommand(configuration_provider_mock, response_mock, db_session_mock)

    
    result = command.Execute()

    assert result == {"BookingFee": "5.00%"}
    configuration_provider_mock.GetSingleValue.assert_called_once_with(db_session_mock, "Booking.FeeMargin")
    response_mock.assert_not_called() 

def test_get_booking_fee_exception():
    
    configuration_provider_mock = MagicMock()
    configuration_provider_mock.GetSingleValue.side_effect = Exception("Database error")
    response_mock = MagicMock()
    db_session_mock = MagicMock()

    command = GetBookingFeeCommand(configuration_provider_mock, response_mock, db_session_mock)
    result = command.Execute()
    assert result == {"Error": "Database error"}
    assert response_mock.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    configuration_provider_mock.GetSingleValue.assert_called_once_with(db_session_mock, "Booking.FeeMargin")