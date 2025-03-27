from pydantic import BaseModel

class GetWeeklyRevenueQuery(BaseModel):
    StartDate: str
    EndDate: str

class UpdateBookingFeeRequest(BaseModel):
    FeeMargin: float

class CreateDiscountRequest(BaseModel):
    WeeklyJourneys: int
    DiscountPercentage: float