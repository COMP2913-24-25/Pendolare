from pydantic import BaseModel
from ..db.PendoDatabase import User, UserBalance
from uuid import UUID

# class CreateTransaction(BaseModel):
#     UserId: UUID
#     JourneyId: UUID

class GetwithUUID(BaseModel):
    UserId: UUID

class MakePendingBooking(BaseModel):
    BookingId: UUID

class PaymentSheetRequest(BaseModel):
    UserId: UUID
    Amount: float