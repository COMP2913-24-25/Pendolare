from pydantic import BaseModel
from ..db.PendoDatabase import User, UserBalance
from uuid import UUID

class ViewBalanceResponse(BaseModel):
    Status : str
    NonPending : float
    Pending : float

class StatusResponse(BaseModel):
    Status: str

class PaymentMethodResponse(BaseModel):
    Status: str
    Methods: list