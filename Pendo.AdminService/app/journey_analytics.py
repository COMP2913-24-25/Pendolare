#View Data Relating to All Journeys (Available/Booked/Cancelled)

from db_provider import get_db
from sqlalchemy.orm import Session
from models import Journey, Booking, BookingStatus
from fastapi import status
from typing import List, Dict

class JourneyAnalyticsCommand:
        def __init__(self, db_session: Session, response):
            self.db_session = db_session
            self.response = response

        def execute(self):
            try:
                journeys = self.db_session.query(Journey).all()
                journey_data: List[Dict] = []
                available_count = 0  
                cancelled_count = 0

                for journey in journeys:
                    bookings = self.db_session.query(Booking).filter(str(Booking.JourneyId) == str(journey.JourneyId)).all()
                    booking_statuses = []
                    for booking in bookings:
                        booking_status = self.db_session.query(BookingStatus).filter(BookingStatus.BookingStatusId == booking.BookingStatusId).first()
                        if booking_status:
                            booking_statuses.append(booking_status.Status)

                    journey_data.append({
                        "journey_id": str(journey.JourneyId),
                        "user_id": str(journey.UserId),
                        "start_name": journey.StartName,
                        "end_name": journey.EndName,
                        "start_date": str(journey.StartDate),
                        "start_time": str(journey.StartTime),
                        "max_passengers": journey.MaxPassengers,
                        "booking_statuses": booking_statuses
                    })

                return journey_data
            except Exception as e:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"Error": str(e)}