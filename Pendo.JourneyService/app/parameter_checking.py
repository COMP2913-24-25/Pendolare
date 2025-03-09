from .request_lib import CreateJourneyRequest
from fastapi import status
#from . import logger_details
from datetime import datetime
import datetime

class CheckJourneyData:
    def __init__(self, request):
        self.request = request

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
                # logger_details.error(f"{field} is None")
                raise Exception(error_message)

        if self.request.JourneyType == 2:
            required_type_2_fields = {
                'Recurrance': "Recurrance is required for JourneyType 2.",
                'ReturnUntil': "ReturnUntil is required for JourneyType 2."
            }
            for field, error_message in required_type_2_fields.items():
                if getattr(self.request, field) is None:
                    # logger_details.error(f"{field} is None for JourneyType 2")
                    raise Exception(error_message)
        elif self.request.JourneyType == 1:
            self.request.RepeatUntil = datetime.datetime(9999, 12, 31, 23, 59, 59)

        return self.request
