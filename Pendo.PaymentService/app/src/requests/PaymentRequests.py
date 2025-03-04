from pydantic import BaseModel
from ..db.PendoDatabase import User
from uuid import UUID

# class CreateTransaction(BaseModel):
#     UserId: UUID
#     JourneyId: UUID

class GetBalanceRequest(BaseModel):
    UserId: UUID