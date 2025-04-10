from datetime import datetime, timedelta, timezone  
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status
from models import Journey, Booking
from typing import List, Dict

class FrequentUsersCommand:
    """
    Command to retrieve frequent users based on their booking history.
    """
    def __init__(self, db_session: Session, response, logger):
        """
        Initialises the FrequentUsersCommand.

        Args:
            db_session (Session): SQLAlchemy database session.
            response (Response): FastAPI response object.
        """
        self.db_session = db_session
        self.response = response
        self.logger = logger

    def Execute(self):
        try:
            """
        Executes the command to retrieve frequent users who have booked more than 4 journeys in the last 7 days.

        Returns:
            Dict[str, List[Dict[str, str]]]: A dictionary containing a list of frequent users with their user IDs and journey counts.

        Raises:
            Exception: If an error occurs during the database query or processing.
        """
            self.logger.info("Retrieving frequent users...")

            current_date = datetime.now(timezone.utc)

            seven_days_ago = current_date - timedelta(days=7)

            frequent_users = (
                    self.db_session.query(Journey.UserId, func.count(Journey.JourneyId).label("journey_count"))
                    .join(Booking, Journey.JourneyId == Booking.JourneyId)  
                    .filter(Journey.StartDate >= seven_days_ago)  
                    .group_by(Journey.UserId)  
                    .having(func.count(Journey.JourneyId) > 4)  
                    .all()
                )

            response_data: List[Dict] = [
                    {"UserId": str(user.UserId), "JourneyCount": user.journey_count}
                    for user in frequent_users
                ]
            
            self.logger.info("Frequent users retrieved successfully.")

            return {"FrequentUsers": response_data}

        except Exception as e:
            self.logger.error(f"An error occurred while retrieving frequent users: {str(e)}")
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}