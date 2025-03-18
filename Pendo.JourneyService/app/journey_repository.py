from .PendoDatabase import Journey
from datetime import datetime, timedelta
from fastapi import status

class JourneyRepository:
    """
    JourneyRepository class is responsible for handling database operations for the Journey model
    """
    def __init__(self, db):
        self.db = db

    def get_journeys(self, filters):
        return self.db.query(Journey).filter(*filters)
    
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
    
    def create_journey(self, journey_data):
        journey_dict = journey_data.dict()
        journey = Journey(**journey_dict)
        self.db.add(journey)
        self.db.commit()
        self.db.refresh(journey)
        return journey

    def adjust_journey(self, JourneyId, response):
        journey = self.db.query(Journey).filter_by(JourneyId=JourneyId).first()

        if journey is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            raise Exception("Cannot lock journey that does not exist.")

        if response.AdvertisedPrice == 0:
            response.status_code = status.HTTP_400_BAD_REQUEST
            raise Exception("AdvertisedPrice is incomplete.")

        journey.AdvertisedPrice = response.AdvertisedPrice
        self.db.commit()
        return journey