import pytest
from unittest.mock import MagicMock
from app.get_journeys import GetJourneysCommand
from app.journey_repository import Journey

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_repository():
    mock = MagicMock()

    #mock.GetUser.return_value = MagicMock(UserId=1)
    #mock.GetExistingBooking.return_value = None
    mock.GetAllJourneys.return_value = [Journey(), Journey()]
    return mock

def test_get_journeys_success(get_journeys_command, mock_booking_repository, mock_request):
    mock_booking_repository.GetAllJourneys.return_value = [Journey(), Journey()]
    journeys = get_journeys_command.Execute()
    assert len(journeys) == 2
    get_journeys_command.logger.debug.assert_called_with(f"Retrieved [2] Bookings successfully.")