import pytest
from unittest.mock import MagicMock, patch
from uuid import uuid4
from app.journey_service import create_journey
from app.request_lib import CreateJourneyRequest
from fastapi import Response

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_response():
    return Response()

@pytest.fixture
def mock_user():
    return {
        "user_id": uuid4(),
        "name": "Test User",
        "email": "testuser@example.com"
    }

@pytest.fixture
def journey_request(mock_user):
    return CreateJourneyRequest(
        UserId=mock_user["user_id"],
        AdvertisedPrice=100.0,
        StartName="Start Location",
        StartLong=10.123,
        StartLat=20.456,
        EndName="End Location",
        EndLong=30.789,
        EndLat=40.012,
        StartDate="2025-03-15",
        RepeatUntil="2025-03-15 18:00:00",
        StartTime="2025-03-15 18:00:00",
        MaxPassengers=4,
        RegPlate="ABC123",
        CurrencyCode="GBP",
        JourneyType=1,
        BootWidth=50.0,
        BootHeight=40.0,
        LockedUntil="2025-03-15 18:00:00"
    )

@patch("app.journey_service.JourneyRepository")
@patch("app.journey_service.CheckJourneyData")
def test_create_journey_success(mock_check_journey, mock_repo, mock_db, mock_response, journey_request):
    mock_repo.return_value.create_journey.return_value = journey_request.dict()
    mock_check_journey.return_value.check_inputs.return_value = journey_request

    result = create_journey(journey_request, db=mock_db)

    assert result["UserId"] == str(journey_request.UserId)
    assert result["AdvertisedPrice"] == journey_request.AdvertisedPrice
    mock_repo.return_value.create_journey.assert_called_once()
    mock_check_journey.return_value.check_inputs.assert_called_once()

    '''
    mock_repo.return_value.create_journey.return_value = journey_request.dict()
    mock_check_journey.return_value.check_inputs.return_value = journey_request
    
    result = create_journey(journey_request, db=mock_db)
    
    assert result["UserId"] == journey_request.user_id
    assert result["AdvertisedPrice"] == journey_request.advertised_price
    mock_repo.return_value.create_journey.assert_called_once()
    mock_check_journey.return_value.check_inputs.assert_called_once()
    '''

@patch("app.journey_service.JourneyRepository")
@patch("app.journey_service.CheckJourneyData")
def test_create_journey_failure(mock_check_journey, mock_repo, mock_db, mock_response, journey_request):
    mock_check_journey.return_value.check_inputs.side_effect = Exception("Invalid data")
    
    result = create_journey(journey_request, db=mock_db)
    
    assert result["Status"] == "Failed"
    assert "Invalid data" in result["Message"]