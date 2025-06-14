from pydantic import BaseModel, condecimal, confloat
from typing import Optional
from uuid import UUID
from datetime import datetime

class GetBookingsRequest(BaseModel):
    UserId: UUID
    DriverView: bool = False

class AddBookingAmmendmentRequest(BaseModel):
    UserId: UUID
    BookingId: UUID
    ProposedPrice: Optional[condecimal(max_digits=18, decimal_places=8)] = None
    StartName: Optional[str] = None
    StartLong: Optional[confloat()] = None
    StartLat: Optional[confloat()] = None
    EndName: Optional[str] = None
    EndLong: Optional[confloat()] = None
    EndLat: Optional[confloat()] = None
    StartTime: Optional[datetime] = None
    CancellationRequest: bool = False
    DriverApproval: bool = False
    PassengerApproval: bool = False
    Recurrance: Optional[str] = None

class ApproveBookingAmmendmentRequest(BaseModel):
    UserId: UUID
    DriverApproval: bool = False
    PassengerApproval: bool = False
    CancellationRequest: bool = False

class ApproveBookingRequest(BaseModel):
    UserId: UUID

class ConfirmAtPickupRequest(BaseModel):
    UserId: UUID
    JourneyTime: datetime = None

class CreateBookingRequest(BaseModel):
    UserId: UUID
    JourneyId: UUID
    JourneyTime: datetime
    EndCommuterWindow: Optional[datetime] = None # Only required for commuter journeys - the end of the window for the current booking period

class CompleteBookingRequest(BaseModel):
    UserId: UUID
    Completed: bool

class UpdateBookingStatusRequest(BaseModel):
    BookingId: UUID
    Status: str
