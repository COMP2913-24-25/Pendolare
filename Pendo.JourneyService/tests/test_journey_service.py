import pytest
from unittest.mock import MagicMock
from app.create_journey import CreateJourneyCommand
from app.get_journeys import GetJourneysCommand
from app.journey_repository import Journey
from app.requests import CreateJourneyRequest, GetJourneysRequest
import uuid
from unittest.mock import Mock
from app.journey_repository import JourneyRepository, Journey
from datetime import datetime, timedelta,timezone

# filepath: /workspaces/software-engineering-project-team-2/Pendo.JourneyService/app/test_journey_service.py


@pytest.fixture
def mock_request():
    request = Mock()
    request.UserId = uuid.uuid4()
    return request

@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
class CreateJourneyCommand:
    def __init__(self, request, logger):
        self.journey_repository = JourneyRepository()
        self.request = request
        self.logger = logger

    def Execute(self):
        try:
            user = self.journey_repository.GetUser(self.request.UserId)
            if user is None:
                raise Exception("User not found")

            JourneyToAdd = Journey(
                UserId=user.UserId,
                AdvertisedPrice=3.5,
                CurrencyCode="GBP",
                StartName="Trinity Center",
                StartLong=44.2,
                StartLat=3.5,
                EndName="King's Cross",
                EndLong=45.0,
                EndLat=4.0,
                JourneyType=1,
                StartDate=datetime.datetime.now(timezone.utc),
                RepeatUntil=datetime.datetime.now(timezone.utc) + timedelta(days=30),
                Recurrance="Weekly",
                StartTime=datetime.datetime.now(timezone.utc),
                JourneyStatusId=1,
                MaxPassengers=4,
                RegPlate="AB12 CDE",
                BootWidth=1.2,
                BootHeight=0.8,
                CreateDate=datetime.datetime.now(timezone.utc),
                UpdateDate=datetime.datetime.now(timezone.utc),
            )

            self.journey_repository.CreateJourney(JourneyToAdd)
            self.logger.debug("Creating booking with request %s.", self.request)
            return {"message": "Create Journey"}
        except Exception as e:
            self.logger.error("Error creating journey: %s", str(e))
            return {"message": "Failed"}
        
    journeys = get_journeys_command.Execute()
    assert len(journeys) == 2
    get_journeys_command.logger.debug.assert_called_with("Getting all journeys")
    get_journeys_command.logger.debug.assert_called_with("Retrieved [2].")

def test_get_journeys_empty(get_journeys_command, mock_repository, mock_request):
    mock_repository.GetAllJourneys.return_value = []
    journeys = get_journeys_command.Execute()
    assert len(journeys) == 0
    get_journeys_command.logger.debug.assert_called_with("Getting all journeys")
    get_journeys_command.logger.debug.assert_called_with("Retrieved [0].")

def test_get_journeys_none(get_journeys_command, mock_repository, mock_request):
    mock_repository.GetAllJourneys.return_value = None
    journeys = get_journeys_command.Execute()
    assert len(journeys) == 0
    get_journeys_command.logger.debug.assert_called_with("Getting all journeys")
    get_journeys_command.logger.debug.assert_called_with("Retrieved [0].")