from pydantic import BaseModel
from datetime import datetime

class GetWeeklyRevenueRequest(BaseModel):
    StartDate: datetime
    EndDate: datetime