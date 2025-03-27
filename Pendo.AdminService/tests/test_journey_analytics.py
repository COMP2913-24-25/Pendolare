import pytest
from unittest.mock import MagicMock
from fastapi import status
from datetime import datetime
from app.journey_analytics import JourneyAnalyticsCommand
from response_lib import JourneyAnalyticsResponse

@pytest.fixture
def mock_logger():
    return MagicMock()

@pytest.fixture
def mock_response():
    return MagicMock()

@pytest.fixture
def mock_db_session():
    return MagicMock()

def setup_db_side_effect(mock_db_session, available, cancelled, booked, past):
    query1 = MagicMock()
    query1.filter.return_value.scalar.return_value = available

    query2 = MagicMock()
    query2.join.return_value.filter.return_value.scalar.return_value = cancelled

    query3 = MagicMock()
    query3.join.return_value.filter.return_value.scalar.return_value = booked

    query4 = MagicMock()
    query4.join.return_value.filter.return_value.scalar.return_value = past

    mock_db_session.query.side_effect = [query1, query2, query3, query4]

def test_no_journeys(mock_db_session, mock_response, mock_logger):
    setup_db_side_effect(mock_db_session, available=0, cancelled=0, booked=0, past=0)
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response, mock_logger)
    result = command.Execute()
    
    assert isinstance(result, JourneyAnalyticsResponse)
    assert result.AvailableJourneys == 0
    assert result.CancelledBookings == 0
    assert result.BookedBookings == 0
    assert result.PastBookings == 0
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_available_only(mock_db_session, mock_response, mock_logger):
    setup_db_side_effect(mock_db_session, available=2, cancelled=0, booked=0, past=0)
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response, mock_logger)
    result = command.Execute()
    
    assert result.AvailableJourneys == 2
    assert result.CancelledBookings == 0
    assert result.BookedBookings == 0
    assert result.PastBookings == 0
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_only_cancelled_bookings(mock_db_session, mock_response, mock_logger):
    setup_db_side_effect(mock_db_session, available=1, cancelled=1, booked=0, past=0)
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response, mock_logger)
    result = command.Execute()
    
    assert result.AvailableJourneys == 1
    assert result.CancelledBookings == 1
    assert result.BookedBookings == 0
    assert result.PastBookings == 0
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_only_booked_future_bookings(mock_db_session, mock_response, mock_logger):
    setup_db_side_effect(mock_db_session, available=1, cancelled=0, booked=1, past=0)
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response, mock_logger)
    result = command.Execute()
    
    assert result.AvailableJourneys == 1
    assert result.CancelledBookings == 0
    assert result.BookedBookings == 1
    assert result.PastBookings == 0
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_only_past_bookings(mock_db_session, mock_response, mock_logger):
    setup_db_side_effect(mock_db_session, available=1, cancelled=0, booked=0, past=2)
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response, mock_logger)
    result = command.Execute()
    
    assert result.AvailableJourneys == 1
    assert result.CancelledBookings == 0
    assert result.BookedBookings == 0
    assert result.PastBookings == 2
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_mixed_bookings(mock_db_session, mock_response, mock_logger):
    setup_db_side_effect(mock_db_session, available=3, cancelled=2, booked=1, past=1)
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response, mock_logger)
    result = command.Execute()
    
    assert result.AvailableJourneys == 3
    assert result.CancelledBookings == 2
    assert result.BookedBookings == 1
    assert result.PastBookings == 1
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_error_handling(mock_db_session, mock_response, mock_logger):
    mock_db_session.query.side_effect = Exception("Database error")
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response, mock_logger)
    result = command.Execute()
    
    assert result == {"Error": "Database error"}
    assert mock_response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
