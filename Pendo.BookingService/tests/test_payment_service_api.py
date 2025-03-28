import pytest
from uuid import uuid4
from unittest.mock import MagicMock
from app.payment_service_api import PaymentServiceClient
import requests

class DummyResponse:
    def __init__(self, json_data):
        self._json = json_data
    def json(self):
        return self._json

@pytest.fixture
def payment_service_configuration():
    return MagicMock(paymentServiceUrl="http://dummy-payment-service")

@pytest.fixture
def dummy_logger():
    return MagicMock()

@pytest.fixture
def payment_service_client(payment_service_configuration, dummy_logger):
    return PaymentServiceClient(payment_service_configuration, dummy_logger)

@pytest.fixture
def dummy_booking_id():
    return uuid4()

@pytest.fixture
def fake_post(monkeypatch):
    def _fake_post(response_json):
        def _inner(url, json):
            return DummyResponse(response_json)
        monkeypatch.setattr(requests, "post", _inner)
    return _fake_post

def test_pending_booking_request_success(fake_post, payment_service_client, dummy_booking_id):
    fake_post({"Status": "Success", "Error": ""})
    result = payment_service_client.PendingBookingRequest(dummy_booking_id, 32)
    assert result is True

def test_completed_booking_request_success(fake_post, payment_service_client, dummy_booking_id):
    fake_post({"Status": "Success", "Error": ""})
    result = payment_service_client.CompletedBookingRequest(dummy_booking_id, 32)
    assert result is True

def test_completed_booking_request_error(fake_post, payment_service_client, dummy_booking_id):
    fake_post({"Status": "Error", "Error": "Some error occurred"})
    with pytest.raises(Exception) as excinfo:
        payment_service_client.CompletedBookingRequest(dummy_booking_id, 32)
    assert "Payment service returned an error" in str(excinfo.value)

def test_refund_request_success(fake_post, payment_service_client, dummy_booking_id):
    fake_post({"Status": "Success", "Error": ""})
    result = payment_service_client.RefundRequest(1, dummy_booking_id, "2025-03-12T12:00:00", "2025-03-12T12:01:00", 100)
    assert result is True

def test_refund_request_insufficient_balance(fake_post, payment_service_client, dummy_booking_id):
    fake_post({"Status": "Success", "Error": "Not enough user balance to set journey to pending"})
    result = payment_service_client.RefundRequest(1, dummy_booking_id, "2025-03-12T12:00:00", "2025-03-12T12:01:00", 100)
    assert result is False
