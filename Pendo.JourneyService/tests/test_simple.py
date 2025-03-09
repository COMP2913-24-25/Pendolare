import pytest
from uuid import uuid4
from app.request_lib import CreateJourneyRequest

def test_create_journey_request_success():
    journey_request = CreateJourneyRequest(
        user_id=uuid4(),
        advertised_price=100.0,
        start_name="Start Location",
        start_long=10.123,
        start_lat=20.456,
        end_name="End Location",
        end_long=30.789,
        end_lat=40.012,
        start_date="2025-03-09T10:00:00",
        repeat_until="2025-03-10T10:00:00",
        start_time="10:00:00",
        max_passengers=4,
        reg_plate="ABC123",
        currency_code="GBP",
        journey_type=1,
        boot_width=50.0,
        boot_height=40.0,
        locked_until=None
    )
    assert journey_request.user_id is not None

def test_create_journey_request_missing_user_id():
    with pytest.raises(ValueError):
        CreateJourneyRequest(
            user_id=None,
            advertised_price=100.0,
            start_name="Start Location",
            start_long=10.123,
            start_lat=20.456,
            end_name="End Location",
            end_long=30.789,
            end_lat=40.012,
            start_date="2025-03-09T10:00:00",
            repeat_until="2025-03-10T10:00:00",
            start_time="10:00:00",
            max_passengers=4,
            reg_plate="ABC123",
            currency_code="GBP",
            journey_type=1,
            boot_width=50.0,
            boot_height=40.0,
            locked_until=None
        )