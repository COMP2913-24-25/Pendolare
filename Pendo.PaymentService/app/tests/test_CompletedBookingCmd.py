import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from src.db.PaymentRepository import PaymentRepository
from src.db.PendoDatabase import Transaction, UserBalance
from src.returns.PaymentReturns import StatusResponse
from src.endpoints.CompletedBookingCmd import CompletedBookingCommand
import uuid

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def booking_id():
    return 1

@pytest.fixture
def mock_booking():
    booking = MagicMock()
    booking.BookingId = 1
    booking.UserId = str(uuid.uuid4())  # Passenger ID
    booking.FeeMargin = 0.1  # 10% fee
    booking_status = MagicMock()
    booking_status.Status = "Confirmed"
    booking.BookingStatus_ = booking_status
    journey = MagicMock()
    journey.UserId = str(uuid.uuid4())  # Driver ID
    journey.AdvertisedPrice = 100.0
    journey.CurrencyCode = "gbp"
    booking.Journey_ = journey
    return booking

@pytest.fixture
def mock_driver():
    driver = MagicMock()
    driver.UserId = str(uuid.uuid4())
    return driver

@pytest.fixture
def mock_passenger():
    passenger = MagicMock()
    passenger.UserId = str(uuid.uuid4())
    return passenger

@pytest.fixture
def mock_driver_balance():
    balance = MagicMock(spec=UserBalance)
    balance.NonPending = 50.0
    balance.Pending = 25.0
    return balance

@pytest.fixture
def mock_passenger_balance():
    balance = MagicMock(spec=UserBalance)
    balance.NonPending = 150.0
    balance.Pending = 0.0
    return balance

@pytest.fixture
def completed_booking_command(mock_logger, booking_id):
    command = CompletedBookingCommand(mock_logger, booking_id)
    command.PaymentRepository = MagicMock(spec=PaymentRepository)
    command.LatestPrice = 100.0
    command.booking_id = booking_id
    return command

def test_completed_booking_constructor():
    # Arrange
    logger = MagicMock()
    booking_id = 1
    latest_price = 100.0
    
    # Act
    command = CompletedBookingCommand(logger, booking_id, latest_price)
    
    # Assert
    assert command.logger == logger
    assert command.BookingId == booking_id
    assert command.LatestPrice == latest_price
    assert isinstance(command.PaymentRepository, PaymentRepository)

def test_completed_booking_success(completed_booking_command, mock_booking, mock_driver, mock_passenger, mock_driver_balance, mock_passenger_balance):
    # Arrange
    completed_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
    
    # Act
    result = completed_booking_command.Execute()
    
    # Assert
    assert result.Status == "success"
    
    # Verify passenger balance update
    completed_booking_command.PaymentRepository.UpdateNonPendingBalance.assert_any_call(
        mock_booking.UserId, 
        -1 * completed_booking_command.LatestPrice
    )
    
    # Verify passenger transaction creation
    passenger_transaction = completed_booking_command.PaymentRepository.CreateTransaction.call_args_list[0][0][0]
    assert passenger_transaction.UserId == mock_booking.UserId
    assert passenger_transaction.Value == float(completed_booking_command.LatestPrice)
    assert passenger_transaction.CurrencyCode == "gbp"
    assert passenger_transaction.TransactionStatusId == 1
    assert passenger_transaction.TransactionTypeId == 3
    
    # Verify driver pending balance update
    completed_booking_command.PaymentRepository.UpdatePendingBalance.assert_called_with(
        mock_booking.Journey_.UserId,  # Note the lowercase 'Journey_'
        -1 * completed_booking_command.LatestPrice
    )
    
    # Verify driver final balance update
    margin = round(mock_booking.FeeMargin * completed_booking_command.LatestPrice, 2)
    final_driver_price = completed_booking_command.LatestPrice - margin
    completed_booking_command.PaymentRepository.UpdateNonPendingBalance.assert_any_call(
        mock_booking.Journey_.UserId,  # Note the lowercase 'Journey_'
        final_driver_price
    )

def test_completed_booking_exception(completed_booking_command):
    # Arrange
    completed_booking_command.PaymentRepository.GetBookingById.side_effect = Exception("Database error")
    
    # Act
    result = completed_booking_command.Execute()
    
    # Assert
    assert result.Status == "fail"
    assert "Database error" in result.Error
    completed_booking_command.logger.error.assert_called_once()

def test_completed_booking_booking_not_found(completed_booking_command):
    # Arrange
    completed_booking_command.PaymentRepository.GetBookingById.return_value = None
    
    # Act
    result = completed_booking_command.Execute()
    
    # Assert
    assert result.Status == "fail"
    assert "Booking not found" in result.Error
    completed_booking_command.logger.error.assert_called_once()

def test_completed_booking_transaction_creation(completed_booking_command, mock_booking):
    # Arrange
    completed_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
    
    # Act
    result = completed_booking_command.Execute()
    
    # Assert
    assert result.Status == "success"
    
    # Verify multiple transaction creations
    assert completed_booking_command.PaymentRepository.CreateTransaction.call_count == 3
    
    # Verify transaction details
    transactions = [call[0][0] for call in completed_booking_command.PaymentRepository.CreateTransaction.call_args_list]
    
    # Check passenger transaction
    passenger_transaction = transactions[0]
    assert passenger_transaction.UserId == mock_booking.UserId
    assert passenger_transaction.TransactionTypeId == 3
    
    # Check driver intermediate transaction
    driver_intermediate_transaction = transactions[1]
    assert driver_intermediate_transaction.UserId == mock_booking.Journey_.UserId
    assert driver_intermediate_transaction.TransactionTypeId == 1
    
    # Check driver final transaction
    driver_final_transaction = transactions[2]
    assert driver_final_transaction.UserId == mock_booking.Journey_.UserId
    assert driver_final_transaction.TransactionTypeId == 2

def test_completed_booking_margin_calculation(completed_booking_command, mock_booking):
    # Arrange
    test_price = 200.0
    completed_booking_command.LatestPrice = test_price
    completed_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
    
    # Act
    result = completed_booking_command.Execute()
    
    # Assert
    assert result.Status == "success"
    
    # Calculate expected margin and price
    expected_margin = round(mock_booking.FeeMargin * test_price, 2)
    expected_driver_price = test_price - expected_margin
    
    # Verify final driver balance update with correct margin deduction
    completed_booking_command.PaymentRepository.UpdateNonPendingBalance.assert_any_call(
        mock_booking.Journey_.UserId, 
        expected_driver_price
    )