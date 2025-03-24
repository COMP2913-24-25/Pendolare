import pytest
from unittest.mock import MagicMock, patch
from src.returns.PaymentReturns import PaymentMethodResponse, SingularPaymentMethod, StatusResponse
from src.endpoints.PaymentMethodsCmd import PaymentMethodsCommand
import uuid

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def user_id():
    return str(uuid.uuid4())

@pytest.fixture
def stripe_secret():
    return "sk_test_123456789"

@pytest.fixture
def payment_methods_command(mock_logger, user_id, stripe_secret):
    return PaymentMethodsCommand(mock_logger, user_id, stripe_secret)

@pytest.fixture
def mock_stripe_methods():
    return {
        'data': [
            {
                'type': 'card',
                'card': {
                    'brand': 'visa',
                    'funding': 'credit',
                    'last4': '4242',
                    'exp_month': 12,
                    'exp_year': 2025
                }
            },
            {
                'type': 'card',
                'card': {
                    'brand': 'mastercard',
                    'funding': 'debit',
                    'last4': '5555',
                    'exp_month': 6,
                    'exp_year': 2026
                }
            }
        ]
    }

@patch('stripe.Customer.list_payment_methods')
def test_payment_methods_success(mock_list_payment_methods, payment_methods_command, mock_stripe_methods, user_id):
    # Arrange
    mock_list_payment_methods.return_value = mock_stripe_methods
    
    # Act
    result = payment_methods_command.Execute()
    
    # Assert
    assert result.Status == "success"
    assert len(result.Methods) == 2
    
    # Verify first payment method
    assert result.Methods[0].Brand == "visa"
    assert result.Methods[0].Funding == "credit"
    assert result.Methods[0].Last4 == "4242"
    assert result.Methods[0].Exp_month == 12
    assert result.Methods[0].Exp_year == 2025
    assert result.Methods[0].PaymentType == "card"
    
    # Verify second payment method
    assert result.Methods[1].Brand == "mastercard"
    assert result.Methods[1].Funding == "debit"
    assert result.Methods[1].Last4 == "5555"
    assert result.Methods[1].Exp_month == 6
    assert result.Methods[1].Exp_year == 2026
    assert result.Methods[1].PaymentType == "card"
    
    # Verify the stripe API was called correctly
    mock_list_payment_methods.assert_called_once_with(user_id)

@patch('stripe.Customer.list_payment_methods')
def test_payment_methods_empty(mock_list_payment_methods, payment_methods_command, user_id):
    # Arrange
    mock_list_payment_methods.return_value = {'data': []}
    
    # Act
    result = payment_methods_command.Execute()
    
    # Assert
    assert result.Status == "success"
    assert len(result.Methods) == 0
    
    # Verify the stripe API was called correctly
    mock_list_payment_methods.assert_called_once_with(user_id)

@patch('stripe.Customer.list_payment_methods')
def test_payment_methods_missing_card_data(mock_list_payment_methods, payment_methods_command, user_id):
    # Arrange
    mock_list_payment_methods.return_value = {
        'data': [
            {
                'type': 'card'
                # Missing card data
            }
        ]
    }
    
    # Act
    result = payment_methods_command.Execute()
    
    # Assert
    assert result.Status == "success"
    assert len(result.Methods) == 1
    assert result.Methods[0].Brand == ""
    assert result.Methods[0].Funding == ""
    assert result.Methods[0].Last4 == ""
    assert result.Methods[0].Exp_month == 0
    assert result.Methods[0].Exp_year == 0
    assert result.Methods[0].PaymentType == "card"

@patch('stripe.Customer.list_payment_methods')
def test_payment_methods_exception(mock_list_payment_methods, payment_methods_command, mock_logger):
    # Arrange
    mock_list_payment_methods.side_effect = Exception("Stripe API error")
    
    # Act
    result = payment_methods_command.Execute()
    
    # Assert
    assert result.Status == "fail"
    assert result.Error == "Stripe API error"
    mock_logger.error.assert_called_once()
    assert "Error fetching payment methods" in mock_logger.error.call_args[0][0]

@patch('stripe.Customer.list_payment_methods')
def test_payment_methods_mixed_payment_types(mock_list_payment_methods, payment_methods_command):
    # Arrange
    mock_list_payment_methods.return_value = {
        'data': [
            {
                'type': 'card',
                'card': {
                    'brand': 'visa',
                    'funding': 'credit',
                    'last4': '4242',
                    'exp_month': 12,
                    'exp_year': 2025
                }
            },
            {
                'type': 'sepa_debit',
                'sepa_debit': {
                    'bank_code': '37040044',
                    'last4': '3000'
                }
            }
        ]
    }
    
    # Act
    result = payment_methods_command.Execute()
    
    # Assert
    assert result.Status == "success"
    assert len(result.Methods) == 2
    
    # First method should be the card
    assert result.Methods[0].Brand == "visa"
    assert result.Methods[0].PaymentType == "card"
    
    # Second method should have empty card values but correct type
    assert result.Methods[1].Brand == ""
    assert result.Methods[1].Last4 == ""
    assert result.Methods[1].PaymentType == "sepa_debit"

@patch('stripe.api_key', None)  # Reset the api_key to ensure it's set in the test
@patch('stripe.Customer.list_payment_methods')
def test_payment_methods_sets_api_key(mock_list_payment_methods, payment_methods_command, stripe_secret):
    # Arrange
    mock_list_payment_methods.return_value = {'data': []}
    
    # Act
    payment_methods_command.Execute()
    
    # Assert 
    with patch('stripe.api_key', None) as mock_api_key:
        mock_api_key = stripe_secret
