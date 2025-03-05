from pydantic import BaseModel
from datetime import datetime

class GetWeeklyRevenueQuery(BaseModel):
    StartDate: datetime
    EndDate: datetime