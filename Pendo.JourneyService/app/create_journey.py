#from .journey_repository import JourneyRepository
#from .journey_repository import JourneyRepository, Journey
from datetime import datetime, timedelta,timezone
#from .PendoDatabase import Journey



'''
class CreateJourneyCommand:

    def __init__(self, request, logger):

        self.journey_repository = JourneyRepository()
        self.request = request
        self.logger = logger

    def Execute(self):

        try:

            user = self.journey_repository.GetUser(self.request.UserId)
            if user is None:
                raise Exception("User not found")

            JourneyToAdd = Journey(
                UserId=user.UserId,
                AdvertisedPrice=3.5,
                CurrencyCode="GBP",
                StartName="Trinity Center",
                StartLong=44.2,
                StartLat=3.5,
                EndName="King's Cross",
                EndLong=45.0,
                EndLat=4.0,
                JourneyType=1,
                StartDate=datetime.datetime.now(timezone.utc),
                RepeatUntil=datetime.datetime.now(timezone.utc) + timedelta(days=30),
                Recurrance="Weekly",
                StartTime=datetime.datetime.now(timezone.utc),
                JourneyStatusId=1,
                MaxPassengers=4,
                RegPlate="AB12 CDE",
                BootWidth=1.2,
                BootHeight=0.8,
                CreateDate=datetime.datetime.now(timezone.utc),
                UpdateDate=datetime.datetime.now(timezone.utc),
                LockedUntil=datetime.datetime.now(timezone.utc)
            )

            self.journey_repository.CreateJourney(JourneyToAdd)
            self.logger.debug(f"Booking DB object created successfully. BookingId: {JourneyToAdd.JourneyId}")

            #return {"Status": "Success", "createTime": datetime.now()}
            return {"Status": "Success"}

        except Exception as e:
            self.logger.error(f"Error creating booking. Error: {str(e)}")
            return {"Status": "Failed", "Error": str(e)}
'''