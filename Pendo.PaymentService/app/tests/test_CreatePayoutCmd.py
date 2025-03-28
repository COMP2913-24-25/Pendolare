import pytest
from unittest.mock import Mock, MagicMock, patch
from src.db.PendoDatabase import UserBalance, Transaction
from src.db.PaymentRepository import PaymentRepository
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
def mock_mail_sender():
    mail_sender = MagicMock()
    mail_sender.SendPayoutEmail.return_value = None
    return mail_sender

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
def create_payout_command(mock_logger, user_id, mock_sendgrid_config, mock_mail_sender):
    # Use patch to mock the dependencies
    with patch('src.endpoints.CreatePayoutCmd.PaymentRepository') as MockRepo, \
         patch('src.endpoints.CreatePayoutCmd.MailSender', return_value=mock_mail_sender):
        
        # Create a real PaymentRepository mock with specific return values
        mock_repo = MockRepo.return_value
        mock_repo.GetUser.return_value = MagicMock(UserId=user_id, Email="test@example.com")
        mock_repo.GetUserBalance.return_value = MagicMock(NonPending=100.00)
        mock_repo.GetAdminUsers.return_value = [MagicMock(Email="admin@example.com")]
        mock_repo.CreateTransaction.return_value = None
        mock_repo.UpdateNonPendingBalance.return_value = None

        command = CreatePayoutCommand(mock_logger, user_id, mock_sendgrid_config)
        return command

def test_create_payout_success(create_payout_command):
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "success", f"Unexpected result: {result.__dict__}"
    
    # Verify method calls
    create_payout_command.PaymentRepository.GetUser.assert_called_once()
    create_payout_command.PaymentRepository.GetUserBalance.assert_called_once()
    create_payout_command.PaymentRepository.UpdateNonPendingBalance.assert_called_once()
    create_payout_command.PaymentRepository.CreateTransaction.assert_called_once()

def test_create_payout_user_not_found(create_payout_command):
    # Arrange
    create_payout_command.PaymentRepository.GetUser.return_value = None
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "fail"
    assert "User not found" in str(result.Error)

def test_create_payout_no_balance_sheet(create_payout_command):
    # Arrange
    create_payout_command.PaymentRepository.GetUserBalance.return_value = None
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    create_payout_command.PaymentRepository.CreateUserBalance.assert_called_once()

def test_create_payout_email_sending(create_payout_command):
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "success"
    
    # Verify email sending
    assert create_payout_command.logger.info.call_count >= 2

def test_create_payout_transaction_creation(create_payout_command):
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "success"
    
    # Verify transaction creation
    transaction_args = create_payout_command.PaymentRepository.CreateTransaction.call_args[0][0]
    assert transaction_args is not None

def test_create_payout_database_error(create_payout_command):
    # Arrange
    create_payout_command.PaymentRepository.UpdateNonPendingBalance.side_effect = Exception("Database error")
    
    # Act
    result = create_payout_command.Execute()
    
    # Assert
    assert result.Status == "fail"
    assert "Database error" in str(result.Error)

def test_create_payout_constructor():
    # Arrange
    logger = MagicMock()
    user_id = str(uuid.uuid4())
    sendgrid_config = MagicMock()
    
    # Act
    with patch('src.endpoints.CreatePayoutCmd.PaymentRepository'), \
         patch('src.endpoints.CreatePayoutCmd.MailSender'):
        command = CreatePayoutCommand(logger, user_id, sendgrid_config)
    
    # Assert
    assert command.logger == logger
    assert command.UserId == user_id
    assert command.sendGridConfig == sendgrid_config