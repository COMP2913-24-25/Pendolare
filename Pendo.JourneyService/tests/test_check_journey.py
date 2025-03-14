import pytest
from unittest.mock import MagicMock
from app.request_lib import CreateJourneyRequest
from app.parameter_checking import CheckJourneyData
from datetime import datetime

@pytest.fixture
def mock_request():
    mock = MagicMock(spec=CreateJourneyRequest)
    mock.AdvertisedPrice = 100
    mock.StartName = "Start Location"
    mock.StartLong = 1.2345
    mock.StartLat = 2.3456
    mock.EndName = "End Location"
    mock.EndLong = 3.4567
    mock.EndLat = 4.5678
    mock.StartDate = datetime.now().date()
    mock.StartTime = datetime.now().time()
    mock.MaxPassengers = 4
    mock.RegPlate = "ABC123"
    mock.CurrencyCode = "USD"
    mock.JourneyType = 1
    mock.BootWidth = 50
    mock.BootHeight = 50
    mock.LockedUntil = datetime.now()
    return mock

def test_check_inputs_success(mock_request):
    checker = CheckJourneyData(mock_request)
    result = checker.check_inputs()
    assert result == mock_request

def test_check_inputs_missing_required_field():
    mock_request = MagicMock(spec=CreateJourneyRequest)
    mock_request.AdvertisedPrice = None
    checker = CheckJourneyData(mock_request)
    with pytest.raises(Exception, match="AdvertisedPrice is required."):
        checker.check_inputs()

def test_check_inputs_journey_type_2_missing_fields():
    mock_request = MagicMock(spec=CreateJourneyRequest)
    mock_request.AdvertisedPrice = 100
    mock_request.StartName = "Start Location"
    mock_request.StartLong = 1.0
    mock_request.StartLat = 1.0
    mock_request.EndName = "End Location"
    mock_request.EndLong = 2.0
    mock_request.EndLat = 3.0
    mock_request.StartDate = datetime.now()
    mock_request.StartTime = datetime.now()
    mock_request.MaxPassengers = 4
    mock_request.RegPlate = "ABC123"
    mock_request.CurrencyCode = "USD"
    mock_request.BootWidth = 50
    mock_request.BootHeight = 60
    mock_request.LockedUntil = datetime.now()
    mock_request.JourneyType = 2
    mock_request.Recurrance = None
    mock_request.ReturnUntil = None
    checker = CheckJourneyData(mock_request)
    with pytest.raises(Exception, match="Recurrance is required for JourneyType 2."):
        checker.check_inputs()

def test_check_inputs_journey_type_1_sets_repeat_until(mock_request):
    mock_request.JourneyType = 1
    checker = CheckJourneyData(mock_request)
    result = checker.check_inputs()
    assert result.RepeatUntil == datetime(9999, 12, 31, 23, 59, 59)
