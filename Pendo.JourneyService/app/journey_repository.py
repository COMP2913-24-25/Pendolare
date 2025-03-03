from .PendoDatabase import Journey
from datetime import datetime, timedelta
from fastapi import status

class JourneyRepository:

    def __init__(self, db):
        self.db = db

    def get_journeys(self, filter):
        return self.db.query(Journey).filter_by(filter).all()
    
    def lock_journey(self, JourneyId, response):
        journey = self.db.query(Journey).filter_by(JourneyId=JourneyId).first()

        if journey is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            raise Exception("Cannot lock journey that does not exist.")
        
        if journey.LockedUntil is not None and journey.LockedUntil > datetime.now():
            response.status_code = status.HTTP_401_UNAUTHORIZED
            raise Exception(f"Journey {JourneyId} is already locked.")

        journey.LockedUntil = datetime.now() + timedelta(minutes=10)
        self.db.commit()
        return journey