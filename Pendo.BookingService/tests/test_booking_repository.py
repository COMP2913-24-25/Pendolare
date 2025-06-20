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
    ammendment.Recurrance = None
    return ammendment

def setup_dummy_booking(ammendments):
    dummy_status = MagicMock()
    dummy_status.Status = 'Confirmed'
    dummy_status.Description = 'Booking is confirmed'
    
    dummy_journey = MagicMock(spec=Journey)
    dummy_journey.UserId = 1
    dummy_journey.User_ = 1
    dummy_journey.StartName = 'Original Start'
    dummy_journey.StartLong = 0.0
    dummy_journey.StartLat = 0.0
    dummy_journey.EndName = 'Original End'
    dummy_journey.EndLong = 0.0
    dummy_journey.EndLat = 0.0
    dummy_journey.AdvertisedPrice = 50
    dummy_journey.JourneyStatusId = 2
    dummy_journey.JourneyType = 'RoundTrip'
    dummy_journey.Recurrance = None

    dummy_booking = MagicMock(spec=Booking)
    dummy_booking.BookingId = 1
    dummy_booking.UserId = 1
    dummy_booking.User_ = 1
    dummy_booking.FeeMargin = 5
    dummy_booking.RideTime = '2025-03-02T09:00:00'
    dummy_booking.BookedWindowEnd = '2025-03-02T10:00:00'
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

def setup_get_bookings_chain(db_session, dummy_booking):
    mock_query = MagicMock()
    mock_join = MagicMock()
    mock_filter = MagicMock()
    mock_options = MagicMock()
    db_session.query.return_value = mock_query
    mock_query.join.return_value = mock_join
    mock_join.filter.return_value = mock_filter
    mock_filter.options.return_value = mock_options
    mock_options.all.return_value = [dummy_booking]

def test_get_bookings_for_user_no_ammendment(booking_repository):
    dummy_booking = setup_dummy_booking([])
    setup_get_bookings_chain(booking_repository.db_session, dummy_booking)

    result = booking_repository.GetBookingsForUser(1)
    expected = [{
        "Booking": {
            "BookingId": 1,
            "User": 1,
            "FeeMargin": 5,
            "RideTime": '2025-03-02T09:00:00',
            "BookedWindowEnd": '2025-03-02T10:00:00'
        },
        "BookingStatus": {
            "StatusId": 1,
            "Status": 'Confirmed',
            "Description": 'Booking is confirmed'
        },
        "Journey": {
            "Discount": None,
            "JourneyId": 1,
            "User": 1,
            "StartTime": '2025-03-02T09:00:00',
            "StartName": 'Original Start',
            "StartLong": 0.0,
            "StartLat": 0.0,
            "EndName": 'Original End',
            "EndLong": 0.0,
            "EndLat": 0.0,
            "Price": 50,
            "JourneyStatusId": 2,
            "JourneyType": 'RoundTrip',
            "Recurrance": None
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
    dummy_booking.RideTime = '2025-03-02T09:00:00'
    dummy_booking.BookedWindowEnd = '2025-03-02T10:00:00'
    setup_get_bookings_chain(booking_repository.db_session, dummy_booking)
    
    result = booking_repository.GetBookingsForUser(1)
    expected = [{
        "Booking": {
            "BookingId": 1,
            "User": 1,
            "FeeMargin": 5,
            "RideTime": "2025-03-02T11:00:00",
            "BookedWindowEnd": '2025-03-02T10:00:00'
        },
        "BookingStatus": {
            "StatusId": 1,
            "Status": 'Confirmed',
            "Description": 'Booking is confirmed'
        },
        "Journey": {
            "Discount": None,
            "JourneyId": 1,
            "User": 1,
            "StartTime": "2025-03-02T11:00:00",
            "StartName": "Ammended Start",
            "StartLong": 11.1,
            "StartLat": 22.2,
            "EndName": "Ammended End",
            "EndLong": 33.3,
            "EndLat": 44.4,
            "Price": 75,
            "JourneyStatusId": 2,
            "JourneyType": 'RoundTrip',
            "Recurrance": None
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
    dummy_booking.RideTime = '2025-03-02T09:00:00'
    dummy_booking.BookedWindowEnd = '2025-03-02T10:00:00'
    setup_get_bookings_chain(booking_repository.db_session, dummy_booking)
    
    result = booking_repository.GetBookingsForUser(1)
    expected = [{
        "Booking": {
            "BookingId": 1,
            "User": 1,
            "FeeMargin": 5,
            "RideTime": "2025-03-02T12:00:00",
            "BookedWindowEnd": '2025-03-02T10:00:00'
        },
        "BookingStatus": {
            "StatusId": 1,
            "Status": 'Confirmed',
            "Description": 'Booking is confirmed'
        },
        "Journey": {
            "Discount": None,
            "JourneyId": 1,
            "User": 1,
            "StartTime": "2025-03-02T12:00:00",
            "StartName": "Late Start",
            "StartLong": 15.5,
            "StartLat": 25.5,
            "EndName": "Late End",
            "EndLong": 35.5,
            "EndLat": 45.5,
            "Price": 80,
            "JourneyStatusId": 2,
            "JourneyType": 'RoundTrip',
            "Recurrance": None
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
    mock_db_session.query.return_value.join.return_value.filter.return_value.first.return_value = Booking()
    result = booking_repository.GetBookingById(1)
    assert result is not None
    mock_db_session.query.assert_called_once_with(Booking)

def test_get_existing_booking(booking_repository, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.first.return_value = Booking()
    result = booking_repository.GetExistingBooking(1, 1)
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
    mock_db_session.query.return_value.join.return_value.filter.return_value.first.return_value = booking

    result = booking_repository.ApproveBooking(1)
    
    assert result.DriverApproval is True
    mock_db_session.commit.assert_called_once()

def test_update_booking_status(booking_repository, mock_db_session):
    with patch('app.booking_repository.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 3, 1, 12, 0, 0)

        booking = Booking(BookingId=1, BookingStatusId=1)
        mock_db_session.query.return_value.join.return_value.filter.return_value.first.return_value = booking

        booking_repository.UpdateBookingStatus(1, 2)
        
        assert booking.BookingStatusId == 2
        assert booking.UpdateDate == datetime(2025, 3, 1, 12, 0, 0)
        mock_db_session.commit.assert_called_once()

def test_add_booking_ammendment(booking_repository, mock_db_session):
    ammendment = BookingAmmendment()
    booking_repository.AddBookingAmmendment(ammendment)
    mock_db_session.add.assert_called_once_with(ammendment)
    mock_db_session.commit.assert_called_once()

def test_get_booking_ammendment(booking_repository, mock_db_session):
    ammendment = MagicMock()
    ammendment.BookingId = 1
    booking = MagicMock()
    booking.UserId = 1
    booking.JourneyId = 1
    passenger = MagicMock()
    journey = MagicMock()
    journey.UserId = 2
    driver = MagicMock()

    mock_db_session.query.return_value.get.return_value = ammendment

    booking_repository.GetBookingById = MagicMock(return_value=booking)
    booking_repository.GetUser = MagicMock(side_effect=[passenger, driver])
    booking_repository.GetJourney = MagicMock(return_value=journey)

    result = booking_repository.GetBookingAmmendment(1)
    assert result == (ammendment, driver, passenger, journey)
    mock_db_session.query.assert_called_with(BookingAmmendment)

def test_calculate_driver_rating_no_bookings(booking_repository, mock_db_session):
    mock_db_session.query.return_value.join.return_value.filter.return_value.count.side_effect = [0, 0]
    driver_mock = MagicMock(UserRating=None)
    mock_db_session.query.return_value.get.return_value = driver_mock

    booking_repository.CalculateDriverRating(1)

    mock_db_session.query.assert_any_call(Booking)
    assert mock_db_session.query.return_value.join.return_value.filter.return_value.count.call_count == 2
    assert driver_mock.UserRating == -1.0
    mock_db_session.commit.assert_called_once()

def test_calculate_driver_rating_only_pending(booking_repository, mock_db_session):
    mock_db_session.query.return_value.join.return_value.filter.return_value.count.side_effect = [3, 0]
    driver_mock = MagicMock(UserRating=None)
    mock_db_session.query.return_value.get.return_value = driver_mock

    booking_repository.CalculateDriverRating(1)

    assert driver_mock.UserRating == 0.0
    mock_db_session.commit.assert_called_once()

def test_calculate_driver_rating_only_completed(booking_repository, mock_db_session):
    mock_db_session.query.return_value.join.return_value.filter.return_value.count.side_effect = [0, 5]
    driver_mock = MagicMock(UserRating=None)
    mock_db_session.query.return_value.get.return_value = driver_mock

    booking_repository.CalculateDriverRating(1)

    assert driver_mock.UserRating == 1.0
    mock_db_session.commit.assert_called_once()

def test_calculate_driver_rating_mixed_bookings(booking_repository, mock_db_session):
    mock_db_session.query.return_value.join.return_value.filter.return_value.count.side_effect = [2, 8]
    driver_mock = MagicMock(UserRating=None)
    mock_db_session.query.return_value.get.return_value = driver_mock

    booking_repository.CalculateDriverRating(1)

    assert driver_mock.UserRating == 0.8
    mock_db_session.commit.assert_called_once()

def test_calculate_driver_rating_driver_not_found(booking_repository, mock_db_session):
    mock_db_session.query.return_value.get.return_value = None

    with pytest.raises(Exception, match="Driver 1 not found"):
        booking_repository.CalculateDriverRating(1)

    mock_db_session.commit.assert_not_called()
