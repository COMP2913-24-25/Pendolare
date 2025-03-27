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
            results = self.db_session.query(
                Journey,
                Booking,
                BookingStatus
            )\
            .outerjoin(Booking, Journey.JourneyId == Booking.JourneyId)\
            .outerjoin(BookingStatus, BookingStatus.BookingStatusId == Booking.BookingStatusId)\
            .all()

            journey_flags = {}
            for journey, booking, booking_status in results:
                if journey.JourneyId not in journey_flags:
                    journey_flags[journey.JourneyId] = {"booked": False, "cancelled": False, "available": True}
                if booking and booking_status:
                    status_lower = booking_status.Status.lower()
                    if status_lower == "booked":
                        journey_flags[journey.JourneyId]["booked"] = True
                        journey_flags[journey.JourneyId]["available"] = False
                    if status_lower == "cancelled":
                        journey_flags[journey.JourneyId]["cancelled"] = True
                        journey_flags[journey.JourneyId]["available"] = False

            available_count = sum(1 for flags in journey_flags.values() if flags["available"] and not flags["booked"] and not flags["cancelled"])
            booked_count = sum(1 for flags in journey_flags.values() if flags["booked"])
            cancelled_count = sum(1 for flags in journey_flags.values() if flags["cancelled"])

            return {
                "available_journeys": available_count,
                "cancelled_journeys": cancelled_count,
                "booked_journeys": booked_count
            }
        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}