import pytest
from datetime import datetime
from decimal import Decimal
from types import SimpleNamespace
from app.get_weekly_revenue import GetWeeklyRevenueCommand

class FakeQuery:
    def __init__(self, result):
        self.result = result
    def join(self, *args, **kwargs):
        return self
    def outerjoin(self, *args, **kwargs):
        return self
    def filter(self, *args, **kwargs):
        return self
    def all(self):
        return self.result

class FakeDBSession:
    def __init__(self, result):
        self.result = result
    def query(self, *args, **kwargs):
        return FakeQuery(self.result)

class FakeDBSessionException:
    def query(self, *args, **kwargs):
        raise Exception("DB Error")

@pytest.fixture
def mock_bookings():
    b1 = SimpleNamespace(
        RideTime=datetime(2023, 1, 3),
        FeeMargin=10,
        BookingAmmendment=[],
        Journey_=SimpleNamespace(AdvertisedPrice=Decimal("100.00"))
    )
    b2 = SimpleNamespace(
        RideTime=datetime(2023, 1, 10),
        FeeMargin=20,
        BookingAmmendment=[SimpleNamespace(ProposedPrice=Decimal("150.00"))],
        Journey_=SimpleNamespace(AdvertisedPrice=Decimal("200.00"))
    )
    return [b1, b2]

@pytest.fixture
def mock_request():
    return SimpleNamespace(StartDate="2023-01-01", EndDate="2023-01-31")

@pytest.fixture
def mock_response():
    return SimpleNamespace(status_code=200)

@pytest.fixture
def mock_configuration_provider():
    return SimpleNamespace()

def test_execute_success(mock_bookings, mock_request, mock_response, mock_configuration_provider):
    db_session = FakeDBSession(mock_bookings)
    cmd = GetWeeklyRevenueCommand(db_session, mock_request, mock_response, mock_configuration_provider)
    result = cmd.Execute()

    assert 'Error' not in result
    assert result.labels == ["WEEK 1", "WEEK 2"]
    assert result.data == [10.0, 30.0]
    assert result.currency == "£"
    assert result.total == "£40.00"
    assert mock_response.status_code != 500

def test_execute_same_week(mock_request, mock_response, mock_configuration_provider):
    b1 = SimpleNamespace(
        RideTime=datetime(2023, 1, 3),
        FeeMargin=10,
        BookingAmmendment=[],
        Journey_=SimpleNamespace(AdvertisedPrice=Decimal("100.00"))
    )
    b2 = SimpleNamespace(
        RideTime=datetime(2023, 1, 4),
        FeeMargin=20,
        BookingAmmendment=[SimpleNamespace(ProposedPrice=Decimal("150.00"))],
        Journey_=SimpleNamespace(AdvertisedPrice=Decimal("200.00"))
    )
    db_session = FakeDBSession([b1, b2])
    cmd = GetWeeklyRevenueCommand(db_session, mock_request, mock_response, mock_configuration_provider)
    result = cmd.Execute()
    assert result.labels == ["WEEK 1"]
    assert result.data == [40.0]
    assert result.currency == "£"
    assert result.total == "£40.00"

def test_execute_exception(mock_request, mock_response, mock_configuration_provider):
    db_session = FakeDBSessionException()
    cmd = GetWeeklyRevenueCommand(db_session, mock_request, mock_response, mock_configuration_provider)
    result = cmd.Execute()
    assert "Error" in result
    assert mock_response.status_code == 500
