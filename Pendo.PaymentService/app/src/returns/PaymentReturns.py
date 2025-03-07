from pydantic import BaseModel
from ..db.PendoDatabase import User, UserBalance
from uuid import UUID

class ViewBalanceResponse(BaseModel):
    Status : str
    NonPending : float
    Pending : float

class StatusResponse(BaseModel):
    Status: str

class SingularPaymentMethod(BaseModel):
    Brand: str
    Funding: str
    Last4: str
    Preferred: str
    Exp_month: int
    Exp_year: int
    PaymentType: str

class PaymentMethodResponse(BaseModel):
    Status: str
    Methods: list[SingularPaymentMethod]

class PaymentSheetResponse(BaseModel):
    Status: str
    PaymentIntent: str
    EphemeralKey: str
    CustomerId: UUID
    PublishableKey: str
