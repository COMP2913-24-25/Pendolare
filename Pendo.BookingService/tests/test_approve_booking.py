import pytest
from unittest.mock import MagicMock
from app.approve_booking import ApproveBookingCommand

class DummyRequest:
    BookingId = 1

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.GetBooking.return_value = MagicMock(BookingId=1, UserId=1, JourneyId=1)
    repo.GetUser.side_effect = lambda user_id: MagicMock(UserId=user_id, Email=f"user{user_id}@example.com")
    repo.GetJourney.return_value = MagicMock(JourneyId=1, UserId=2, VehicleRegistration="ABC123")
    repo.GetBookingAmmendments.return_value = []
    return repo

@pytest.fixture
def mock_email_sender():
    return MagicMock()

@pytest.fixture
def mock_dvla_client():
    client = MagicMock()
    client.GetVehicleDetails.return_value = {"Make": "Test", "Model": "Car"}
    return client

@pytest.fixture
def approve_booking_command(mock_repository, mock_logger, mock_email_sender, mock_dvla_client):
    cmd = ApproveBookingCommand(1, DummyRequest(), mock_logger, mock_email_sender, mock_dvla_client)
    cmd.booking_repository = mock_repository
    return cmd

def test_approve_booking_success(approve_booking_command, mock_repository, mock_logger, mock_email_sender):
    result = approve_booking_command.Execute()
    assert result["Status"] == "Success"
    mock_repository.UpdateBookingStatus.assert_called_once_with(1, 2)
    mock_email_sender.SendBookingConfirmation.assert_called_once()
    mock_logger.debug.assert_any_call(f"Booking 1 approved successfully.")

def test_approve_booking_with_ammendments(approve_booking_command, mock_repository, mock_logger):
    mock_repository.GetBookingAmmendments.return_value = [MagicMock()]
    result = approve_booking_command.Execute()
    assert result["Status"] == "Error"
    assert "has ammendments pending approval" in result["Message"]
    mock_logger.debug.assert_any_call(f"Booking 1 has ammendments pending approval.")

def test_approve_booking_exception(approve_booking_command, mock_repository, mock_logger):
    mock_repository.UpdateBookingStatus.side_effect = Exception("Update failed")
    result = approve_booking_command.Execute()
    assert result["Status"] == "Error"
    assert "Update failed" in result["Message"]
    mock_logger.error.assert_any_call(f"Error when attempting to approve booking 1: Update failed")