import pytest
from unittest.mock import MagicMock, patch
from src.returns.PaymentReturns import SingularPaymentMethod, PaymentMethodResponse, StatusResponse
from src.endpoints.PaymentMethodsCmd import PaymentMethodsCommand

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_secret():
    return MagicMock()

@pytest.fixture
def mock_stripe_customer():
    with patch('src.endpoints.PaymentMethodsCmd.stripe') as mock_stripe:
        mock_stripe.api_key = None
        mock_payment_methods = {
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
                        'exp_month': 10,
                        'exp_year': 2024
                    }
                }
            ]
        }
        mock_stripe.Customer.list_payment_methods.return_value = mock_payment_methods
        yield mock_stripe

@pytest.fixture
def payment_methods_command(mock_logger, mock_secret, mock_stripe_customer):
    return PaymentMethodsCommand(mock_logger, "user123", mock_secret)

def test_execute_success(payment_methods_command, mock_stripe_customer):
    result = payment_methods_command.Execute()
    
    # Verify stripe customer methods were requested
    mock_stripe_customer.Customer.list_payment_methods.assert_called_once_with("user123")
    
    # Verify result structure
    assert isinstance(result, PaymentMethodResponse)
    assert result.Status == "success"
    assert len(result.Methods) == 2
    
    # Verify first payment method
    assert isinstance(result.Methods[0], SingularPaymentMethod)
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
    assert result.Methods[1].Exp_month == 10
    assert result.Methods[1].Exp_year == 2024

def test_execute_empty_payment_methods(payment_methods_command, mock_stripe_customer):
    # Set empty payment methods
    mock_stripe_customer.Customer.list_payment_methods.return_value = {'data': []}
    
    result = payment_methods_command.Execute()
    
    assert result.Status == "success"
    assert len(result.Methods) == 0

def test_execute_exception_handling(payment_methods_command, mock_stripe_customer, mock_logger):
    # Simulate exception
    mock_stripe_customer.Customer.list_payment_methods.side_effect = Exception("Test exception")
    
    result = payment_methods_command.Execute()
    
    assert isinstance(result, StatusResponse)
    assert result.Status == "fail"
    assert result.Error == "Test exception"
    mock_logger.error.assert_called_once()
    assert "Error fetching payment methods" in mock_logger.error.call_args[0][0]

def test_execute_handles_missing_card_data(payment_methods_command, mock_stripe_customer):
    # Payment method without card data
    mock_stripe_customer.Customer.list_payment_methods.return_value = {
        'data': [
            {
                'type': 'card'
                # No card data
            }
        ]
    }
    
    result = payment_methods_command.Execute()
    
    assert result.Status == "success"
    assert len(result.Methods) == 1
    assert result.Methods[0].Brand == ""
    assert result.Methods[0].Funding == ""
    assert result.Methods[0].Last4 == ""
    assert result.Methods[0].Exp_month == 0
    assert result.Methods[0].Exp_year == 0
    assert result.Methods[0].PaymentType == "card"