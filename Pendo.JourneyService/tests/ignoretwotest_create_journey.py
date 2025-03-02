import pytest
from unittest.mock import MagicMock
from app.create_journey import CreateJourneyCommand
from app.get_journeys import GetJourneysCommand

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def create_journey_command(mock_repository, mock_logger):
    return CreateJourneyCommand(mock_repository, mock_logger)

@pytest.fixture
def get_journeys_command(mock_repository, mock_logger):
    return GetJourneysCommand(mock_repository, mock_logger)

def test_create_journey_success(create_journey_command, mock_repository, mock_logger):
    result = create_journey_command.Execute()
    assert result["Status"] == "Success"