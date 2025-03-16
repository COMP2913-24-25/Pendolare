import pytest
from unittest.mock import MagicMock
from app.get_booking_fee import GetBookingFeeCommand
from fastapi import status

def test_get_booking_fee_success():
    """
    GIVEN a GetBookingFeeCommand instance
    WHEN the configuration provider returns a valid booking fee
    THEN the Execute method should return the booking fee formatted correctly.
    """
    # Arrange
    configuration_provider_mock = MagicMock()
    configuration_provider_mock.GetSingleValue.return_value = "0.05"  # Example fee
    response_mock = MagicMock()
    db_session_mock = MagicMock()

    command = GetBookingFeeCommand(configuration_provider_mock, response_mock, db_session_mock)

    # Act
    result = command.Execute()

    # Assert
    assert result == {"BookingFee": "5.00%"}
    configuration_provider_mock.GetSingleValue.assert_called_once_with(db_session_mock, "Booking.FeeMargin")
    response_mock.assert_not_called()  # Ensure no response status was set

def test_get_booking_fee_exception():
    """
    GIVEN a GetBookingFeeCommand instance
    WHEN the configuration provider raises an exception
    THEN the Execute method should set the response status to 500 and return an error message.
    """
    # Arrange
    configuration_provider_mock = MagicMock()
    configuration_provider_mock.GetSingleValue.side_effect = Exception("Database error")
    response_mock = MagicMock()
    db_session_mock = MagicMock()

    command = GetBookingFeeCommand(configuration_provider_mock, response_mock, db_session_mock)

    # Act
    result = command.Execute()

    # Assert
    assert result == {"Error": "Database error"}
    assert response_mock.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    configuration_provider_mock.GetSingleValue.assert_called_once_with(db_session_mock, "Booking.FeeMargin")