from pydantic import BaseModel
from ..db.PendoDatabase import User, UserBalance
from uuid import UUID
from datetime import datetime

class GetwithUUID(BaseModel):
    UserId: UUID

class CompletedBookingRequest(BaseModel):
    BookingId: UUID
    LatestPrice: float

class PaymentSheetRequest(BaseModel):
    UserId: UUID
    Amount: float

class RefundPaymentRequest(BaseModel):
    BookingId: UUID
    CancelledById: UUID
    LatestPrice: float
    CancellationTime: datetime
    JourneyTime: datetime

class CompletedBookingRequest(BaseModel):
    BookingId: UUID
    LatestPrice: float