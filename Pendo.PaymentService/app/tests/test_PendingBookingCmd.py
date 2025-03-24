# import pytest
# from unittest.mock import MagicMock, patch
# from datetime import datetime
# from src.db.PaymentRepository import PaymentRepository
# from src.db.PendoDatabase import Transaction, UserBalance
# from src.returns.PaymentReturns import StatusResponse
# from src.endpoints.PendingBookingCmd import PendingBookingCommand
# from src.db.PaymentRepository import PaymentRepository  
# import uuid

# @pytest.fixture
# def mock_logger():
#     return MagicMock()

# @pytest.fixture
# def booking_id():
#     return 1

# @pytest.fixture
# def mock_booking():
#     booking = MagicMock()
#     booking.BookingId = 1
#     booking.UserId = str(uuid.uuid4())  # Booker/Passenger ID
#     booking.FeeMargin = 0.1  # 10% fee
#     booking_status = MagicMock()
#     booking_status.Status = "PrePending"
#     booking.BookingStatus_ = booking_status
#     journey = MagicMock()
#     journey.UserId = str(uuid.uuid4())  # Driver ID
#     journey.AdvertisedPrice = 100.0
#     journey.CurrencyCode = "USD"
#     booking.Journey_ = journey
#     return booking

# @pytest.fixture
# def mock_driver():
#     driver = MagicMock()
#     driver.UserId = str(uuid.uuid4())
#     return driver

# @pytest.fixture
# def mock_booker():
#     booker = MagicMock()
#     booker.UserId = str(uuid.uuid4())
#     booker.NonPending = 150.0  # Sufficient balance
#     return booker

# @pytest.fixture
# def mock_driver_balance():
#     balance = MagicMock(spec=UserBalance)
#     balance.NonPending = 50.0
#     balance.Pending = 25.0
#     return balance

# @pytest.fixture
# def mock_booker_balance():
#     balance = MagicMock(spec=UserBalance)
#     balance.NonPending = 150.0
#     balance.Pending = 0.0
#     return balance

# @pytest.fixture
# def pending_booking_command(mock_logger, booking_id):
#     command = PendingBookingCommand(mock_logger, booking_id)
#     command.PaymentRepository = MagicMock(spec=PaymentRepository)
#     return command

# def test_pending_booking_success(pending_booking_command, mock_booking, mock_driver, mock_booker, mock_driver_balance, mock_booker_balance):
#     # Arrange
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
#     pending_booking_command.PaymentRepository.GetUser.side_effect = [mock_driver, mock_booker]
#     pending_booking_command.PaymentRepository.GetUserBalance.side_effect = [mock_driver_balance, mock_booker_balance]
#     pending_booking_command.PaymentRepository.UpdatePendingBalance.return_value = True
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "success"
#     pending_booking_command.PaymentRepository.GetBookingById.assert_called_once_with(pending_booking_command.BookingId)
#     pending_booking_command.PaymentRepository.GetUser.assert_any_call(mock_booking.Journey_.UserId)
#     pending_booking_command.PaymentRepository.GetUser.assert_any_call(mock_booking.UserId)
#     pending_booking_command.PaymentRepository.GetUserBalance.assert_any_call(mock_driver.UserId)
#     pending_booking_command.PaymentRepository.GetUserBalance.assert_any_call(mock_booker.UserId)
    
#     # Calculate expected price and margin
#     expected_margin = round(mock_booking.FeeMargin * mock_booking.Journey_.AdvertisedPrice, 2)
#     expected_price = mock_booking.Journey_.AdvertisedPrice - expected_margin
    
#     pending_booking_command.PaymentRepository.UpdatePendingBalance.assert_called_once_with(mock_driver.UserId, expected_price)
#     pending_booking_command.PaymentRepository.CreateTransaction.assert_called_once()
#     # Verify transaction was created with correct values
#     created_transaction = pending_booking_command.PaymentRepository.CreateTransaction.call_args[0][0]
#     assert created_transaction.UserId == mock_driver.UserId
#     assert created_transaction.BookingId == pending_booking_command.BookingId
#     assert created_transaction.Value == expected_price
#     assert created_transaction.CurrencyCode == mock_booking.Journey_.CurrencyCode
#     assert created_transaction.TransactionStatusId == 1
#     assert created_transaction.TransactionTypeId == 1

# def test_pending_booking_not_found(pending_booking_command):
#     # Arrange
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = None
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Booking not found"
#     pending_booking_command.logger.error.assert_called_once()
#     assert "Error in Pending Booking" in pending_booking_command.logger.error.call_args[0][0]

# def test_pending_booking_incorrect_status(pending_booking_command, mock_booking):
#     # Arrange
#     mock_booking.BookingStatus_.Status = "Confirmed"  # Not in PrePending state
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Not a pending booking"
#     pending_booking_command.logger.error.assert_called_once()

# def test_pending_booking_driver_not_found(pending_booking_command, mock_booking):
#     # Arrange
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
#     pending_booking_command.PaymentRepository.GetUser.side_effect = [None, MagicMock()]  # Driver not found
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Driver not found"
#     pending_booking_command.logger.error.assert_called_once()

# def test_pending_booking_passenger_not_found(pending_booking_command, mock_booking, mock_driver):
#     # Arrange
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
#     pending_booking_command.PaymentRepository.GetUser.side_effect = [mock_driver, None]  # Passenger not found
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Passenger not found"
#     pending_booking_command.logger.error.assert_called_once()

# def test_pending_booking_create_driver_balance(pending_booking_command, mock_booking, mock_driver, mock_booker, mock_booker_balance):
#     # Arrange
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
#     pending_booking_command.PaymentRepository.GetUser.side_effect = [mock_driver, mock_booker]
#     pending_booking_command.PaymentRepository.GetUserBalance.side_effect = [None, mock_booker_balance, MagicMock(spec=UserBalance)]
#     pending_booking_command.PaymentRepository.UpdatePendingBalance.return_value = True
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "success"
#     pending_booking_command.PaymentRepository.CreateUserBalance.assert_called_once()
#     created_balance = pending_booking_command.PaymentRepository.CreateUserBalance.call_args[0][0]
#     assert created_balance.UserId == mock_driver.UserId
#     assert pending_booking_command.PaymentRepository.GetUserBalance.call_count == 3  # Initial check + check after creation

# def test_pending_booking_create_booker_balance(pending_booking_command, mock_booking, mock_driver, mock_booker, mock_driver_balance):
#     # Arrange
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
#     pending_booking_command.PaymentRepository.GetUser.side_effect = [mock_driver, mock_booker]
#     pending_booking_command.PaymentRepository.GetUserBalance.side_effect = [mock_driver_balance, None, MagicMock(spec=UserBalance)]
#     pending_booking_command.PaymentRepository.UpdatePendingBalance.return_value = True
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "success"
#     pending_booking_command.PaymentRepository.CreateUserBalance.assert_called_once()
#     created_balance = pending_booking_command.PaymentRepository.CreateUserBalance.call_args[0][0]
#     assert created_balance.UserId == mock_booker.UserId
#     assert pending_booking_command.PaymentRepository.GetUserBalance.call_count == 3  # Initial check + check after creation

# def test_pending_booking_insufficient_balance(pending_booking_command, mock_booking, mock_driver, mock_booker, mock_driver_balance, mock_booker_balance):
#     # Arrange
#     mock_booker.NonPending = 50.0  # Insufficient balance (less than AdvertisedPrice of 100.0)
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
#     pending_booking_command.PaymentRepository.GetUser.side_effect = [mock_driver, mock_booker]
#     pending_booking_command.PaymentRepository.GetUserBalance.side_effect = [mock_driver_balance, mock_booker_balance]
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Not enough user balance to set journey to pending"
#     pending_booking_command.logger.error.assert_called_once()
#     pending_booking_command.PaymentRepository.UpdatePendingBalance.assert_not_called()
#     pending_booking_command.PaymentRepository.CreateTransaction.assert_not_called()

# def test_pending_booking_update_pending_exception(pending_booking_command, mock_booking, mock_driver, mock_booker, mock_driver_balance, mock_booker_balance):
#     # Arrange
#     pending_booking_command.PaymentRepository.GetBookingById.return_value = mock_booking
#     pending_booking_command.PaymentRepository.GetUser.side_effect = [mock_driver, mock_booker]
#     pending_booking_command.PaymentRepository.GetUserBalance.side_effect = [mock_driver_balance, mock_booker_balance]
#     pending_booking_command.PaymentRepository.UpdatePendingBalance.side_effect = Exception("Database error")
    
#     # Act
#     result = pending_booking_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Database error"
#     pending_booking_command.logger.error.assert_called_once()
#     pending_booking_command.PaymentRepository.CreateTransaction.assert_not_called()

# def test_pending_booking_constructor():
#     # Arrange
#     logger = MagicMock()
#     booking_id = 1
    
#     # Act
#     command = PendingBookingCommand(logger, booking_id)
    
#     # Assert
#     assert command.logger == logger
#     assert command.BookingId == booking_id
#     assert isinstance(command.PaymentRepository, PaymentRepository)
