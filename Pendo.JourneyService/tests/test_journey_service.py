import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.journey_service import create_journey, get_journeys, lock_journey, adjust_price
from app.request_lib import CreateJourneyRequest, GetJourneysRequest, AdjustPriceRequest
from app.journey_repository import JourneyRepository
from fastapi import Response
from app.parameter_checking import CheckJourneyData
from datetime import datetime

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def mock_repository(mock_db_session):
    return JourneyRepository(mock_db_session)

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def create_journey_request():
    return CreateJourneyRequest(
        UserId=uuid4(),
        Origin="City A",
        Destination="City B",
        StartTime="2025-03-15T08:00:00"
    )

@pytest.fixture
def get_journeys_request():
    return GetJourneysRequest(SortByPrice="asc")

@pytest.fixture
def adjust_price_request():
    return AdjustPriceRequest(
        UserId=uuid4(),
        NewPrice=100.00
    )

@pytest.fixture
def response():
    return Response()

def test_create_journey_success(mock_db_session, create_journey_request):
    create_journey_request.StartName = "Test Start"
    create_journey_request.StartLong = 1.0
    create_journey_request.StartLat = 1.0
    create_journey_request.EndName = "Test End"
    create_journey_request.EndLong = 2.0
    create_journey_request.EndLat = 2.0
    create_journey_request.AdvertisedPrice = 100
    create_journey_request.StartDate = datetime.now()
    create_journey_request.StartTime = datetime.now()
    create_journey_request.MaxPassengers = 4
    create_journey_request.RegPlate = "ABC123"
    create_journey_request.CurrencyCode = "GBP"
    create_journey_request.JourneyType = 1
    create_journey_request.BootWidth = 50
    create_journey_request.BootHeight = 60
    create_journey_request.LockedUntil = datetime.now()
    
    mock_journey = MagicMock()
    mock_journey.JourneyId = uuid4()
    
    mock_db_session.add.return_value = None
    mock_db_session.commit.return_value = None
    mock_db_session.refresh.side_effect = lambda x: setattr(x, "JourneyId", mock_journey.JourneyId)
    
    result = create_journey(create_journey_request, db=mock_db_session)
    
    assert hasattr(result, "JourneyId")
    assert result.JourneyId is not None

def test_create_journey_validation_error(mock_db_session):
    invalid_request = CreateJourneyRequest(
        UserId=uuid4(),
        Origin=None,
        Destination=None,
        StartTime=None
    )
    result = create_journey(invalid_request, db=mock_db_session)

    assert result["Status"] == "Failed"
    assert "Message" in result

def test_get_journeys_success(mock_db_session, get_journeys_request):
    mock_db_session.query.return_value.filter.return_value.order_by.return_value.all.return_value = [
        {"JourneyId": uuid4()}
    ]

    result = get_journeys(get_journeys_request, db=mock_db_session)
    assert len(result) > 0

def test_lock_journey_success(mock_db_session, response):
    journey_id = uuid4()
    
    mock_journey = MagicMock()
    mock_journey.JourneyId = journey_id
    mock_journey.LockedUntil = None
    
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_journey
    
    result = lock_journey(journey_id, response, db=mock_db_session)
    
    assert result == mock_journey

def test_adjust_price_success(mock_db_session, adjust_price_request):
    mock_repo = MagicMock()
    journey_id = 1
    mock_repo.adjust_journey.return_value = {"JourneyId": journey_id, "AdvertisedPrice": adjust_price_request.AdvertisedPrice}
    
    mock_db_session.query.return_value.filter_by.return_value.first.return_value = MagicMock(JourneyId=journey_id)
    
    result = adjust_price(journey_id, adjust_price_request)
    
    assert result is not None

def test_check_inputs_journey_type_2_missing_fields():
    mock_request = MagicMock(spec=CreateJourneyRequest)
    for field in ["AdvertisedPrice", "StartName", "StartLong", "StartLat", "EndName", 
                 "EndLong", "EndLat", "StartDate", "StartTime", "MaxPassengers", 
                 "RegPlate", "CurrencyCode", "BootWidth", "BootHeight", "LockedUntil"]:
        setattr(mock_request, field, "dummy_value")
    
    mock_request.JourneyType = 2
    mock_request.Recurrance = None
    mock_request.ReturnUntil = None
    checker = CheckJourneyData(mock_request)
    with pytest.raises(Exception, match="Recurrance is required for JourneyType 2."):
        checker.check_inputs()