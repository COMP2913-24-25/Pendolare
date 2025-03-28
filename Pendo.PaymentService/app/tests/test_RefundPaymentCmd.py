import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from src.db.PaymentRepository import PaymentRepository
from src.db.PendoDatabase import Transaction, UserBalance
from src.returns.PaymentReturns import StatusResponse
from src.endpoints.RefundPaymentCmd import RefundPaymentCommand
import uuid

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def booking_id():
    return str(uuid.uuid4())

@pytest.fixture
def mock_booking():
    booking = MagicMock()
    booking.BookingId = str(uuid.uuid4())
    booking.UserId = str(uuid.uuid4())  # Passenger ID
    booking.FeeMargin = 0.1  # 10% fee
    booking.DriverApproval = True
    journey = MagicMock()
    journey.UserId = str(uuid.uuid4())  # Driver ID
    booking.Journey_ = journey
    return booking

@pytest.fixture
def refund_payment_command(mock_logger, booking_id):
    cancelled_by_id = str(uuid.uuid4())
    latest_price = 100.0
    cancellation_time = datetime.now()
    Journey_time = cancellation_time + timedelta(hours=1)
    
    command = RefundPaymentCommand(
        mock_logger, 
        booking_id, 
        cancelled_by_id, 
        latest_price, 
        cancellation_time, 
        Journey_time
    )
    command.PaymentRepository = MagicMock(spec=PaymentRepository)
    return command

def test_refund_payment_passenger_success(refund_payment_command, mock_booking):
    # Arrange
    refund_payment_command.PaymentRepository.GetBookingById.return_value = mock_booking
    refund_payment_command.PaymentRepository.GetUserType.return_value = "Passenger"
    
    refund_payment_command.PaymentRepository.UpdatePendingBalance.return_value = None
    refund_payment_command.PaymentRepository.UpdateNonPendingBalance.return_value = None
    refund_payment_command.PaymentRepository.CreateTransaction.return_value = None
    refund_payment_command.PaymentRepository.UpdateBookingStatus.return_value = None
    
    # Act
    result = refund_payment_command.Execute()

    # Assert
    assert result.Status == "success"
    
    # Verify method calls
    refund_payment_command.PaymentRepository.GetBookingById.assert_called_once()
    refund_payment_command.PaymentRepository.GetUserType.assert_called_once()

def test_refund_payment_driver_refund(refund_payment_command, mock_booking):
    # Arrange
    refund_payment_command.PaymentRepository.GetBookingById.return_value = mock_booking
    refund_payment_command.PaymentRepository.GetUserType.return_value = "Driver"
    
    # Ensure repository methods are mocked to return successfully
    refund_payment_command.PaymentRepository.UpdatePendingBalance.return_value = None
    refund_payment_command.PaymentRepository.CreateTransaction.return_value = None
    refund_payment_command.PaymentRepository.UpdateBookingStatus.return_value = None
    
    # Act
    result = refund_payment_command.Execute()

    # Assert
    assert result.Status == "success"
    
    # Verify no updates to non-pending balance for driver
    refund_payment_command.PaymentRepository.UpdateNonPendingBalance.assert_not_called()

def test_refund_payment_booking_not_found(refund_payment_command):
    # Arrange
    refund_payment_command.PaymentRepository.GetBookingById.return_value = None

    # Act
    result = refund_payment_command.Execute()

    # Assert
    assert result.Status == "fail"
    assert "Booking not found" in result.Error
    refund_payment_command.logger.error.assert_called_once()

def test_refund_payment_invalid_user_type(refund_payment_command, mock_booking):
    # Arrange
    refund_payment_command.PaymentRepository.GetBookingById.return_value = mock_booking
    refund_payment_command.PaymentRepository.GetUserType.return_value = None

    # Act
    result = refund_payment_command.Execute()

    # Assert
    assert result.Status == "fail"
    assert "Could not determine user type" in result.Error
    refund_payment_command.logger.error.assert_called_once()

def test_refund_payment_no_driver_approval(refund_payment_command, mock_booking):
    # Arrange
    mock_booking.DriverApproval = False
    refund_payment_command.PaymentRepository.GetBookingById.return_value = mock_booking
    refund_payment_command.PaymentRepository.GetUserType.return_value = "Passenger"

    # Act
    result = refund_payment_command.Execute()

    # Assert
    assert result.Status == "fail"
    assert "Booking does not have driver approval" in result.Error
    refund_payment_command.logger.error.assert_called_once()

def test_refund_payment_passenger_late_cancellation(refund_payment_command, mock_booking):
    # Arrange
    refund_payment_command.CancellationTime = datetime.now()
    refund_payment_command.JourneyTime = refund_payment_command.CancellationTime + timedelta(minutes=5)
    refund_payment_command.PaymentRepository.GetBookingById.return_value = mock_booking
    refund_payment_command.PaymentRepository.GetUserType.return_value = "Passenger"
    
    # Ensure repository methods are mocked to return successfully
    refund_payment_command.PaymentRepository.UpdatePendingBalance.return_value = None
    refund_payment_command.PaymentRepository.UpdateNonPendingBalance.return_value = None
    refund_payment_command.PaymentRepository.CreateTransaction.return_value = None
    refund_payment_command.PaymentRepository.UpdateBookingStatus.return_value = None

    # Act
    result = refund_payment_command.Execute()

    # Assert
    assert result.Status == "success"

def test_refund_payment_passenger_early_cancellation(refund_payment_command, mock_booking):
    # Arrange
    refund_payment_command.CancellationTime = datetime.now()
    refund_payment_command.JourneyTime = refund_payment_command.CancellationTime + timedelta(hours=2)
    refund_payment_command.PaymentRepository.GetBookingById.return_value = mock_booking
    refund_payment_command.PaymentRepository.GetUserType.return_value = "Passenger"
    
    # Ensure repository methods are mocked to return successfully
    refund_payment_command.PaymentRepository.UpdatePendingBalance.return_value = None
    refund_payment_command.PaymentRepository.CreateTransaction.return_value = None
    refund_payment_command.PaymentRepository.UpdateBookingStatus.return_value = None

    # Act
    result = refund_payment_command.Execute()

    # Assert
    assert result.Status == "success"

def test_refund_payment_balance_update_failure(refund_payment_command, mock_booking):
    # Arrange
    refund_payment_command.PaymentRepository.GetBookingById.return_value = mock_booking
    refund_payment_command.PaymentRepository.GetUserType.return_value = "Passenger"
    refund_payment_command.PaymentRepository.UpdatePendingBalance.return_value = False

    # Act
    result = refund_payment_command.Execute()

    # Assert
    assert result.Status == "fail"
    assert "Failed to update driver's pending balance" in result.Error
    refund_payment_command.logger.error.assert_called_once()

def test_refund_payment_constructor():
    # Arrange
    logger = MagicMock()
    booking_id = str(uuid.uuid4())
    cancelled_by_id = str(uuid.uuid4())
    latest_price = 100.0
    cancellation_time = datetime.now()
    Journey_time = cancellation_time + timedelta(hours=1)
    
    # Act
    command = RefundPaymentCommand(
        logger, 
        booking_id, 
        cancelled_by_id, 
        latest_price, 
        cancellation_time, 
        Journey_time
    )
    
    # Assert
    assert command.logger == logger
    assert command.BookingId == booking_id
    assert command.CancelledById == cancelled_by_id
    assert command.LatestPrice == latest_price
    assert command.CancellationTime == cancellation_time
    assert command.JourneyTime == Journey_time
    assert isinstance(command.PaymentRepository, PaymentRepository)