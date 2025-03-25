import pytest
from unittest.mock import Mock, MagicMock
from src.endpoints.ViewBalanceCmd import ViewBalanceCommand
from src.db.PaymentRepository import UserBalance
import uuid

@pytest.fixture
def mock_request():
    request = MagicMock(UserId = uuid.uuid4())
    return request

@pytest.fixture
def mock_logger():
    return Mock()

@pytest.fixture
def mock_payment_repository():
    return Mock()

@pytest.fixture
def get_bookings_command(mock_request, mock_logger, mock_payment_repository):
    command = GetBookingsCommand(mock_request, mock_logger)
    command.Payment_Repository = mock_payment_repository
    return command


# from src.returns.PaymentReturns import ViewBalanceResponse, StatusResponse
# from src.endpoints.ViewBalanceCmd import ViewBalanceCommand
# import uuid

# @pytest.fixture
# def mock_logger():
#     return MagicMock()

# @pytest.fixture
# def user_id():
#     return str(uuid.uuid4())

# @pytest.fixture
# def mock_user():
#     user = MagicMock()
#     user.UserId = str(uuid.uuid4())
#     return user

# @pytest.fixture
# def mock_user_balance():
#     balance = MagicMock(spec=UserBalance)
#     balance.NonPending = 100.00
#     balance.Pending = 50.00
#     return balance

# @pytest.fixture
# def view_balance_command(mock_logger, user_id):
#     command = ViewBalanceCommand(mock_logger, user_id)
#     command.PaymentRepository = MagicMock(spec=PaymentRepository)
#     return command

# def test_view_balance_success(view_balance_command, mock_user, mock_user_balance, user_id):
#     # Arrange
#     view_balance_command.PaymentRepository.GetUser.return_value = mock_user
#     view_balance_command.PaymentRepository.GetUserBalance.return_value = mock_user_balance
    
#     # Act
#     result = view_balance_command.Execute()
    
#     # Assert
#     assert result.Status == "success"
#     assert result.NonPending == 100.00
#     assert result.Pending == 50.00
#     view_balance_command.PaymentRepository.GetUser.assert_called_once_with(user_id)
#     view_balance_command.PaymentRepository.GetUserBalance.assert_called_once_with(user_id)

# def test_view_balance_user_not_found(view_balance_command, user_id):
#     # Arrange
#     view_balance_command.PaymentRepository.GetUser.return_value = None
    
#     # Act
#     result = view_balance_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "User not found"
#     view_balance_command.PaymentRepository.GetUser.assert_called_once_with(user_id)
#     view_balance_command.logger.error.assert_called_once()
#     view_balance_command.PaymentRepository.GetUserBalance.assert_not_called()

# def test_view_balance_no_balance_sheet(view_balance_command, mock_user, user_id):
#     # Arrange
#     view_balance_command.PaymentRepository.GetUser.return_value = mock_user
#     view_balance_command.PaymentRepository.GetUserBalance.side_effect = [None, MagicMock(spec=UserBalance, NonPending=0.0, Pending=0.0)]
    
#     # Act
#     result = view_balance_command.Execute()
    
#     # Assert
#     assert result.Status == "success"
#     assert result.NonPending == 0.0
#     assert result.Pending == 0.0
#     view_balance_command.PaymentRepository.CreateUserBalance.assert_called_once()
#     # Check that UserBalance was created with the correct UserId
#     created_balance = view_balance_command.PaymentRepository.CreateUserBalance.call_args[0][0]
#     assert created_balance.UserId == user_id
#     # Verify GetUserBalance was called twice (before and after creating a new balance)
#     assert view_balance_command.PaymentRepository.GetUserBalance.call_count == 2

# def test_view_balance_repository_exception(view_balance_command, mock_user, user_id):
#     # Arrange
#     view_balance_command.PaymentRepository.GetUser.return_value = mock_user
#     view_balance_command.PaymentRepository.GetUserBalance.side_effect = Exception("Database error")
    
#     # Act
#     result = view_balance_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Database error"
#     view_balance_command.logger.error.assert_called_once()
#     assert "Error fetching balance sheet" in view_balance_command.logger.error.call_args[0][0]

# def test_view_balance_create_balance_failure(view_balance_command, mock_user, user_id):
#     # Arrange
#     view_balance_command.PaymentRepository.GetUser.return_value = mock_user
#     view_balance_command.PaymentRepository.GetUserBalance.return_value = None
#     view_balance_command.PaymentRepository.CreateUserBalance.side_effect = Exception("Failed to create balance")
    
#     # Act
#     result = view_balance_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Failed to create balance"
#     view_balance_command.logger.error.assert_called_once()

# def test_view_balance_constructor():
#     # Arrange
#     logger = MagicMock()
#     user_id = str(uuid.uuid4())
    
#     # Act
#     command = ViewBalanceCommand(logger, user_id)
    
#     # Assert
#     assert command.logger == logger
#     assert command.UserId == user_id
#     assert isinstance(command.PaymentRepository, PaymentRepository)

# def test_view_balance_get_balance_after_create_failure(view_balance_command, mock_user, user_id):
#     # Arrange
#     view_balance_command.PaymentRepository.GetUser.return_value = mock_user
#     view_balance_command.PaymentRepository.GetUserBalance.side_effect = [None, Exception("Failed to get balance after creation")]
    
#     # Act
#     result = view_balance_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Failed to get balance after creation"
#     view_balance_command.PaymentRepository.CreateUserBalance.assert_called_once()
#     assert view_balance_command.PaymentRepository.GetUserBalance.call_count == 2
#     view_balance_command.logger.error.assert_called_once()
