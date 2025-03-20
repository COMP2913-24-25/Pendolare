import pytest
from unittest.mock import MagicMock
from app.create_booking import CreateBookingCommand
from datetime import datetime, timedelta

@pytest.fixture
def mock_email_sender():
    return MagicMock()

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_repository():
    mock = MagicMock()
    mock.GetUser.return_value = MagicMock(UserId=1, Email="test@user.com")
    mock.GetJourney.return_value = MagicMock(JourneyId=2, JourneyType=1)
    mock.GetExistingBooking.return_value = None
    return mock

@pytest.fixture
def mock_dvla_client():
    return MagicMock()

@pytest.fixture
def mock_configuration_provider():
    mock = MagicMock()
    mock.GetSingleValue.return_value = "50.00"
    return mock

@pytest.fixture
def mock_payment_service_client():
    client = MagicMock()
    client.PendingBookingRequest.return_value = True
    return client

@pytest.fixture
def create_booking_command(mock_repository, mock_email_sender, mock_logger, mock_dvla_client, mock_configuration_provider, mock_payment_service_client):
    class DummyRequest:
        UserId = 1
        JourneyId = 2
        JourneyTime = datetime.now() + timedelta(days=1)
    class DummyResponse:
        def __init__(self):
            self.status_code = None
    cmd = CreateBookingCommand(DummyRequest(), DummyResponse(), mock_email_sender, mock_logger, mock_dvla_client, mock_configuration_provider, mock_payment_service_client)
    cmd.booking_repository = mock_repository
    return cmd

def test_create_booking_success(create_booking_command, mock_repository, mock_email_sender, mock_logger):
    result = create_booking_command.Execute()
    assert result.Status == "Success"
    mock_repository.CreateBooking.assert_called_once()
    mock_email_sender.SendBookingPending.assert_called_once()
    mock_logger.debug.assert_any_call("Booking pending email sent successfully.")

def test_create_booking_user_not_found(create_booking_command, mock_repository):
    mock_repository.GetUser.return_value = None
    result = create_booking_command.Execute()
    assert result.Status == "Failed"
    assert "User not found" in result.Message
    assert create_booking_command.response.status_code == 404

def test_create_booking_journey_not_found(create_booking_command, mock_repository):
    mock_repository.GetJourney.return_value = None
    result = create_booking_command.Execute()
    assert result.Status == "Failed"
    assert "Journey not found" in result.Message
    assert create_booking_command.response.status_code == 404

def test_create_booking_already_exists(create_booking_command, mock_repository):
    mock_repository.GetExistingBooking.return_value = MagicMock(BookingId=10)
    result = create_booking_command.Execute()
    assert result.Status == "Failed"
    assert "Booking for this time and journey combination already exists" in result.Message
    assert create_booking_command.response.status_code == 400

def test_create_booking_fee_margin_not_found(create_booking_command, mock_configuration_provider):
    mock_configuration_provider.GetSingleValue.return_value = None
    result = create_booking_command.Execute()
    assert result.Status == "Failed"
    assert "Booking fee margin not found" in result.Message
    assert create_booking_command.response.status_code == 404

def test_create_booking_invalid_commuter_time(create_booking_command, mock_repository, monkeypatch):
    mock_repository.GetJourney.return_value = MagicMock(JourneyId=2, JourneyType=2, Recurrance="weekly", VehicleRegistration="XYZ")
    monkeypatch.setattr("app.create_booking.checkTimeValid", lambda r, t: False)
    result = create_booking_command.Execute()
    assert result.Status == "Failed"
    assert "Booking time is not valid for the commuter journey" in result.Message
    assert create_booking_command.response.status_code == 400