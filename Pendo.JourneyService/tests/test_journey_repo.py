import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from fastapi import status
from app.PendoDatabase import Journey
from app.journey_repository import JourneyRepository

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_response():
    class DummyResponse:
        def __init__(self):
            self.status_code = None
            self.AdvertisedPrice = 100
    return DummyResponse()

@pytest.fixture
def journey_repository(mock_db):
    return JourneyRepository(mock_db)

def test_get_journeys(journey_repository, mock_db):
    mock_db.query.return_value.filter.return_value = [MagicMock(JourneyId=1), MagicMock(JourneyId=2)]
    filters = [MagicMock()]
    journeys = journey_repository.get_journeys(filters)
    assert len(journeys) == 2
    mock_db.query.assert_called_once_with(Journey)
    mock_db.query().filter.assert_called_once_with(*filters)

def test_lock_journey_success(journey_repository, mock_db, mock_response):
    journey = MagicMock(JourneyId=1, LockedUntil=None)
    mock_db.query.return_value.filter_by.return_value.first.return_value = journey
    result = journey_repository.lock_journey(1, mock_response)
    assert result == journey  # Keep as is since you're returning journey
    assert journey.LockedUntil is not None
    mock_db.commit.assert_called_once()

def test_lock_journey_not_found(journey_repository, mock_db, mock_response):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with pytest.raises(Exception, match="Cannot lock journey that does not exist."):
        journey_repository.lock_journey(1, mock_response)
    assert mock_response.status_code == status.HTTP_404_NOT_FOUND

def test_lock_journey_already_locked(journey_repository, mock_db, mock_response):
    journey = MagicMock(JourneyId=1, LockedUntil=datetime.now() + timedelta(minutes=5))
    mock_db.query.return_value.filter_by.return_value.first.return_value = journey
    with pytest.raises(Exception, match="Journey 1 is already locked."):
        journey_repository.lock_journey(1, mock_response)
    assert mock_response.status_code == status.HTTP_401_UNAUTHORIZED

def test_create_journey(journey_repository, mock_db):
    mock_data = MagicMock()
    mock_data.dict.return_value = {"JourneyId": 1, "LockedUntil": None}
    journey_instance = MagicMock(JourneyId=1)
    mock_db.add.side_effect = lambda x: setattr(x, "JourneyId", 1)
    mock_db.commit.side_effect = lambda: None
    mock_db.refresh.side_effect = lambda x: None
    mock_db.add.return_value = None
    result = journey_repository.create_journey(mock_data)
    assert result.JourneyId == 1
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

def test_adjust_journey_success(journey_repository, mock_db, mock_response):
    journey = MagicMock(JourneyId=1, AdvertisedPrice=50)
    mock_db.query.return_value.filter_by.return_value.first.return_value = journey
    result = journey_repository.adjust_journey(1, mock_response)
    assert result == journey
    assert journey.AdvertisedPrice == mock_response.AdvertisedPrice
    mock_db.commit.assert_called_once()

def test_adjust_journey_not_found(journey_repository, mock_db, mock_response):
    mock_db.query.return_value.filter_by.return_value.first.return_value = None
    with pytest.raises(Exception, match="Cannot lock journey that does not exist."):
        journey_repository.adjust_journey(1, mock_response)
    assert mock_response.status_code == status.HTTP_404_NOT_FOUND

def test_adjust_journey_invalid_price(journey_repository, mock_db):
    mock_response = MagicMock()
    mock_response.status_code = None
    mock_response.AdvertisedPrice = 0
    journey = MagicMock(JourneyId=1, AdvertisedPrice=50)
    mock_db.query.return_value.filter_by.return_value.first.return_value = journey
    with pytest.raises(Exception, match="AdvertisedPrice is incomplete."):
        journey_repository.adjust_journey(1, mock_response)
    assert mock_response.status_code == status.HTTP_400_BAD_REQUEST