import pytest
from unittest.mock import Mock, MagicMock
from app.get_bookings import GetBookingsCommand
from app.booking_repository import Booking
import uuid

@pytest.fixture
def mock_request():
    request = MagicMock(UserId = uuid.uuid4())
    return request

@pytest.fixture
def mock_logger():
    return Mock()

@pytest.fixture
def mock_booking_repository():
    return Mock()

@pytest.fixture
def get_bookings_command(mock_request, mock_logger, mock_booking_repository):
    command = GetBookingsCommand(mock_request, mock_logger)
    command.booking_repository = mock_booking_repository
    return command

def test_get_bookings_success(get_bookings_command, mock_booking_repository, mock_request):
    mock_booking_repository.GetBookingsForUser.return_value = [Booking(), Booking()]
    bookings = get_bookings_command.Execute()
    assert len(bookings) == 2
    get_bookings_command.logger.debug.assert_called_with(f"Retrieved [2] Bookings for user {mock_request.UserId} successfully.")

def test_get_bookings_no_bookings(get_bookings_command, mock_booking_repository, mock_request):
    mock_booking_repository.GetBookingsForUser.return_value = []
    bookings = get_bookings_command.Execute()
    assert bookings == []
    get_bookings_command.logger.debug.assert_called_with(f"Retrieved [0] Bookings for user {mock_request.UserId} successfully.")

def test_get_bookings_none(get_bookings_command, mock_booking_repository, mock_request):
    mock_booking_repository.GetBookingsForUser.return_value = None
    bookings = get_bookings_command.Execute()
    assert bookings == []
    get_bookings_command.logger.debug.assert_called_with(f"Retrieved [0] Bookings for user {mock_request.UserId} successfully.")