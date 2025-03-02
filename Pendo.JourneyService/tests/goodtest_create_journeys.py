import pytest
from unittest.mock import MagicMock
from app.create_journey import CreateJourneyCommand
from app.get_journeys import GetJourneysCommand
from app.journey_repository import Journey
import uuid
from unittest.mock import Mock

@pytest.fixture
def mock_request():
    request = Mock()
    request.UserId = uuid.uuid4()
    return request

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def create_journey_command(mock_repository, mock_logger):
    return CreateJourneyCommand(mock_repository, mock_logger)

def test_create_journey_success(create_journey_command, mock_repository, mock_logger):
    result = create_journey_command.Execute()
    assert result["Status"] == "Success"
    mock_repository.CreateJourney.assert_called_once()
    mock_logger.debug.assert_any_call("Booking pending email sent successfully.")