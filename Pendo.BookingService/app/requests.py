from pydantic import BaseModel
from .models import Booking
from uuid import UUID

class CreateBookingRequest(BaseModel):
    UserId: UUID
    JourneyId: UUID

class GetBookingsRequest(BaseModel):
    UserId: UUID