import pytest
from unittest.mock import Mock, MagicMock
from src.db.PendoDatabase import UserBalance, Transaction
from src.endpoints.CreatePayoutCmd import CreatePayoutCommand
from src.returns.PaymentReturns import StatusResponse
import uuid
import datetime

@pytest.fixture
def mock_logger():
    return Mock()

@pytest.fixture
def mock_sendgrid_config():
    return Mock()

@pytest.fixture
def user_id():
    return str(uuid.uuid4())

@pytest.fixture
def mock_user():
    user = MagicMock()
    user.UserId = str(uuid.uuid4())
    user.Email = "test@example.com"
    return user

@pytest.fixture
def mock_user_balance():
    balance = MagicMock(spec=UserBalance)
    balance.NonPending = 100.00
    balance.UserId = str(uuid.uuid4())
    return balance

@pytest.fixture
def create_payout_command(mock_logger, user_id, mock_sendgrid_config):
    # Use patch to mock the PaymentRepository class
    with pytest.mock.patch('src.endpoints.CreatePayoutCmd.PaymentRepository') as MockRepo:
        MockRepo.return_value = MagicMock()

        command = CreatePayoutCommand(mock_logger, user_id, mock_sendgrid_config)
        yield command

def test_create_payout_success(create_payout_command, mock_user, mock_user_balance):
    # Arrange
    create_payout_command.PaymentRepository.GetUser.return_value = mock_user
    create_payout_command.PaymentRepository.GetUserBalance.return_value = mock_user_balance
    create_payout_command.PaymentRepository.GetAdminUsers.return_value = [mock_user]
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "success"
    
    # Verify method calls
    create_payout_command.PaymentRepository.GetUser.assert_called_once_with(create_payout_command.UserId)
    create_payout_command.PaymentRepository.GetUserBalance.assert_called_once_with(mock_user.UserId)
    create_payout_command.PaymentRepository.UpdateNonPendingBalance.assert_called_once_with(
        mock_user.UserId, 
        -1 * mock_user_balance.NonPending
    )
    create_payout_command.PaymentRepository.CreateTransaction.assert_called_once()

def test_create_payout_user_not_found(create_payout_command):
    # Arrange
    create_payout_command.PaymentRepository.GetUser.return_value = None
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "fail"
    assert "User not found" in result.Error
    create_payout_command.logger.error.assert_called_once()

def test_create_payout_no_balance_sheet(create_payout_command, mock_user):
    # Arrange
    create_payout_command.PaymentRepository.GetUser.return_value = mock_user
    create_payout_command.PaymentRepository.GetUserBalance.return_value = None
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    create_payout_command.PaymentRepository.CreateUserBalance.assert_called_once()
    assert isinstance(create_payout_command.PaymentRepository.CreateUserBalance.call_args[0][0], UserBalance)
    assert create_payout_command.PaymentRepository.CreateUserBalance.call_args[0][0].UserId == mock_user.UserId

def test_create_payout_email_sending(create_payout_command, mock_user, mock_user_balance):
    # Arrange
    create_payout_command.PaymentRepository.GetUser.return_value = mock_user
    create_payout_command.PaymentRepository.GetUserBalance.return_value = mock_user_balance
    mock_admin = MagicMock()
    mock_admin.Email = "admin@example.com"
    create_payout_command.PaymentRepository.GetAdminUsers.return_value = [mock_admin]
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "success"
    
    # Verify email sending
    mailer = create_payout_command.logger.info.call_args_list
    assert any("Sent Payout email to user" in str(call) for call in mailer)
    assert any("Sent Payout email to admin" in str(call) for call in mailer)

def test_create_payout_transaction_creation(create_payout_command, mock_user, mock_user_balance):
    # Arrange
    create_payout_command.PaymentRepository.GetUser.return_value = mock_user
    create_payout_command.PaymentRepository.GetUserBalance.return_value = mock_user_balance
    create_payout_command.PaymentRepository.GetAdminUsers.return_value = [mock_user]
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    transaction_args = create_payout_command.PaymentRepository.CreateTransaction.call_args[0][0]
    assert isinstance(transaction_args, Transaction)
    assert transaction_args.UserId == mock_user.UserId
    assert transaction_args.Value == mock_user_balance.NonPending
    assert transaction_args.CurrencyCode == "GBP"
    assert transaction_args.TransactionStatusId == 1
    assert transaction_args.TransactionTypeId == 1

def test_create_payout_database_error(create_payout_command, mock_user, mock_user_balance):
    # Arrange
    create_payout_command.PaymentRepository.GetUser.return_value = mock_user
    create_payout_command.PaymentRepository.GetUserBalance.return_value = mock_user_balance
    create_payout_command.PaymentRepository.UpdateNonPendingBalance.side_effect = Exception("Database error")
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "fail"
    assert "Database error" in result.Error
    create_payout_command.logger.error.assert_called_once()

def test_create_payout_constructor():
    # Arrange
    logger = MagicMock()
    user_id = str(uuid.uuid4())
    sendgrid_config = MagicMock()
    
    # Act
    command = CreatePayoutCommand(logger, user_id, sendgrid_config)
    
    # Assert
    assert command.logger == logger
    assert command.UserId == user_id
    assert command.sendGridConfig == sendgrid_config
    assert isinstance(command.PaymentRepository, PaymentRepository)