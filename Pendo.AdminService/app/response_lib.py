from pydantic import BaseModel
from typing import List

class GetWeeklyRevenueResponse(BaseModel):
    """
    GetWeeklyRevenueResponse is the response object for the GetWeeklyRevenueCommand.
    Please note, this must remain in this format as it is used directly by the dashboard graphs.
    """
    labels: List[str]
    data: List[float]
    currency: str
    total: str

class JourneyAnalyticsResponse(BaseModel):
    """
    JourneyAnalyticsResponse is the response object for the JourneyAnalyticsCommand.
    """
    AvailableJourneys: int
    CancelledBookings: int
    BookedBookings: int
    PastBookings: int