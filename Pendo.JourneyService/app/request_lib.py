from pydantic import BaseModel
import datetime
from typing import Optional

class GetJourneysRequest(BaseModel):
    BootHeight: Optional[float] = 0
    BootWidth: Optional[float] = 0
    StartDate: Optional[datetime.datetime] = None
    #JourneyTime: Optional[datetime.datetime] = None
    JourneyType: Optional[int] = 0
    MaxPrice: Optional[float] = 0
    NumPassengers: Optional[int] = 0
    DistanceRadius: Optional[float] = 0
    StartLat: Optional[float] = 0
    StartLong: Optional[float] = 0
    EndLat: Optional[float] = 0
    EndLong: Optional[float] = 0
    SortByPrice: Optional[str] = None

'''
from pydantic import BaseModel
import datetime
from typing import Optional

class GetJourneysRequest(BaseModel):
    OrderByPrice: Optional[str] = None
    DistanceRadius: Optional[float] = None
    StartLat: Optional[float] = None
    StartLong: Optional[float] = None
    EndLong: Optional[float] = None
    EndLat: Optional[float] = None
    BootHeight: Optional[float] = None
    BootWidth: Optional[float] = None
    StartDate: Optional[datetime.datetime] = None
    JourneyTime: Optional[datetime.datetime] = None
    JourneyType: Optional[int] = None
    MaxPrice: Optional[float] = None
    NumPassengers: Optional[int] = None
'''
'''
class GetJourneysRequest(BaseModel):
    OrderByPrice: str
    DistanceRadius: float
    StartLat: float
    StartLong: float
    EndLong: float
    EndLat: float
    BootHeight : float
    BootWidth : float
    StartDate: datetime.datetime
    JourneyTime: datetime.datetime
    JourneyType: int
    MaxPrice: float
    NumPassengers: int
'''
    #Date
    #Time
    #Commuter
    #Start location
    #End location
    #Num Passengers
    #Max Price
    #Longitude
    #StartLatitude
    #EndLatitude
    #EndLongitude
'''
    user_id: UUID
    advertised_price: float
    start_name: str
    start_long: float
    start_lat: float
    end_name: str
    end_long: float
    end_lat: float
    start_date: datetime.datetime
    repeat_until: datetime.datetime
    start_time: datetime.datetime
    max_passengers: int
    reg_plate: str
    currency_code: str = "GBP"
    journey_type: int = 1
    recurrance: Optional[str] = None
    journey_status_id: int = 1
    boot_width: Optional[float] = None
    boot_height: Optional[float] = None
    locked_until: Optional[datetime.datetime] = None
'''

    #ADD MORE FILTERS
    #2023-01-01 12:00:00