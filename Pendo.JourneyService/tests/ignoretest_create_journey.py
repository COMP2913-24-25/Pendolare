# 
# Python testing implentation for Pendo.JourneyService using Pytest
# Author: Catherine Weightman
# Created: 12/02/2025
#

import pytest
#from fastapi.testclient import TestClient
#from src.journey_service import app, some_testing_function
#from src.PendoDatabase import Journey
from unittest.mock import MagicMock
#from .app.src.create_journey import CreateJourneyCommand
#from src.journey_repository import Journey
#import uuid
 
from app.create_journey import CreateJourneyCommand
from app.journey_repository import JourneyRepository

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_repository():
    mock = MagicMock()

    #mock.GetUser.return_value = MagicMock(UserId=1)

    #mock.GetUser.return_value = MagicMock(UserId=1, Email="test@user.com")
    #mock.GetJourney.return_value = MagicMock(JourneyId=2)
    #mock.GetExistingBooking.return_value = None
    return mock


@pytest.fixture
def create_journey_command(mock_repository, mock_logger):
    class DummyRequest:
        UserId = 1

    cmd = CreateJourneyCommand(DummyRequest(), mock_logger)
    cmd.journey_repository = mock_repository
    return cmd

def test_create_journey_success(create_journey_command, mock_repository, mock_logger):
    result = create_journey_command.Execute()
    assert result["Status"] == "Success"
    mock_repository.CreateJourney.assert_called_once()
    mock_logger.debug.assert_any_call("Booking pending email sent successfully.")

'''
client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Journey"}

def test_view_endpoint():
    response = client.get("/view")
    assert response.status_code == 200
    assert response.json() == {"message": "View Journey"}
'''

#def test_create_endpoint():
    #response = client.post("/create/")
    #assert response.status_code == 200
    #assert response.json() == "Create Journey"

    #@pytest.fixture(scope="function", autouse=True)
    #def src(self):

'''
def test_create_journey():
    payload = {
        "UserId": "12345",
        "Cost": 10.5,
        "StartName": "A",
        "StartLong": 123456,
        "StartLat": 123456,
        "EndName": "B",
        "EndLong": 654321,
        "EndLat": 654321,
        "JourneyType": 1,
        "StartDate": "2025-02-20 14:00:00",
        "RepeatUntil": "2025-02-20 20:00:00",
        "Recurrance": "0 0 0 ? * 3/3 *",
        "Status": 2,
        "MaxPassengers": 3,
        "RegPlate": "XXXXXX",
        "BootWidth": 2.1,
        "BootHeight": 1.2
    }
'''
    #No start time

    #response = requests.post(f"{BASE_URL}/create", json=payload)
    #assert response.status_code == 201
    #assert "data" in response.json()
'''
def test_create_journey():
    payload = {
        "UserId": "12345",
        "Cost": 10.5,
        "StartName": "A",
        "StartLong": 123456,
        "StartLat": 123456,
        "EndName": "B",
        "EndLong": 654321,
        "EndLat": 654321,
        "JourneyType": 1,
        "StartDate": "2025-02-20 14:00:00",
        "RepeatUntil": "2025-02-20 20:00:00",
        "Recurrance": "0 0 0 ? * 3/3 *",
        "Status": 2,
        "MaxPassengers": 3,
        "RegPlate": "XXXXXX",
        "BootWidth": 2.1,
        "BootHeight": 1.2
    }

    response = client.post("/create/", json=payload)
    assert response.status_code == 200  # Adjust if you expect 201
    assert response.json() == {"message": "Create Journey"}
'''
'''
def test_testing_function():
    # Arrange
    param = True

    # Act
    result = some_testing_function(param)

    # Assert
    assert result == param
'''