from pydantic import BaseModel
import datetime
from typing import Optional
from uuid import UUID

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

class CreateJourneyRequest(BaseModel):
    UserId: UUID
    AdvertisedPrice: Optional[float] = 0
    StartName: Optional[str] = None
    StartLong: Optional[float] = 0
    StartLat: Optional[float] = 0
    EndName: Optional[str] = None
    EndLong: Optional[float] = 0
    EndLat: Optional[float] = 0
    StartDate: Optional[datetime.datetime] = None
    RepeatUntil: Optional[datetime.datetime] = datetime.datetime(2025, 3, 9, 21, 33)
    StartTime: Optional[datetime.datetime] = None
    MaxPassengers: Optional[int] = 0
    RegPlate: Optional[str] = None
    CurrencyCode: Optional[str] = "GBP"
    JourneyType: Optional[int] = 0
    Recurrance: Optional[str] = None
    JourneyStatusId: int = 1
    BootWidth: Optional[float] = None
    BootHeight: Optional[float] = None
    LockedUntil: Optional[datetime.datetime] = None