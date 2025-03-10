import pytest
from unittest.mock import MagicMock
from fastapi import status
from app.confirm_at_pickup import ConfirmAtPickupCommand

class DummyRequest:
    UserId = None

class DummyResponse:
    def __init__(self):
        self.status_code = None

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_email_sender():
    sender = MagicMock()
    sender.SendBookingArrivalEmail.return_value = "Email sent successfully"
    return sender

@pytest.fixture
def mock_dvla_client():
    client = MagicMock()
    client.GetVehicleDetails.return_value = {"vehicle": "details"}
    return client

@pytest.fixture
def mock_repository():
    repo = MagicMock()
    booking = MagicMock()
    booking.BookingStatusId = 2
    booking.JourneyId = "journey1"
    booking.UserId = "passenger1"
    repo.GetBookingById.return_value = booking

    journey = MagicMock()
    journey.UserId = "passenger1"
    journey.RegPlate = "ABC123"
    repo.GetJourney.return_value = journey

    passenger = MagicMock()
    passenger.Email = "passenger@test.com"
    driver = MagicMock()
    repo.GetUser.side_effect = lambda user_id: passenger if user_id == "passenger1" else driver

    return repo

def get_command(booking_id, request, response, logger, email_sender, dvla_client, repository):
    cmd = ConfirmAtPickupCommand(booking_id, request, response, configuration_provider=None, email_sender=email_sender, logger=logger, dvla_client=dvla_client)
    cmd.booking_repository = repository
    return cmd

def test_booking_not_found(mock_repository, mock_logger, mock_email_sender, mock_dvla_client):
    req = DummyRequest()
    req.UserId = "passenger1"
    res = DummyResponse()
    mock_repository.GetBookingById.return_value = None
    cmd = get_command("booking1", req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository)
    result = cmd.Execute()
    assert result["Status"] == "Failed"
    assert result["Message"] == "Booking not found"
    assert res.status_code == status.HTTP_404_NOT_FOUND
    mock_logger.warn.assert_called_with("Booking not found for booking id: booking1")

def test_booking_not_confirmed(mock_repository, mock_logger, mock_email_sender, mock_dvla_client):
    req = DummyRequest()
    req.UserId = "passenger1"
    res = DummyResponse()
    booking = mock_repository.GetBookingById.return_value
    booking.BookingStatusId = 1
    cmd = get_command("booking1", req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository)
    result = cmd.Execute()
    assert result["Status"] == "Failed"
    assert result["Message"] == "Booking is not in confirmed status"
    assert res.status_code == status.HTTP_400_BAD_REQUEST
    mock_logger.warn.assert_called_with("Booking is not in confirmed status for booking id: booking1")

def test_journey_not_found(mock_repository, mock_logger, mock_email_sender, mock_dvla_client):
    req = DummyRequest()
    req.UserId = "passenger1"
    res = DummyResponse()
    mock_repository.GetJourney.return_value = None
    cmd = get_command("booking1", req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository)
    result = cmd.Execute()
    assert result["Status"] == "Failed"
    assert result["Message"] == "Journey not found"
    assert res.status_code == status.HTTP_404_NOT_FOUND
    mock_logger.warn.assert_called_with("Journey not found for booking id: booking1")

def test_user_not_authorised(mock_repository, mock_logger, mock_email_sender, mock_dvla_client):
    req = DummyRequest()
    req.UserId = "unauthorized_user"
    res = DummyResponse()
    cmd = get_command("booking1", req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository)
    result = cmd.Execute()
    assert result["Status"] == "Failed"
    assert result["Message"] == "User not authorised to confirm booking"
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    mock_logger.warn.assert_called_with("User not authorized to confirm booking for booking id: booking1")

def test_successful_confirm_at_pickup(mock_repository, mock_logger, mock_email_sender, mock_dvla_client):
    req = DummyRequest()
    req.UserId = "passenger1"
    res = DummyResponse()
    cmd = get_command("booking1", req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository)
    result = cmd.Execute()
    passenger_email = "passenger@test.com"
    mock_email_sender.SendBookingArrivalEmail.assert_called_once()
    mock_repository.UpdateBookingStatus.assert_called_with("booking1", 4)
    assert result["Status"] == "Success"
    assert result["Message"] == "Booking confirmed successfully"
    mock_logger.debug.assert_any_call("Updating booking status to 'Pending Completion'")

def test_exception_handling(mock_repository, mock_logger, mock_email_sender, mock_dvla_client):
    req = DummyRequest()
    req.UserId = "passenger1"
    res = DummyResponse()
    mock_repository.GetBookingById.side_effect = Exception("Test Exception")
    cmd = get_command("booking1", req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository)
    result = cmd.Execute()
    assert result["Status"] == "Failed"
    assert "Test Exception" in result["Message"]
    assert res.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
