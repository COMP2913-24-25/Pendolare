from .request_lib import GetJourneysRequest
from .PendoDatabase import Journey
from sqlalchemy.sql import and_, or_
import math
from datetime import timedelta, datetime

class FilterJourneys:
    """
    FilterJourneys class is responsible for creating a filtering statement for journeys based on the request
    """
    def __init__(self, request : GetJourneysRequest, db):
        self.request = request
        self.db = db

    def apply_filters(self):
        filters = []

        if self.request.DriverView:
            filters.append(Journey.UserId == self.request.UserId)
        else: 
            filters.append(Journey.UserId != self.request.UserId)

        if self.request.MaxPrice is not None and self.request.MaxPrice > 0:
            filters.append(Journey.AdvertisedPrice <= self.request.MaxPrice)

        if self.request.BootHeight is not None and self.request.BootHeight > 0:
            filters.append(Journey.BootHeight >= self.request.BootHeight)

        if self.request.BootWidth is not None and self.request.BootWidth > 0:
            filters.append(Journey.BootWidth >= self.request.BootWidth)

        if self.request.JourneyType is not None:
            # If specific journey type requested, filter by it
            if self.request.JourneyType == 1:
                filters.append(Journey.JourneyType == 1)
            elif self.request.JourneyType == 2:
                filters.append(Journey.JourneyType == 2)
        else:
            # If no journey type specified, include both types (1 and 2)
            filters.append(or_(Journey.JourneyType == 1, Journey.JourneyType == 2))
        
        if self.request.NumPassengers is not None:
            filters.append(Journey.MaxPassengers >= self.request.NumPassengers)

        # Improved date filtering for commuter journeys
        if self.request.StartDate is not None:
            current_date = datetime.now() if isinstance(self.request.StartDate, str) else self.request.StartDate
            # For commuter journeys, check if they're still active (RepeatUntil >= current_date)
            commuter_date_filter = and_(
                Journey.JourneyType == 2,
                Journey.RepeatUntil >= current_date
            )
            # For single journeys, use the standard date comparison
            single_date_filter = and_(
                Journey.JourneyType == 1,
                Journey.StartDate >= current_date
            )
            # Add the date filter as an OR condition to include both types
            filters.append(or_(commuter_date_filter, single_date_filter))
        
        if self.request.EndDate is not None:
            filters.append(Journey.StartDate <= self.request.EndDate)

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
