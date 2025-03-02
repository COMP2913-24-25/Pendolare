from pydantic import BaseModel
from .PendoDatabase import Journey
from uuid import UUID

class CreateJourneyRequest(BaseModel):
    UserId: UUID

class GetJourneysRequest(BaseModel):
    UserId: UUID