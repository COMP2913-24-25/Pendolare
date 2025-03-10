from datetime import datetime, timedelta, timezone  
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import status
from models import Journey, Booking
from typing import List, Dict

class FrequentUsersCommand:
    def __init__(self, db_session: Session, response):
        self.db_session = db_session
        self.response = response

    def execute(self):
        # 7 days??
        try:
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
                    {"user_id": str(user.UserId), "journey_count": user.journey_count}
                    for user in frequent_users
                ]

            return {"frequent_users": response_data}

        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}