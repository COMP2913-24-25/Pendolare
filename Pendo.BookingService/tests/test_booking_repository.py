import pytest
from unittest.mock import MagicMock, patch
from app.booking_repository import BookingRepository
from app.models import Booking, User, Journey, BookingAmmendment

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def booking_repository(mock_db_session):
    with patch('app.booking_repository.get_db', return_value=iter([mock_db_session])):
        return BookingRepository()

def test_get_bookings_for_user(booking_repository, mock_db_session):
    mock_db_session.query.return_value.filter.return_value.options.return_value.all.return_value = [Booking()]
    result = booking_repository.GetBookingsForUser(1)
    assert len(result) == 1
    mock_db_session.query.assert_called_once_with(Booking)

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