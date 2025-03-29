import pytest
from unittest.mock import MagicMock
from app.booking_complete import BookingCompleteCommand
from app.statuses.booking_statii import BookingStatus

class DummyRequest:
    UserId = None
    Completed = False

class DummyResponse:
    def __init__(self):
        self.status_code = None

@pytest.fixture
def dummy_request():
    return DummyRequest()

@pytest.fixture
def dummy_response():
    return DummyResponse()

@pytest.fixture
def dummy_logger():
    return MagicMock()

@pytest.fixture
def dummy_payment_service_client():
    return MagicMock()

@pytest.fixture
def dummy_booking_repository():
    repo = MagicMock()
    repo.GetUser.return_value = None
    repo.GetBookingById.return_value = None
    repo.GetJourney.return_value = None
    return repo

@pytest.fixture
def command(dummy_request, dummy_response, dummy_logger, dummy_payment_service_client, dummy_booking_repository):
    cmd = BookingCompleteCommand("dummy_booking_id", dummy_request, dummy_response, dummy_logger, dummy_payment_service_client)
    cmd.booking_repository = dummy_booking_repository
    return cmd

def test_user_not_found(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger):
    dummy_request.UserId = 1
    dummy_booking_repository.GetUser.return_value = None
    
    result = command.Execute()
    
    assert result.Status == "Failed"
    assert "User 1 not found" in result.Message
    assert dummy_response.status_code == 404
    dummy_logger.error.assert_called_with("User 1 not found")

def test_booking_not_found(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger):
    dummy_request.UserId = 2
    user = MagicMock(UserId=2)
    dummy_booking_repository.GetUser.return_value = user
    dummy_booking_repository.GetBookingById.return_value = None
    
    result = command.Execute()
    
    assert result.Status == "Failed"
    assert "Booking dummy_booking_id not found" in result.Message
    assert dummy_response.status_code == 404
    dummy_logger.error.assert_called_with("Booking dummy_booking_id not found")

def test_driver_pending_completion_success(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger):
    dummy_request.UserId = 10
    user = MagicMock(UserId=10)
    dummy_booking_repository.GetUser.return_value = user
    booking = MagicMock(BookingId="dummy_booking_id", JourneyId="journey_1", UserId=9, BookingStatusId=BookingStatus.Confirmed)
    dummy_booking_repository.GetBookingById.return_value = booking
    journey = MagicMock(JourneyId="journey_1", UserId=10)
    dummy_booking_repository.GetJourney.return_value = journey
    
    result = command.Execute()
    
    dummy_booking_repository.UpdateBookingStatus.assert_called_with("dummy_booking_id", BookingStatus.PendingCompletion)
    assert result.Status == "Success"
    assert "pending completion" in result.Message

def test_driver_booking_not_confirmed(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger):
    dummy_request.UserId = 10
    user = MagicMock(UserId=10)
    dummy_booking_repository.GetUser.return_value = user
    booking = MagicMock(BookingId="dummy_booking_id", JourneyId="journey_1", BookingStatusId=BookingStatus.NotCompleted)
    dummy_booking_repository.GetBookingById.return_value = booking
    journey = MagicMock(JourneyId="journey_1", UserId=10)
    dummy_booking_repository.GetJourney.return_value = journey
    
    result = command.Execute()
    
    assert result.Status == "Failed"
    assert "Booking is not confirmed" in result.Message
    assert dummy_response.status_code == 400
    dummy_logger.error.assert_called_with("Booking is not confirmed. Cannot complete booking.")

def test_passenger_completed_success(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger, dummy_payment_service_client):
    dummy_request.UserId = 20
    dummy_request.Completed = True
    user = MagicMock(UserId=20)
    dummy_booking_repository.GetUser.return_value = user
    booking = MagicMock(BookingId="dummy_booking_id", JourneyId="journey_2", BookingStatusId=BookingStatus.PendingCompletion)
    booking.UserId = 20
    dummy_booking_repository.GetBookingById.return_value = booking
    dummy_booking_repository.GetBookingsForUser.return_value = [{"Journey": {"JourneyType": 1, "Price": 20}}]
    journey = MagicMock(JourneyId="journey_2", UserId=99, JourneyType=1)
    dummy_booking_repository.GetJourney.return_value = journey
    dummy_payment_service_client.CompletedBookingRequest.return_value = True
    
    result = command.Execute()
    
    dummy_booking_repository.UpdateBookingStatus.assert_any_call("dummy_booking_id", BookingStatus.Completed)
    dummy_payment_service_client.CompletedBookingRequest.assert_called_with("dummy_booking_id", 20)
    assert result.Status == "Success"
    assert "completed successfully" in result.Message

def test_passenger_completed_failure(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger, dummy_payment_service_client):
    dummy_request.UserId = 20
    dummy_request.Completed = True
    user = MagicMock(UserId=20)
    dummy_booking_repository.GetUser.return_value = user
    booking = MagicMock(BookingId="dummy_booking_id", JourneyId="journey_2", BookingStatusId=BookingStatus.PendingCompletion)
    booking.UserId = 20
    dummy_booking_repository.GetBookingById.return_value = booking
    journey = MagicMock(JourneyId="journey_2", UserId=99)
    dummy_booking_repository.GetJourney.return_value = journey
    dummy_payment_service_client.CompletedBookingRequest.return_value = False
    
    result = command.Execute()
    
    dummy_booking_repository.UpdateBookingStatus.assert_any_call("dummy_booking_id", BookingStatus.NotCompleted)
    assert result.Status == "Failed"
    assert "Payment service returned an error" in result.Message

def test_passenger_not_completed(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger):
    dummy_request.UserId = 20
    dummy_request.Completed = False
    user = MagicMock(UserId=20)
    dummy_booking_repository.GetUser.return_value = user
    booking = MagicMock(BookingId="dummy_booking_id", JourneyId="journey_2", BookingStatusId=BookingStatus.PendingCompletion)
    booking.UserId = 20
    dummy_booking_repository.GetBookingById.return_value = booking
    journey = MagicMock(JourneyId="journey_2", UserId=99)
    dummy_booking_repository.GetJourney.return_value = journey
    
    result = command.Execute()
    
    dummy_booking_repository.UpdateBookingStatus.assert_called_with("dummy_booking_id", BookingStatus.NotCompleted)
    assert result.Status == "Success"
    assert "not completed" in result.Message

def test_unauthorized_user(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger):
    dummy_request.UserId = 30
    user = MagicMock(UserId=30)
    dummy_booking_repository.GetUser.return_value = user
    booking = MagicMock(BookingId="dummy_booking_id", JourneyId="journey_3", BookingStatusId=BookingStatus.Confirmed)
    booking.UserId = 20
    dummy_booking_repository.GetBookingById.return_value = booking
    journey = MagicMock(JourneyId="journey_3", UserId=10)
    dummy_booking_repository.GetJourney.return_value = journey
    
    result = command.Execute()
    
    assert result.Status == "Failed"
    assert "not authorised" in result.Message
    assert dummy_response.status_code == 401
    dummy_logger.error.assert_called_with("User 30 not authorised to complete booking dummy_booking_id")

def test_exception_handling(command, dummy_request, dummy_response, dummy_booking_repository, dummy_logger):
    dummy_request.UserId = 1
    dummy_booking_repository.GetUser.side_effect = Exception("Unexpected error")
    
    result = command.Execute()
    
    assert result.Status == "Failed"
    assert "Error completing booking" in result.Message
    assert dummy_response.status_code == 500
    dummy_logger.error.assert_called()