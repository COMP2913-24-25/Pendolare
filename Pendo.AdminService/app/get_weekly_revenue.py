from booking_repository import BookingRepository
from response_lib import GetWeeklyRevenueResponse
from fastapi import status
from datetime import datetime
from decimal import Decimal

from models import Booking, BookingStatus, Journey, BookingAmmendment

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
            
            bookings = self.db_session.query(
                Booking,
                BookingStatus.Status,
                Journey.AdvertisedPrice,
                BookingAmmendment.ProposedPrice
            ).join(
                BookingStatus, Booking.BookingStatusId == BookingStatus.BookingStatusId
            ).join(
                Journey, Booking.JourneyId == Journey.JourneyId
            ).join(
                BookingAmmendment, Booking.BookingId == BookingAmmendment.BookingId
            ).filter(
                Booking.RideTime >= datetime.strptime(self.request.StartDate, "%Y-%m-%d"),
                Booking.RideTime <= datetime.strptime(self.request.EndDate, "%Y-%m-%d")
            ).all()

            weekly_revenue_data = self.calculate_management_revenue(bookings, booking_fee_margin, self.request.StartDate)

            labels, data, total = self.get_labels(weekly_revenue_data)
            currency = '£'

            return GetWeeklyRevenueResponse(labels=labels, data=data, currency=currency, total=f"{currency}{float(total):.2f}")

        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}
        
    def calculate_week_number(self, booking_date, start_date_str):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        return ((booking_date.date() - start_date).days // 7) + 1
    
    def calculate_management_revenue(self, bookings, fee_margin, start_date_str):
        weekly_revenue = {}

        for booking, status, advertised_price, proposed_price in bookings:
            # Calculate TotalCost based on proposed price
            total_cost = proposed_price

            booking_fee = float(total_cost) * (fee_margin / 100)

            week_number = self.calculate_week_number(booking.RideTime, start_date_str)

            if week_number not in weekly_revenue:
                weekly_revenue[week_number] = 0

            weekly_revenue[week_number] += booking_fee

        return weekly_revenue
        
    def get_labels(self, weekly_revenue):
        labels = []
        data = []
        total = sum(weekly_revenue.values())
        for week_num in sorted(weekly_revenue):
            labels.append(f"WEEK {week_num}")
            data.append(round(weekly_revenue[week_num], 2))
        return labels, data, total

