import pytest
from unittest.mock import MagicMock
from app.request_lib import GetJourneysRequest
from app.PendoDatabase import Journey
from app.parameter_filtering import FilterJourneys
from datetime import datetime
from uuid import UUID
from sqlalchemy.sql import and_

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_request():
    return GetJourneysRequest(UserId=UUID('123e4567-e89b-12d3-a456-426614174000'))

@pytest.fixture
def filter_journeys(mock_request, mock_db):
    return FilterJourneys(mock_request, mock_db)

def test_filter_journeys_max_price(filter_journeys, mock_request):
    mock_request.MaxPrice = 100
    filters = filter_journeys.apply_filters()
    assert any(str(f) == str(Journey.AdvertisedPrice <= 100) for f in filters)

def test_filter_journeys_boot_height(filter_journeys, mock_request):
    mock_request.BootHeight = 50
    filters = filter_journeys.apply_filters()
    assert any(str(f) == str(Journey.BootHeight >= 50) for f in filters)

def test_filter_journeys_boot_width(filter_journeys, mock_request):
    mock_request.BootWidth = 30
    filters = filter_journeys.apply_filters()
    assert any(str(f) == str(Journey.BootWidth >= 30) for f in filters)

def test_filter_journeys_journey_type(filter_journeys, mock_request):
    mock_request.JourneyType = 1
    filters = filter_journeys.apply_filters()
    assert any(str(f) == str(Journey.JourneyType == 1) for f in filters)

def test_filter_journeys_num_passengers(filter_journeys, mock_request):
    mock_request.NumPassengers = 3
    filters = filter_journeys.apply_filters()
    assert any(str(f) == str(Journey.MaxPassengers >= 3) for f in filters)

def test_filter_journeys_start_date(filter_journeys, mock_request):
    mock_request.StartDate = datetime(2025, 1, 1)
    filters = filter_journeys.apply_filters()
    assert any(str(Journey.StartDate >= datetime(2025, 1, 1)) in str(f) for f in filters)

def test_filter_journeys_start_location(filter_journeys, mock_request):
    mock_request.StartLat = 52.5
    mock_request.StartLong = -1.5
    mock_request.DistanceRadius = 0.1
    filters = filter_journeys.apply_filters()
    expected_filter = and_(
        Journey.StartLat.between(52.4, 52.6),
        Journey.StartLong.between(-1.6, -1.4)
    )
    assert any(str(f) == str(expected_filter) for f in filters)

def test_filter_journeys_end_location(filter_journeys, mock_request):
    mock_request.EndLat = 53.0
    mock_request.EndLong = -2.0
    mock_request.DistanceRadius = 0.2
    filters = filter_journeys.apply_filters()
    expected_filter = and_(
        Journey.EndLat.between(52.8, 53.2),
        Journey.EndLong.between(-2.2, -1.8)
    )
    assert any(str(f) == str(expected_filter) for f in filters)

def test_filter_journeys_journey_status(filter_journeys):
    filters = filter_journeys.apply_filters()
    assert any(str(f) == str(Journey.JourneyStatusId == 1) for f in filters)
