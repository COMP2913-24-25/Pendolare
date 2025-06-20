from booking_repository import BookingRepository
from response_lib import GetWeeklyRevenueResponse
from fastapi import status
from datetime import datetime
from sqlalchemy import and_

from models import Booking, BookingStatus, Journey, BookingAmmendment

class GetWeeklyRevenueCommand:

    def __init__(self, db_session, request, response, configuration_provider, logger):
        self.db_session = db_session
        self.booking_repo = BookingRepository(db_session)
        self.configuration_provider = configuration_provider
        self.request = request
        self.response = response
        self.logger = logger

    def Execute(self):
        """
        Get the weekly revenue from the database.
        """
        try:
            self.logger.info("Getting weekly revenue data...")

            bookings = self.db_session.query(
                Booking,
                BookingStatus.Status,
                Journey.AdvertisedPrice,
                BookingAmmendment.ProposedPrice
            ).join(
                BookingStatus, Booking.BookingStatusId == BookingStatus.BookingStatusId
            ).join(
                Journey, Booking.JourneyId == Journey.JourneyId
            ).outerjoin(
                BookingAmmendment,
                and_(
                    Booking.BookingId == BookingAmmendment.BookingId,
                    BookingAmmendment.DriverApproval == True,
                    BookingAmmendment.PassengerApproval == True
                )
            ).filter(
                Booking.RideTime >= datetime.strptime(self.request.StartDate, "%Y-%m-%d"),
                Booking.RideTime <= datetime.strptime(self.request.EndDate, "%Y-%m-%d")
            ).all()

            self.logger.debug("Retrieved bookings data successfully")

            weekly_revenue_data = self.calculate_management_revenue(bookings, self.request.StartDate)

            self.logger.info("Calculated weekly revenue data successfully")

            labels, data, total = self.get_labels(weekly_revenue_data)
            currency = '£'

            return GetWeeklyRevenueResponse(labels=labels, data=data, currency=currency, total=f"{currency}{float(total):.2f}")

        except Exception as e:
            self.logger.error("Error in GetWeeklyRevenueCommand Execute method: %s", str(e))
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}
        
    def calculate_week_number(self, booking_date, start_date_str):
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        return ((booking_date.date() - start_date).days // 7) + 1
    
    def calculate_management_revenue(self, bookings, start_date_str):
        weekly_revenue = {}

        for booking in bookings:
            # Unpack the tuple elements
            booking_obj, status, advertised_price, proposed_price = booking
            
            # Use proposed_price if available, otherwise fall-back to advertised_price
            total_cost = proposed_price if proposed_price is not None else advertised_price

            booking_fee = float(total_cost) * float(booking_obj.FeeMargin) / 100
            week_number = self.calculate_week_number(booking_obj.RideTime, start_date_str)

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
