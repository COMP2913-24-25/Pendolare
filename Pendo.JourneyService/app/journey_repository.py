from .PendoDatabase import User, Journey
from sqlalchemy.orm import joinedload
from .db_provider import get_db

class JourneyRepository():

    def __init__(self):

        self.db_session = next(get_db())

    def GetUser(self, user_id):
        return self.db_session.query(User).get(user_id)
    
    def CreateJourney(self, journey):

        self.db_session.add(journey)
        self.db_session.commit()
    
    def GetAllJourneys(self):
        return self.db_session.query(Journey).all()

    
