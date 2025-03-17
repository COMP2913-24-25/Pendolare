import pytest
from unittest.mock import MagicMock
from src.returns.PaymentReturns import StatusResponse
from src.db.PendoDatabase import UserBalance
from src.endpoints.StripeWebhookCmd import StripeWebhookCommand

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_payment_repository():
    repo = MagicMock()
    # Set up default returns for repository methods
    user = MagicMock()
    user.UserId = "user123"
    repo.GetUser.return_value = user
    
    balance = MagicMock()
    balance.UserId = "user123"
    balance.NonPending = 100.0
    balance.Pending = 50.0
    repo.GetUserBalance.return_value = balance
    
    transaction = MagicMock()
    transaction.TransactionId = "trans123"
    transaction.UserId = "user123"
    transaction.Value = 25.0
    repo.GetTransaction.return_value = transaction
    
    return repo

@pytest.fixture
def stripe_webhook_command(mock_logger, mock_payment_repository):
    cmd = StripeWebhookCommand(mock_logger, "user123", 25.0)
    cmd.PaymentRepository = mock_payment_repository
    return cmd

def test_execute_success(stripe_webhook_command, mock_payment_repository, mock_logger):
    result = stripe_webhook_command.Execute()
    
    assert isinstance(result, StatusResponse)
    assert result.Status == "success"
    mock_payment_repository.UpdateTransaction.assert_called_once_with("trans123", 25.0, 5, 5)
    mock_payment_repository.UpdateNonPendingBalance.assert_called_once_with("user123", 25.0)
    mock_logger.info.assert_called_with("Got user", mock_payment_repository.GetUser.return_value)

def test_execute_user_not_found(stripe_webhook_command, mock_payment_repository):
    mock_payment_repository.GetUser.return_value = None
    
    result = stripe_webhook_command.Execute()
    
    assert isinstance(result, StatusResponse)
    assert result.Status == "fail"
    assert "User not found" in result.Error
    mock_payment_repository.UpdateTransaction.assert_not_called()
    mock_payment_repository.UpdateNonPendingBalance.assert_not_called()

def test_execute_create_user_balance_if_none(stripe_webhook_command, mock_payment_repository):
    mock_payment_repository.GetUserBalance.return_value = None
    
    result = stripe_webhook_command.Execute()
    
    assert result.Status == "success"
    mock_payment_repository.CreateUserBalance.assert_called_once()
    
    # Verify the created UserBalance has the correct UserId
    created_balance = mock_payment_repository.CreateUserBalance.call_args[0][0]
    assert isinstance(created_balance, UserBalance)
    assert created_balance.UserId == "user123"

def test_execute_transaction_not_found(stripe_webhook_command, mock_payment_repository):
    mock_payment_repository.GetTransaction.return_value = None
    
    result = stripe_webhook_command.Execute()
    
    assert result.Status == "fail"
    assert "Transaction not found" in result.Error
    mock_payment_repository.UpdateTransaction.assert_not_called()
    mock_payment_repository.UpdateNonPendingBalance.assert_not_called()

def test_execute_exception_handling(stripe_webhook_command, mock_payment_repository, mock_logger):
    mock_payment_repository.GetUser.side_effect = Exception("Test exception")
    
    result = stripe_webhook_command.Execute()
    
    assert result.Status == "fail"
    assert "Test exception" in result.Error
    mock_logger.error.assert_called_once()
    assert "Error fetching balance sheet" in mock_logger.error.call_args[0][0]