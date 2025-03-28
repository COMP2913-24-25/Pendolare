from .request_lib import CreateJourneyRequest
from fastapi import status
from datetime import datetime
import datetime
from .PendoDatabase import Discounts

class CheckJourneyData:
    """
    CheckJourneyData class used to validate the CreateJourneyRequest
    """
    def __init__(self, request, logger, db=None):
        self.request = request
        self.logger = logger
        self.db = db

    def check_inputs(self):
        required_fields = {
            'AdvertisedPrice': "AdvertisedPrice is required.",
            'StartName': "StartName is required.",
            'StartLong': "StartLong is required.",
            'StartLat': "StartLat is required.",
            'EndName': "EndName is required.",
            'EndLong': "EndLong is required.",
            'EndLat': "EndLat is required.",
            'StartDate': "StartDate is required.",
            'StartTime': "StartTime is required.",
            'MaxPassengers': "MaxPassengers is required.",
            'RegPlate': "RegPlate is required.",
            'CurrencyCode': "CurrencyCode is required.",
            'JourneyType': "JourneyType is required.",
            'BootWidth': "BootWidth is required.",
            'BootHeight': "BootHeight is required.",
            'LockedUntil': "LockedUntil is required."
        }

        for field, error_message in required_fields.items():
            if getattr(self.request, field) is None:
                self.logger.error(f"{field} is None")
                raise Exception(error_message)

        if self.request.JourneyType == 2:
            required_type_2_fields = {
                'Recurrance': "Recurrance is required for JourneyType 2.",
                'ReturnUntil': "ReturnUntil is required for JourneyType 2."
            }
            for field, error_message in required_type_2_fields.items():
                if getattr(self.request, field) is None:
                    self.logger.error(f"{field} is None for JourneyType 2")
                    raise Exception(error_message)
            
            # Validate DiscountID for commuter journeys
            if self.request.DiscountID is not None and self.db is not None:
                discount = self.db.query(Discounts).filter_by(DiscountID=self.request.DiscountID).first()
                if discount is None:
                    self.logger.error(f"DiscountID {self.request.DiscountID} does not exist")
                    raise Exception(f"DiscountID {self.request.DiscountID} does not exist")
                self.logger.info(f"Found discount: {discount.DiscountPercentage * 100}% off for {discount.WeeklyJourneys} weekly journeys")
        elif self.request.JourneyType == 1:
            self.request.RepeatUntil = datetime.datetime(9999, 12, 31, 23, 59, 59)

        return self.request
