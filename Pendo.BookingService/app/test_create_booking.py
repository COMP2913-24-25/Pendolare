import pytest
from unittest.mock import MagicMock
from .create_booking import CreateBookingCommand

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
    mock.GetJourney.return_value = MagicMock(JourneyId=2)
    mock.GetExistingBooking.return_value = None
    return mock

@pytest.fixture
def create_booking_command(mock_repository, mock_email_sender, mock_logger):
    class DummyRequest:
        UserId = 1
        JourneyId = 2

    cmd = CreateBookingCommand(DummyRequest(), mock_email_sender, mock_logger)
    cmd.booking_repository = mock_repository
    return cmd

def test_create_booking_success(create_booking_command, mock_repository, mock_email_sender, mock_logger):
    result = create_booking_command.Execute()
    assert result["Status"] == "Success"
    mock_repository.CreateBooking.assert_called_once()
    mock_email_sender.SendBookingPending.assert_called_once()
    mock_logger.debug.assert_any_call("Booking pending email sent successfully.")

def test_create_booking_user_not_found(create_booking_command, mock_repository):
    mock_repository.GetUser.return_value = None
    result = create_booking_command.Execute()
    assert result["Status"] == "Failed"
    assert "User not found" in result["Error"]

def test_create_booking_journey_not_found(create_booking_command, mock_repository):
    mock_repository.GetJourney.return_value = None
    result = create_booking_command.Execute()
    assert result["Status"] == "Failed"
    assert "Journey not found" in result["Error"]

def test_create_booking_already_exists(create_booking_command, mock_repository):
    mock_repository.GetExistingBooking.return_value = MagicMock(BookingId=10)
    result = create_booking_command.Execute()
    assert result["Status"] == "Failed"
    assert "Booking already exists" in result["Error"]