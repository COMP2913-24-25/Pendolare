import pytest
from unittest.mock import MagicMock, patch
from app.dvla_api import VehicleEnquiryClient

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def vehicle_enquiry_client(mock_logger):
    return VehicleEnquiryClient(api_key="dummy_api_key", logger=mock_logger)

@patch("app.dvla_api.requests.post")
def test_get_vehicle_details_success(mock_post, vehicle_enquiry_client, mock_logger):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "registrationNumber": "ABC123",
        "make": "Toyota",
        "colour": "Red"
    }
    mock_post.return_value = mock_response

    result = vehicle_enquiry_client.GetVehicleDetails("ABC123")
    assert result == "Red Toyota (ABC123)"
    mock_logger.debug.assert_any_call("Vehicle enquiry request: {'registrationNumber': 'ABC123'}")
    mock_logger.debug.assert_any_call(f"Vehicle enquiry response: {mock_response.json()}")

@patch("app.dvla_api.requests.post")
def test_get_vehicle_details_no_colour(mock_post, vehicle_enquiry_client, mock_logger):
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "registrationNumber": "XYZ789",
        "make": "Honda"
    }
    mock_post.return_value = mock_response

    result = vehicle_enquiry_client.GetVehicleDetails("XYZ789")
    assert result == " Honda (XYZ789)"
    mock_logger.debug.assert_any_call("Vehicle enquiry request: {'registrationNumber': 'XYZ789'}")
    mock_logger.debug.assert_any_call(f"Vehicle enquiry response: {mock_response.json()}")

@patch("app.dvla_api.requests.post")
def test_get_vehicle_details_vehicle_not_found(mock_post, vehicle_enquiry_client, mock_logger):
    mock_response = MagicMock()
    mock_response.json.return_value = {"errors": [{"code": "vehicleNotFound"}]}
    mock_post.return_value = mock_response

    result = vehicle_enquiry_client.GetVehicleDetails("UNKNOWN")
    assert result == "Unknown (UNKNOWN)"
    mock_logger.info.assert_called_once_with("Vehicle 'UNKNOWN' not found")

@patch("app.dvla_api.requests.post")
def test_get_vehicle_details_api_error(mock_post, vehicle_enquiry_client, mock_logger):
    mock_response = MagicMock()
    mock_response.json.return_value = {"errors": [{"code": "apiError"}]}
    mock_post.return_value = mock_response

    result = vehicle_enquiry_client.GetVehicleDetails("ERROR")
    assert result == "Unknown (ERROR)"
    mock_logger.info.assert_called_once_with("Vehicle 'ERROR' not found")
