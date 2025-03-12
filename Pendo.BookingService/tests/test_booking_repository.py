import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch
from app.booking_repository import BookingRepository
from app.models import Booking, User, Journey, BookingAmmendment

def create_dummy_ammendment(create_date, start_name, start_long, start_lat, end_name, end_long, end_lat, start_time, proposed_price):
    ammendment = MagicMock(spec=BookingAmmendment)
    ammendment.CreateDate = create_date
    ammendment.StartName = start_name
    ammendment.StartLong = start_long
    ammendment.StartLat = start_lat
    ammendment.EndName = end_name
    ammendment.EndLong = end_long
    ammendment.EndLat = end_lat
    ammendment.StartTime = start_time
    ammendment.ProposedPrice = proposed_price
    ammendment.DriverApproval = True
    ammendment.PassengerApproval = True
    return ammendment

def setup_dummy_booking(ammendments):
    dummy_status = MagicMock()
    dummy_status.Status = 'Confirmed'
    dummy_status.Description = 'Booking is confirmed'
    
    dummy_journey = MagicMock(spec=Journey)
    dummy_journey.UserId = 1
    dummy_journey.StartName = 'Original Start'
    dummy_journey.StartLong = 0.0
    dummy_journey.StartLat = 0.0
    dummy_journey.EndName = 'Original End'
    dummy_journey.EndLong = 0.0
    dummy_journey.EndLat = 0.0
    dummy_journey.AdvertisedPrice = 50
    dummy_journey.JourneyStatusId = 2
    dummy_journey.JourneyType = 'RoundTrip'
    
    dummy_booking = MagicMock(spec=Booking)
    dummy_booking.BookingId = 1
    dummy_booking.UserId = 1
    dummy_booking.FeeMargin = 5
    dummy_booking.RideTime = '2025-03-02T09:00:00'
    dummy_booking.BookingStatusId = 1
    dummy_booking.BookingStatus_ = dummy_status
    dummy_booking.JourneyId = 1
    dummy_booking.Journey_ = dummy_journey
    dummy_booking.BookingAmmendment = ammendments
    return dummy_booking

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def booking_repository(mock_db_session):
    with patch('app.booking_repository.get_db', return_value=iter([mock_db_session])):
        return BookingRepository()
    
def test_get_bookings_for_user_no_ammendment(booking_repository):
    dummy_booking = setup_dummy_booking([])
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_options = MagicMock()
    booking_repository.db_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.options.return_value = mock_options
    mock_options.all.return_value = [dummy_booking]

    result = booking_repository.GetBookingsForUser(1)

    expected = [{
        "Booking": {
            "BookingId": 1,
            "UserId": 1,
            "FeeMargin": 5,
            "RideTime": '2025-03-02T09:00:00'
        },
        "BookingStatus": {
            "StatusId": 1,
            "Status": dummy_booking.BookingStatus_.Status,
            "Description": dummy_booking.BookingStatus_.Description
        },
        "Journey": {
            "JourneyId": 1,
            "UserId": dummy_booking.Journey_.UserId,
            "StartTime": dummy_booking.RideTime,
            "StartName": dummy_booking.Journey_.StartName,
            "StartLong": dummy_booking.Journey_.StartLong,
            "StartLat": dummy_booking.Journey_.StartLat,
            "EndName": dummy_booking.Journey_.EndName,
            "EndLong": dummy_booking.Journey_.EndLong,
            "EndLat": dummy_booking.Journey_.EndLat,
            "Price": dummy_booking.Journey_.AdvertisedPrice,
            "JourneyStatusId": dummy_booking.Journey_.JourneyStatusId,
            "JourneyType": dummy_booking.Journey_.JourneyType
        }
    }]

    assert result == expected
    booking_repository.db_session.query.assert_called_once_with(Booking)

def test_get_bookings_for_user_single_ammendment(booking_repository):
    ammendment = create_dummy_ammendment(
        create_date=datetime(2025, 3, 1, 12, 0, 0),
        start_name="Ammended Start",
        start_long=11.1,
        start_lat=22.2,
        end_name="Ammended End",
        end_long=33.3,
        end_lat=44.4,
        start_time="2025-03-02T11:00:00",
        proposed_price=75
    )
    dummy_booking = setup_dummy_booking([ammendment])
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_options = MagicMock()
    booking_repository.db_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.options.return_value = mock_options
    mock_options.all.return_value = [dummy_booking]
    
    result = booking_repository.GetBookingsForUser(1)
    
    expected = [{
        "Booking": {
            "BookingId": 1,
            "UserId": 1,
            "FeeMargin": 5,
            "RideTime": "2025-03-02T11:00:00"
        },
        "BookingStatus": {
            "StatusId": 1,
            "Status": 'Confirmed',
            "Description": 'Booking is confirmed'
        },
        "Journey": {
            "JourneyId": 1,
            "UserId": 1,
            "StartTime": "2025-03-02T11:00:00",
            "StartName": "Ammended Start",
            "StartLong": 11.1,
            "StartLat": 22.2,
            "EndName": "Ammended End",
            "EndLong": 33.3,
            "EndLat": 44.4,
            "Price": 75,
            "JourneyStatusId": 2,
            "JourneyType": 'RoundTrip'
        }
    }]
    
    assert result == expected
    booking_repository.db_session.query.assert_called_once_with(Booking)

def test_get_bookings_for_user_multiple_ammendments(booking_repository):
    earlier_ammendment = create_dummy_ammendment(
        create_date=datetime(2025, 3, 1, 10, 0, 0),
        start_name="Early Start",
        start_long=10.0,
        start_lat=20.0,
        end_name="Early End",
        end_long=30.0,
        end_lat=40.0,
        start_time="2025-03-02T10:00:00",
        proposed_price=60
    )
    later_ammendment = create_dummy_ammendment(
        create_date=datetime(2025, 3, 1, 15, 0, 0),
        start_name="Late Start",
        start_long=15.5,
        start_lat=25.5,
        end_name="Late End",
        end_long=35.5,
        end_lat=45.5,
        start_time="2025-03-02T12:00:00",
        proposed_price=80
    )
    dummy_booking = setup_dummy_booking([later_ammendment, earlier_ammendment])
    mock_query = MagicMock()
    mock_filter = MagicMock()
    mock_options = MagicMock()
    booking_repository.db_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_filter
    mock_filter.options.return_value = mock_options
    mock_options.all.return_value = [dummy_booking]
    
    result = booking_repository.GetBookingsForUser(1)
    
    expected = [{
        "Booking": {
            "BookingId": 1,
            "UserId": 1,
            "FeeMargin": 5,
            "RideTime": "2025-03-02T12:00:00"
        },
        "BookingStatus": {
            "StatusId": 1,
            "Status": 'Confirmed',
            "Description": 'Booking is confirmed'
        },
        "Journey": {
            "JourneyId": 1,
            "UserId": 1,
            "StartTime": "2025-03-02T12:00:00",
            "StartName": "Late Start",
            "StartLong": 15.5,
            "StartLat": 25.5,
            "EndName": "Late End",
            "EndLong": 35.5,
            "EndLat": 45.5,
            "Price": 80,
            "JourneyStatusId": 2,
            "JourneyType": 'RoundTrip'
        }
    }]
    
    assert result == expected
    booking_repository.db_session.query.assert_called_once_with(Booking)

def test_get_user(booking_repository, mock_db_session):
    mock_db_session.query.return_value.get.return_value = User()
    result = booking_repository.GetUser(1)
    assert result is not None
    mock_db_session.query.assert_called_once_with(User)

def test_get_journey(booking_repository, mock_db_session):
    mock_db_session.query.return_value.get.return_value = Journey()
    result = booking_repository.GetJourney(1)
    assert result is not None
    mock_db_session.query.assert_called_once_with(Journey)

def test_get_booking_by_id(booking_repository, mock_db_session):
    mock_db_session.query.return_value.get.return_value = Booking()
    result = booking_repository.GetBookingById(1)
    assert result is not None
    mock_db_session.query.assert_called_once_with(Booking)

def test_get_existing_booking(booking_repository, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Booking()
    result = booking_repository.GetExistingBooking(1, 1, "2023-01-01 12:00:00")
    assert result is not None
    mock_db_session.query.assert_called_once_with(Booking)

def test_create_booking(booking_repository, mock_db_session):
    booking = Booking(JourneyId=1)
    mock_db_session.query.return_value.get.return_value = Journey()
    booking_repository.CreateBooking(booking)
    mock_db_session.add.assert_called_once_with(booking)
    mock_db_session.commit.assert_called_once()

def test_approve_booking(booking_repository, mock_db_session):
    booking = Booking(BookingId=1, DriverApproval=False)
    mock_db_session.query.return_value.get.return_value = booking
    result = booking_repository.ApproveBooking(1)
    assert result.DriverApproval is True
    mock_db_session.commit.assert_called_once()

def test_update_booking_status(booking_repository, mock_db_session):
    booking = Booking(BookingId=1)
    mock_db_session.query.return_value.get.return_value = booking
    booking_repository.UpdateBookingStatus(1, 2)
    assert booking.BookingStatusId == 2
    mock_db_session.commit.assert_called_once()

def test_add_booking_ammendment(booking_repository, mock_db_session):
    ammendment = BookingAmmendment()
    booking_repository.AddBookingAmmendment(ammendment)
    mock_db_session.add.assert_called_once_with(ammendment)
    mock_db_session.commit.assert_called_once()

def test_get_booking_ammendment(booking_repository, mock_db_session):
    ammendment = MagicMock()
    ammendment.BookingId = 1
    booking = MagicMock(UserId=1, JourneyId=1)
    journey = MagicMock(UserId=2)
    mock_db_session.query.return_value.get.side_effect = [ammendment, booking, User(), journey, User()]
    result = booking_repository.GetBookingAmmendment(1)
    assert result is not None
    mock_db_session.query.assert_any_call(BookingAmmendment)
    mock_db_session.query.assert_any_call(Booking)
    mock_db_session.query.assert_any_call(User)
    mock_db_session.query.assert_any_call(Journey)