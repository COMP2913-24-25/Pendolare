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
                #Retrieve all journeys from Journey table
                journeys = self.db_session.query(Journey).all()
                # List of dictionaries that will store information about individual journeys
                journey_data: List[Dict] = []
                # Two counters are initialinitialised to store number of available journeys and cancelled journeys
                available_count = 0  
                cancelled_count = 0
                booked_count = 0

                # Iterates through all journeys to find available journeys 
                for journey in journeys:
                    bookings = self.db_session.query(Booking).filter(Booking.JourneyId == journey.JourneyId).all()

                    booking_statuses = []
                    is_available = True
                    is_booked = False
                    is_cancelled = False
                    # If there is a booking associated with a journey then loop through booking details to see if booked or cancelled 
                    for booking in bookings:
                        booking_status = self.db_session.query(BookingStatus).filter(BookingStatus.BookingStatusId == booking.BookingStatusId).first()
                        if booking_status:
                            booking_statuses.append(booking_status.Status)
                            if booking_status.Status.lower() == "booked":
                                is_available = False  
                                is_booked = True
                            if booking_status.Status.lower() == "cancelled":
                                is_cancelled = True
                                is_available = False  

                    if is_booked:
                        booked_count += 1
                    if is_cancelled:
                        cancelled_count += 1
                    if is_available and not is_booked and not is_cancelled:
                        available_count += 1
                    
                    

                return {
                "available_journeys": available_count,
                "cancelled_journeys": cancelled_count,
                "booked_journeys": booked_count
            }
            except Exception as e:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                return {"Error": str(e)}