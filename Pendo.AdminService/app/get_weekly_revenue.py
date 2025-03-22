from booking_repository import BookingRepository
from response_lib import GetWeeklyRevenueResponse
from fastapi import status
from datetime import datetime
from sqlalchemy import and_

from models import Booking, BookingStatus, Journey, BookingAmmendment

class GetWeeklyRevenueCommand:
    """
    Command to retrieve weekly revenue data for management.
    """

    def __init__(self, db_session, request, response, configuration_provider):
        """
        Initializes the GetWeeklyRevenueCommand.

        Args:
            db_session (Session): SQLAlchemy database session.
            request: FastAPI request object containing start and end dates.
            response (Response): FastAPI response object.
            configuration_provider (ConfigurationProvider): Provider for accessing configuration values.
        """
        self.db_session = db_session
        self.booking_repo = BookingRepository(db_session)
        self.configuration_provider = configuration_provider
        self.request = request
        self.response = response

    def Execute(self):
        """
        Executes the command to retrieve weekly revenue data.

        Returns:
            GetWeeklyRevenueResponse: An object containing labels, data, currency, and total revenue.

        Raises:
            Exception: If an error occurs during database query or processing.
        """
        try:
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

            weekly_revenue_data = self.calculate_management_revenue(bookings, self.request.StartDate)

            labels, data, total = self.get_labels(weekly_revenue_data)
            currency = '£'

            return GetWeeklyRevenueResponse(labels=labels, data=data, currency=currency, total=f"{currency}{float(total):.2f}")

        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}
        
    def calculate_week_number(self, booking_date, start_date_str):
        """
        Calculates the week number for a given booking date relative to a start date.

        Args:
            booking_date (datetime): The booking date.
            start_date_str (str): The start date as a string in "%Y-%m-%d" format.

        Returns:
            int: The week number.
        """
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        return ((booking_date.date() - start_date).days // 7) + 1
    
    def calculate_management_revenue(self, bookings, start_date_str):
        """
        Calculates the weekly revenue data.

        Args:
            bookings (List[Tuple]): List of booking tuples containing booking information.
            start_date_str (str): The start date as a string in "%Y-%m-%d" format.

        Returns:
            Dict[int, float]: A dictionary containing weekly revenue data.
        """
        weekly_revenue = {}

        for booking in bookings:
            # Calculate TotalCost based on proposed price
            total_cost = booking.BookingAmmendment[-1].ProposedPrice if len(booking.BookingAmmendment) != 0 else booking.Journey_.AdvertisedPrice

            booking_fee = float(total_cost) * (booking.FeeMargin / 100)

            week_number = self.calculate_week_number(booking.RideTime, start_date_str)

            if week_number not in weekly_revenue:
                weekly_revenue[week_number] = 0

            weekly_revenue[week_number] += booking_fee

        return weekly_revenue
        
    def get_labels(self, weekly_revenue):
        """
        Generates labels and data for the weekly revenue chart.

        Args:
            weekly_revenue (Dict[int, float]): Dictionary containing weekly revenue data.

        Returns:
            Tuple[List[str], List[float], float]: A tuple containing labels, data, and total revenue.
        """
        labels = []
        data = []
        total = sum(weekly_revenue.values())
        for week_num in sorted(weekly_revenue):
            labels.append(f"WEEK {week_num}")
            data.append(round(weekly_revenue[week_num], 2))
        return labels, data, total