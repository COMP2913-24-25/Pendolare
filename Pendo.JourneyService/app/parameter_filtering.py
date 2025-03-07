from .request_lib import GetJourneysRequest
from .PendoDatabase import Journey
from datetime import datetime
from sqlalchemy.sql import and_
from geopy.distance import geodesic
import logging

class FilterJourneys:
    def __init__(self, request, db):
        self.request = request
        self.db = db

    def apply_filters(self):
        filters = []

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
            #if self.request.JourneyTime is not None:
                #JourneyStartTime = self.request.JourneyTime.time()
            #else:
                #JourneyStartTime = "00:00:00"
            
            #JourneyStartDate = self.request.StartDate.date()
            #JourneyStartDateTime = datetime.combine(JourneyStartDate, JourneyStartTime)
            #filters.append(Journey.StartDate >= JourneyStartDateTime)
            filters.append(Journey.StartDate >= self.request.StartDate)

        '''
        if self.request.StartLat is not None and self.request.StartLong is not None and self.request.DistanceRadius is not None:
            journeys = self.db.query(Journey).all()
            journey_ids_within_radius = []
            for journey in journeys:
                distance = geodesic((self.request.StartLat, self.request.StartLong), (journey.StartLat, journey.StartLong)).kilometers
                if distance <= self.request.DistanceRadius:
                    journey_ids_within_radius.append(journey.JourneyId)
            filters.append(Journey.JourneyId.in_(journey_ids_within_radius))
        '''

        if self.request.StartLat and self.request.StartLong:
            filters.append(
                and_(
                    Journey.StartLat.between(self.request.StartLat - self.request.DistanceRadius, self.request.StartLat + self.request.DistanceRadius),
                    Journey.StartLong.between(self.request.StartLong - self.request.DistanceRadius, self.request.StartLong + self.request.DistanceRadius)
                )
            )

        if self.request.EndLat and self.request.EndLong:
            filters.append(
                and_(
                    Journey.EndLat.between(self.request.EndLat - self.request.DistanceRadius, self.request.EndLat + self.request.DistanceRadius),
                    Journey.EndLong.between(self.request.EndLong - self.request.DistanceRadius, self.request.EndLong + self.request.DistanceRadius)
                )
            )

        #logger.debug("Applied filters: %s", filters)

        #return and_(*filters)
        return filters