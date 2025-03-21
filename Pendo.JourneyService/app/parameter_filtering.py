from .request_lib import GetJourneysRequest
from .PendoDatabase import Journey
from sqlalchemy.sql import and_
import math
from datetime import timedelta

class FilterJourneys:
    """
    FilterJourneys class is responsible for creating a filtering statement for journeys based on the request
    """
    def __init__(self, request : GetJourneysRequest, db):
        self.request = request
        self.db = db

    def apply_filters(self):
        filters = []

        # Don't show the user their own journeys!
        filters.append(Journey.UserId != self.request.UserId)

        if self.request.MaxPrice is not None and self.request.MaxPrice > 0:
            filters.append(Journey.AdvertisedPrice <= self.request.MaxPrice)

        if self.request.BootHeight is not None and self.request.BootHeight > 0:
            filters.append(Journey.BootHeight >= self.request.BootHeight)

        if self.request.BootWidth is not None and self.request.BootWidth > 0:
            filters.append(Journey.BootWidth >= self.request.BootWidth)

        if self.request.JourneyType is not None:
            if self.request.JourneyType == 1:
                filters.append(Journey.JourneyType == 1)
            elif self.request.JourneyType == 2:
                filters.append(Journey.JourneyType == 2)
        
        if self.request.NumPassengers is not None:
            filters.append(Journey.MaxPassengers >= self.request.NumPassengers)

        if self.request.StartDate is not None:
            filters.append(and_(Journey.StartDate >= self.request.StartDate, Journey.StartDate < (self.request.StartDate + timedelta(days=1))))

        if self.request.StartLat and self.request.StartLong:
            lat_diff = self.request.DistanceRadius / 111.0
            long_diff = self.request.DistanceRadius / (111.0 * math.cos(math.radians(self.request.StartLat)))
            filters.append(
                and_(
                    Journey.StartLat.between(self.request.StartLat - lat_diff, self.request.StartLat + lat_diff),
                    Journey.StartLong.between(self.request.StartLong - long_diff, self.request.StartLong + long_diff)
                )
            )

        if self.request.EndLat and self.request.EndLong:
            lat_diff = self.request.DistanceRadius / 111.0
            long_diff = self.request.DistanceRadius / (111.0 * math.cos(math.radians(self.request.EndLat)))
            filters.append(
                and_(
                    Journey.EndLat.between(self.request.EndLat - lat_diff, self.request.EndLat + lat_diff),
                    Journey.EndLong.between(self.request.EndLong - lat_diff, self.request.EndLong + long_diff)
                )
            )

        filters.append(Journey.JourneyStatusId == 1)


        return filters
