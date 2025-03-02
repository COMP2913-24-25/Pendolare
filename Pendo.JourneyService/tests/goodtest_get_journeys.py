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

'''
@pytest.fixture
def get_journeys_command(mock_request, mock_logger, mock_repository):
    command = GetJourneysCommand(mock_request, mock_logger)
    command.journey_repository = mock_repository
    return command


def test_get_journeys_success(get_journeys_command, mock_journey_repository, mock_request):
    mock_journey_repository.GetAllJourneys.return_value = [Journey(), Journey()]
    journeys = get_journeys_command.Execute()
    assert len(journeys) == 2
    get_journeys_command.logger.debug.assert_called_with(f"Retrieved [2] Bookings successfully.")


    pytest.fixture
'''

def test_get_journeys_command(mock_request, mock_logger, mock_repository):
    command = GetJourneysCommand(mock_request, mock_logger)
    command.journey_repository = mock_repository
    assert command
    #return command
'''
def test_get_journeys_command():
    result = app.get_journeys.GetJourneysCommand()
    assert result is not None
'''
'''
def test_get_journeys_success(get_journeys_command, mock_repository, mock_request):
    mock_repository.GetJourney.return_value = [Journey(), Journey()]
    journeys = get_journeys_command.Execute()
    assert len(journeys) == 2
    get_journeys_command.logger.debug.assert_called_with("Getting all journeys")
    get_journeys_command.logger.debug.assert_called_with("Retrieved [2].")
'''
'''

def test_get_journeys_empty(get_journeys_command, mock_repository, mock_request):
    mock_repository.GetJourney.return_value = []
    journeys = get_journeys_command.Execute()
    assert len(journeys) == 0
    get_journeys_command.logger.debug.assert_called_with("Getting all journeys")
    get_journeys_command.logger.debug.assert_called_with("Retrieved [0].")

def test_get_journeys_none(get_journeys_command, mock_repository, mock_request):
    mock_repository.GetJourney.return_value = None
    journeys = get_journeys_command.Execute()
    assert len(journeys) == 0
    get_journeys_command.logger.debug.assert_called_with("Getting all journeys")
    get_journeys_command.logger.debug.assert_c
'''