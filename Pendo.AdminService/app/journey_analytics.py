#View Data Relating to All Journeys (Available/Booked/Cancelled)

from sqlalchemy import func
from sqlalchemy.orm import Session
from models import Journey, Booking, BookingStatus
from fastapi import status
from datetime import datetime
from response_lib import JourneyAnalyticsResponse

class JourneyAnalyticsCommand:
        def __init__(self, db_session: Session, response, logger):
            self.db_session = db_session
            self.response = response
            self.logger = logger

        def Execute(self) -> JourneyAnalyticsResponse:
            try:
                # Get:
                # - Number of available journeys (JourneyStatus = 1, not in past)
                # - Number of cancelled bookings (BookingStatus = "Cancelled")
                # - Number of booked bookings (BookingStatus = "Pending" / "Confirmed") & Not in past
                # - Number of past bookings

                self.logger.info("Getting journey analytics")

                available_count = self.db_session.query(
                    func.count(Journey.JourneyId)
                ).filter(Journey.JourneyStatusId == 1).scalar()

                self.logger.debug(f"Available journeys: {available_count}")

                cancelled_count = self.db_session.query(func.count(Booking.BookingId))\
                    .join(BookingStatus, Booking.BookingStatusId == BookingStatus.BookingStatusId)\
                    .filter(BookingStatus.Status == "Cancelled").scalar()
                
                self.logger.debug(f"Cancelled bookings: {cancelled_count}")
                
                booked_count = self.db_session.query(func.count(Booking.BookingId))\
                    .join(BookingStatus, Booking.BookingStatusId == BookingStatus.BookingStatusId)\
                    .filter(BookingStatus.Status.in_(["Pending", "Confirmed"]),
                            Booking.RideTime > datetime.now()).scalar()
                
                self.logger.debug(f"Booked bookings: {booked_count}")
                
                past_count = self.db_session.query(func.count(Booking.BookingId))\
                    .join(BookingStatus, Booking.BookingStatusId == BookingStatus.BookingStatusId)\
                    .filter(BookingStatus.Status.in_(["Pending", "Confirmed"]), 
                            Booking.RideTime < datetime.now()).scalar()
                
                self.logger.debug(f"Past bookings: {past_count}")

                response = JourneyAnalyticsResponse(
                    AvailableJourneys=available_count,
                    CancelledBookings=cancelled_count,
                    BookedBookings=booked_count,
                    PastBookings=past_count
                )

                self.logger.info("Journey analytics retrieved successfully: %s", response)

                return response
            
            except Exception as e:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"Error": str(e)}