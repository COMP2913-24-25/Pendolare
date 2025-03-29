# 
# Response bodies for Pendo.PaymentService
# Author: Alexander McCall
#

from pydantic import BaseModel
from ..db.PendoDatabase import User, UserBalance
from uuid import UUID
from typing import Optional

class ViewBalanceResponse(BaseModel):
    Status : str
    NonPending : float
    Pending : float
    Weekly: list

class StatusResponse(BaseModel):
    Status: str
    Error: Optional[str] = None

class SingularPaymentMethod(BaseModel):
    Brand: str
    Funding: str
    Last4: str
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
