import pytest
from unittest.mock import MagicMock
from app.approve_booking_ammendment import ApproveBookingAmmendmentCommand

class DummyRequest:
    UserId = None
    DriverApproval = False
    PassengerApproval = False

class DummyResponse:
    def __init__(self):
        self.status_code = None

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_email_sender():
    return MagicMock()

@pytest.fixture
def mock_dvla_client():
    client = MagicMock()
    client.GetVehicleDetails.return_value = {"dummy": "data"}
    return client

@pytest.fixture
def mock_payment_service_client():
    return MagicMock()

@pytest.fixture
def mock_repository():
    repo = MagicMock()
    # By default, return a dummy booking ammendment, driver, passenger, journey
    booking_ammendment = MagicMock()
    booking_ammendment.DriverApproval = False
    booking_ammendment.PassengerApproval = False
    booking_ammendment.BookingId = 100
    booking_ammendment.CancellationRequest = False
    driver = MagicMock(UserId=10)
    passenger = MagicMock(UserId=20, Email="passenger@test.com")
    journey = MagicMock(JourneyId=200, VehicleRegistration="ABC123")
    booking = MagicMock(BookingId=100, JourneyId=200, BookingStatusId=1)
    repo.GetBookingAmmendment.return_value = (booking_ammendment, driver, passenger, journey)
    repo.GetBookingById.return_value = booking
    return repo

def get_command(ammendment_id, request, response, logger, email_sender, dvla_client, repository, payment_service_client):
    cmd = ApproveBookingAmmendmentCommand(ammendment_id, request, response, logger, email_sender, dvla_client, payment_service_client)
    cmd.booking_repository = repository
    return cmd

def test_driver_approval(mock_repository, mock_logger, mock_email_sender, mock_dvla_client, mock_payment_service_client):
    req = DummyRequest()
    res = DummyResponse()
    req.UserId = 10
    req.DriverApproval = True
    cmd = get_command(1, req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository, mock_payment_service_client)

    result = cmd.Execute()

    assert result["Status"] == "Success"
    assert "Driver approved" in result["Message"]

def test_passenger_approval(mock_repository, mock_logger, mock_email_sender, mock_dvla_client, mock_payment_service_client):
    req = DummyRequest()
    res = DummyResponse()
    req.UserId = 20
    req.PassengerApproval = True
    cmd = get_command(1, req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository, mock_payment_service_client)

    result = cmd.Execute()

    assert result["Status"] == "Success"
    assert "Passenger approved" in result["Message"]

def test_full_approval(mock_repository, mock_logger, mock_email_sender, mock_dvla_client, mock_payment_service_client):
    booking_ammendment, _, _, _ = mock_repository.GetBookingAmmendment.return_value
    booking_ammendment.DriverApproval = True
    req = DummyRequest()
    res = DummyResponse()
    req.UserId = 20
    req.PassengerApproval = True
    cmd = get_command(1, req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository, mock_payment_service_client)

    result = cmd.Execute()

    mock_repository.UpdateBookingStatus.assert_called_with(booking_ammendment.BookingId, 2)
    mock_email_sender.SendBookingConfirmation.assert_called_once()
    assert result["Status"] == "Success"
    assert "fully approved and applied" in result["Message"]

def test_full_approval_cancellation(mock_repository, mock_logger, mock_email_sender, mock_dvla_client, mock_payment_service_client):
    booking_ammendment, _, _, _ = mock_repository.GetBookingAmmendment.return_value
    booking_ammendment.DriverApproval = True
    booking_ammendment.CancellationRequest = True
    req = DummyRequest()
    res = DummyResponse()
    req.UserId = 20
    req.PassengerApproval = True
    cmd = get_command(1, req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository, mock_payment_service_client)

    result = cmd.Execute()

    mock_repository.UpdateBookingStatus.assert_called_with(booking_ammendment.BookingId, 3)
    assert result["Status"] == "Success"
    assert "cancelled" in result["Message"]

def test_not_authorised(mock_repository, mock_logger, mock_email_sender, mock_dvla_client, mock_payment_service_client):
    req = DummyRequest()
    res = DummyResponse()
    req.UserId = 99  # neither driver (10) nor passenger (20)
    req.DriverApproval = True
    req.PassengerApproval = True
    cmd = get_command(1, req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository, mock_payment_service_client)

    result = cmd.Execute()

    assert result["Status"] == "Error"
    assert res.status_code == 401
    assert f"User {req.UserId} not authorised to approve booking ammendment {cmd.ammendment_id}" in result["Message"]

def test_booking_ammendment_not_found(mock_repository, mock_logger, mock_email_sender, mock_dvla_client, mock_payment_service_client):
    mock_repository.GetBookingAmmendment.return_value = (None, None, None, None)
    req = DummyRequest()
    res = DummyResponse()
    req.UserId = 10
    req.DriverApproval = True
    cmd = get_command(1, req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository, mock_payment_service_client)

    result = cmd.Execute()

    assert result["Status"] == "Error"
    assert res.status_code == 404
    assert f"Booking ammendment {cmd.ammendment_id} not found" in result["Message"]

def test_driver_only_approval(mock_repository, mock_logger, mock_email_sender, mock_dvla_client, mock_payment_service_client):
    req = DummyRequest()
    res = DummyResponse()
    req.UserId = 10
    req.DriverApproval = True
    cmd = get_command(1, req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository, mock_payment_service_client)

    result = cmd.Execute()

    assert result["Status"] == "Success"
    assert "Driver approved booking ammendment" in result["Message"]

def test_passenger_only_approval(mock_repository, mock_logger, mock_email_sender, mock_dvla_client, mock_payment_service_client):
    req = DummyRequest()
    res = DummyResponse()
    req.UserId = 20
    req.PassengerApproval = True
    cmd = get_command(1, req, res, mock_logger, mock_email_sender, mock_dvla_client, mock_repository, mock_payment_service_client)

    result = cmd.Execute()
    
    assert result["Status"] == "Success"
    assert "Passenger approved booking ammendment" in result["Message"]
