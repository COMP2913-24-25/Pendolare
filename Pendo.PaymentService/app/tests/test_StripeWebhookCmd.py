# import pytest
# from unittest.mock import MagicMock, patch
# from src.db.PendoDatabase import UserBalance
# from src.returns.PaymentReturns import StatusResponse
# import uuid

# @pytest.fixture
# def mock_logger():
#     return MagicMock()

# @pytest.fixture
# def user_id():
#     return str(uuid.uuid4())

# @pytest.fixture
# def amount():
#     return 100.00

# @pytest.fixture
# def mock_user():
#     user = MagicMock()
#     user.UserId = str(uuid.uuid4())
#     return user

# @pytest.fixture
# def mock_transaction():
#     transaction = MagicMock()
#     transaction.TransactionId = str(uuid.uuid4())
#     return transaction

# @pytest.fixture
# def stripe_webhook_command(mock_logger, user_id, amount):
#     # Use patch to mock the PaymentRepository class
#     with patch('src.endpoints.StripeWebhookCmd.PaymentRepository') as MockRepo:
#         MockRepo.return_value = MagicMock()

#         from src.endpoints.StripeWebhookCmd import StripeWebhookCommand
#         command = StripeWebhookCommand(mock_logger, user_id, amount)
#         yield command

# def test_webhook_success(stripe_webhook_command, mock_user, mock_transaction, user_id, amount):
#     # Arrange
#     stripe_webhook_command.PaymentRepository.GetUser.return_value = mock_user
#     stripe_webhook_command.PaymentRepository.GetUserBalance.return_value = MagicMock(spec=UserBalance)
#     stripe_webhook_command.PaymentRepository.GetTransaction.return_value = mock_transaction
    
#     # Act
#     result = stripe_webhook_command.Execute()
    
#     # Assert
#     assert result.Status == "success"
#     stripe_webhook_command.PaymentRepository.GetUser.assert_called_once_with(user_id)
#     stripe_webhook_command.PaymentRepository.GetUserBalance.assert_called_once_with(user_id)
#     stripe_webhook_command.PaymentRepository.GetTransaction.assert_called_once_with(user_id, amount, 3, 5)
#     stripe_webhook_command.PaymentRepository.UpdateTransaction.assert_called_once_with(
#         mock_transaction.TransactionId, amount, 5, 5
#     )
#     stripe_webhook_command.PaymentRepository.UpdateNonPendingBalance.assert_called_once_with(user_id, amount)

# def test_webhook_user_not_found(stripe_webhook_command, user_id):
#     # Arrange
#     stripe_webhook_command.PaymentRepository.GetUser.return_value = None
    
#     # Act
#     result = stripe_webhook_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "User not found"
#     stripe_webhook_command.PaymentRepository.GetUser.assert_called_once_with(user_id)
#     stripe_webhook_command.logger.error.assert_called_once()

# def test_webhook_no_user_balance(stripe_webhook_command, mock_user, mock_transaction, user_id, amount):
#     # Arrange
#     stripe_webhook_command.PaymentRepository.GetUser.return_value = mock_user
#     stripe_webhook_command.PaymentRepository.GetUserBalance.return_value = None
#     stripe_webhook_command.PaymentRepository.GetTransaction.return_value = mock_transaction
    
#     # Act
#     result = stripe_webhook_command.Execute()
    
#     # Assert
#     assert result.Status == "success"
#     stripe_webhook_command.PaymentRepository.CreateUserBalance.assert_called_once()
#     assert stripe_webhook_command.PaymentRepository.CreateUserBalance.call_args[0][0].UserId == user_id
    
#     # Verify the flow continues after creating the user balance
#     stripe_webhook_command.PaymentRepository.UpdateTransaction.assert_called_once()
#     stripe_webhook_command.PaymentRepository.UpdateNonPendingBalance.assert_called_once()

# def test_webhook_transaction_not_found(stripe_webhook_command, mock_user, user_id, amount):
#     # Arrange
#     stripe_webhook_command.PaymentRepository.GetUser.return_value = mock_user
#     stripe_webhook_command.PaymentRepository.GetUserBalance.return_value = MagicMock(spec=UserBalance)
#     stripe_webhook_command.PaymentRepository.GetTransaction.return_value = None
    
#     # Act
#     result = stripe_webhook_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Transaction not found"
#     stripe_webhook_command.PaymentRepository.GetTransaction.assert_called_once_with(user_id, amount, 3, 5)
#     stripe_webhook_command.logger.error.assert_called_once()
    
#     # Verify that update methods were not called
#     stripe_webhook_command.PaymentRepository.UpdateTransaction.assert_not_called()
#     stripe_webhook_command.PaymentRepository.UpdateNonPendingBalance.assert_not_called()

# def test_webhook_update_failure(stripe_webhook_command, mock_user, mock_transaction, user_id, amount):
#     # Arrange
#     stripe_webhook_command.PaymentRepository.GetUser.return_value = mock_user
#     stripe_webhook_command.PaymentRepository.GetUserBalance.return_value = MagicMock(spec=UserBalance)
#     stripe_webhook_command.PaymentRepository.GetTransaction.return_value = mock_transaction
#     stripe_webhook_command.PaymentRepository.UpdateTransaction.side_effect = Exception("Database error")
    
#     # Act
#     result = stripe_webhook_command.Execute()
    
#     # Assert
#     assert result.Status == "fail"
#     assert result.Error == "Database error"
#     stripe_webhook_command.logger.error.assert_called_once()
    
#     # Verify update was attempted
#     stripe_webhook_command.PaymentRepository.UpdateTransaction.assert_called_once()
#     # Verify balance was not updated after the transaction update failed
#     stripe_webhook_command.PaymentRepository.UpdateNonPendingBalance.assert_not_called()

# # Modified to use patching instead of directly checking instance type
# def test_webhook_constructor():
#     # Arrange
#     logger = MagicMock()
#     user_id = str(uuid.uuid4())
#     amount = 50.0
    
#     # Act - Use patch to mock the PaymentRepository
#     with patch('src.endpoints.StripeWebhookCmd.PaymentRepository') as MockRepo:
#         # Mock the repository class
#         mock_repo_instance = MagicMock()
#         MockRepo.return_value = mock_repo_instance
        
#         from src.endpoints.StripeWebhookCmd import StripeWebhookCommand
#         command = StripeWebhookCommand(logger, user_id, amount)
        
#         # Assert
#         assert command.logger == logger
#         assert command.UserId == user_id
#         assert command.Amount == amount
#         # Verify the repository was instantiated
#         MockRepo.assert_called_once()
#         assert command.PaymentRepository == mock_repo_instance

# @patch('uuid.uuid4')
# def test_webhook_complete_flow_with_new_balance(mock_uuid, stripe_webhook_command, mock_user, mock_transaction, user_id, amount):
#     # Arrange
#     mock_uuid.return_value = "test-uuid"
#     stripe_webhook_command.PaymentRepository.GetUser.return_value = mock_user
#     stripe_webhook_command.PaymentRepository.GetUserBalance.return_value = None
#     stripe_webhook_command.PaymentRepository.GetTransaction.return_value = mock_transaction
    
#     # Act
#     result = stripe_webhook_command.Execute()
    
#     # Assert
#     assert result.Status == "success"
    
#     # Verify the flow of operations is correct
#     expected_calls = [
#         stripe_webhook_command.PaymentRepository.GetUser,
#         stripe_webhook_command.logger.info,
#         stripe_webhook_command.PaymentRepository.GetUserBalance,
#         stripe_webhook_command.PaymentRepository.CreateUserBalance,
#         stripe_webhook_command.PaymentRepository.GetTransaction,
#         stripe_webhook_command.PaymentRepository.UpdateTransaction,
#         stripe_webhook_command.PaymentRepository.UpdateNonPendingBalance
#     ]
    
#     # Rough verification of method call order
#     for i, call in enumerate(expected_calls[:-1]):
#         assert call.call_count > 0, f"Method at index {i} was not called"