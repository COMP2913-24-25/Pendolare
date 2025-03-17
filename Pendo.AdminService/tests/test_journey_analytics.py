import pytest
from unittest.mock import MagicMock
from fastapi import status
from app.journey_analytics import JourneyAnalyticsCommand

def test_no_journeys():
    mock_db_session = MagicMock()
    mock_db_session.query().all.return_value = [] 
    
    mock_response = MagicMock()
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response)
    result = command.execute()

    assert result["available_journeys"] == 0
    assert result["cancelled_journeys"] == 0
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_no_bookings():
    mock_journey1 = MagicMock(JourneyId="1")
    mock_journey2 = MagicMock(JourneyId="2")
    
    mock_db_session = MagicMock()
    mock_db_session.query().all.return_value = [mock_journey1, mock_journey2]
    mock_db_session.query().filter().all.return_value = []  

    mock_response = MagicMock()
    
    command = JourneyAnalyticsCommand(mock_db_session, mock_response)
    result = command.execute()

    assert result["available_journeys"] == 2
    assert result["cancelled_journeys"] == 0
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_only_booked_bookings():
    mock_journey = MagicMock(JourneyId="1")
    mock_booking = MagicMock(JourneyId="1", BookingStatusId=1)
    mock_booking_status = MagicMock(BookingStatusId=1, Status="booked")

    mock_db_session = MagicMock()
    mock_db_session.query().all.return_value = [mock_journey]
    mock_db_session.query().filter().all.return_value = [mock_booking]
    mock_db_session.query().filter().first.return_value = mock_booking_status

    mock_response = MagicMock()

    command = JourneyAnalyticsCommand(mock_db_session, mock_response)
    result = command.execute()

    assert result["available_journeys"] == 0
    assert result["cancelled_journeys"] == 0
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_only_cancelled_bookings():
    mock_journey = MagicMock(JourneyId="1")
    mock_booking = MagicMock(JourneyId="1", BookingStatusId=1)
    mock_booking_status = MagicMock(BookingStatusId=1, Status="cancelled")

    mock_db_session = MagicMock()
    mock_db_session.query().all.return_value = [mock_journey]
    mock_db_session.query().filter().all.return_value = [mock_booking]
    mock_db_session.query().filter().first.return_value = mock_booking_status

    mock_response = MagicMock()

    command = JourneyAnalyticsCommand(mock_db_session, mock_response)
    result = command.execute()

    assert result["available_journeys"] == 0
    assert result["cancelled_journeys"] == 1
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_journeys_with_mixed_bookings():
    mock_journey = MagicMock(JourneyId="1")
    mock_booking_booked = MagicMock(JourneyId="1", BookingStatusId=1)
    mock_booking_cancelled = MagicMock(JourneyId="1", BookingStatusId=2)
    mock_booking_status_booked = MagicMock(BookingStatusId=1, Status="booked")
    mock_booking_status_cancelled = MagicMock(BookingStatusId=2, Status="cancelled")

    mock_db_session = MagicMock()
    mock_db_session.query().all.return_value = [mock_journey]
    mock_db_session.query().filter().all.return_value = [mock_booking_booked, mock_booking_cancelled]
    mock_db_session.query().filter().first.side_effect = [mock_booking_status_booked, mock_booking_status_cancelled]

    mock_response = MagicMock()

    command = JourneyAnalyticsCommand(mock_db_session, mock_response)
    result = command.execute()

    assert result["available_journeys"] == 0
    assert result["cancelled_journeys"] == 1
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR


def test_case_insensitive_status_check():
    mock_journey = MagicMock(JourneyId="1")
    mock_booking1 = MagicMock(JourneyId="1", BookingStatusId=1)
    mock_booking2 = MagicMock(JourneyId="1", BookingStatusId=2)
    mock_booking3 = MagicMock(JourneyId="1", BookingStatusId=3)
    mock_booking_status1 = MagicMock(BookingStatusId=1, Status="Booked")
    mock_booking_status2 = MagicMock(BookingStatusId=2, Status="CANCELLED")
    mock_booking_status3 = MagicMock(BookingStatusId=3, Status="booked")

    mock_db_session = MagicMock()
    mock_db_session.query().all.return_value = [mock_journey]
    mock_db_session.query().filter().all.return_value = [mock_booking1, mock_booking2, mock_booking3]
    mock_db_session.query().filter().first.side_effect = [
        mock_booking_status1, mock_booking_status2, mock_booking_status3
    ]

    mock_response = MagicMock()

    command = JourneyAnalyticsCommand(mock_db_session, mock_response)
    result = command.execute()

    assert result["available_journeys"] == 0
    assert result["cancelled_journeys"] == 1
    assert mock_response.status_code != status.HTTP_500_INTERNAL_SERVER_ERROR

def test_error_handling():
    mock_db_session = MagicMock()
    mock_db_session.query.side_effect = Exception("Database error")

    mock_response = MagicMock()
    mock_response.status_code = None  

    command = JourneyAnalyticsCommand(mock_db_session, mock_response)
    result = command.execute()

    assert result == {"Error": "Database error"}
    assert mock_response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
