import pytest
from unittest.mock import MagicMock
from app.add_booking_ammendment import AddBookingAmmendmentCommand
from datetime import datetime, timedelta

class DummyRequest:
    BookingId = 1
    ProposedPrice = 100.0
    StartName = "Start"
    StartLong = 0.0
    StartLat = 0.0
    EndName = "End"
    EndLat = 1.0
    StartTime = datetime.now() + timedelta(hours=1)
    CancellationRequest = False
    DriverApproval = False
    PassengerApproval = False

class DummyResponse:
    def __init__(self):
        self.status_code = None

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.GetBookingById.return_value = MagicMock(BookingId=1, BookingStatusId=1)
    return repo

@pytest.fixture
def add_booking_ammendment_command(mock_repository, mock_logger):
    req = DummyRequest()
    res = DummyResponse()
    cmd = AddBookingAmmendmentCommand(req, res, mock_logger)
    cmd.booking_repository = mock_repository
    return cmd

def test_add_booking_ammendment_success(add_booking_ammendment_command, mock_repository, mock_logger):
    result = add_booking_ammendment_command.Execute()

    assert result["Status"] == "Success"
    mock_repository.AddBookingAmmendment.assert_called_once()
    mock_logger.debug.assert_any_call(f"Added booking amendment for booking {DummyRequest.BookingId} successfully.")

def test_add_booking_ammendment_booking_not_found(add_booking_ammendment_command, mock_repository):
    mock_repository.GetBookingById.return_value = None

    result = add_booking_ammendment_command.Execute()

    assert result["Status"] == "Error"
    assert add_booking_ammendment_command.response.status_code == 404
    assert f"Booking {DummyRequest.BookingId} not found" in result["Message"]