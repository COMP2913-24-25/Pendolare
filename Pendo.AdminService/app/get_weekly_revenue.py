from booking_repository import BookingRepository
from response_lib import GetWeeklyRevenueResponse
from fastapi import status
import datetime
from models import Booking, BookingStatus

# Get weekly revenue for maangement
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

            #bookings = self.booking_repo.GetBookingsInWindow(self.request.StartDate, self.request.EndDate)
            #wweekly_revenue_data = self.calculate_weekly_revenue(bookings, booking_fee_margin)
            bookings = self.db_session.query(Booking, BookingStatus.Status).join(
                BookingStatus, Booking.BookingStatusId == BookingStatus.BookingStatusId
            ).filter(
                Booking.BookingDate >= datetime.strptime(self.request.StartDate, "%Y-%m-%d"),
                Booking.BookingDate <= datetime.strptime(self.request.EndDate, "%Y-%m-%d")
            ).all()

            weekly_revenue_data = self.calculate_weekly_revenue(bookings, booking_fee_margin)

            labels, data, total = self.generate_weekly_labels_and_data(weekly_revenue_data)
            currency = '£'

            return GetWeeklyRevenueResponse(labels=labels, data=data, currency=currency, total=f"{currency}{float(total):.2f}")

        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}
        
    def calculate_week_number(self, booking_date, start)
    def calculate_management_revenue(self, bookings, fee_margin):
        weekly_revenue = {}

        for booking, status in bookings:
            # If there is no cost then calculation would return 0 error
            if booking.TotalCost == None:
                continue
            booking_fee = booking.TotalCost * (fee_margin / 100)
