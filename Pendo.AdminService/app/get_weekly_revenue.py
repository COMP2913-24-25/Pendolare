from booking_repository import BookingRepository
from response_lib import GetWeeklyRevenueResponse
from fastapi import status
import datetime

class GetWeeklyRevenueCommand:

    def __init__(self, db_session, request, response, configuration_provider):
        self.db_session = db_session
        self.booking_repo = BookingRepository(db_session)
        self.configuration_provider = configuration_provider
        self.request = request
        self.response = response

    def Execute(self):
        """
        Get the weekly revenue from the database.
        """
        try:
            booking_fee_margin = float(self.configuration_provider.GetSingleValue(self.db_session, "Booking.FeeMargin"))

            bookings = self.booking_repo.GetBookingsInWindow(self.request.StartDate, self.request.EndDate)
            weekly_revenue_data = self.calculate_weekly_revenue(bookings, booking_fee_margin)

            labels = 'Week 1', 'Week 2', 'Week 3', 'Week 4' #work out dynamically from the start and end date
            data = [0, 0, 0, 0] # work out dynamically from the bookings (sum of booking fees)
            total = 352.00
            currency = '£'

            return GetWeeklyRevenueResponse(labels=labels, data=data, currency=currency, total=f"{currency}{float(total):.2f}")

        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}