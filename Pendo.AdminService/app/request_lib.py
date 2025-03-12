from pydantic import BaseModel
from datetime import datetime

class GetWeeklyRevenueQuery(BaseModel):
    StartDate: str
    EndDate: str

class UpdateBookingFeeRequest(BaseModel):
    FeeMargin: float