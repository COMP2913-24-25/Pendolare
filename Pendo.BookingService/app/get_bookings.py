from .booking_repository import BookingRepository, Booking
from datetime import datetime

class GetBookingsCommand:
    """
    GetBookingsCommand class is responsible for getting all bookings for a user.
    """

    def __init__(self, userId, logger):
        """
        Constructor for GetBookingCommand class.
        :param request: Request object containing the booking details.
        """
        self.booking_repository = BookingRepository()
        self.userId = userId
        self.logger = logger

    def Execute(self):
        """
        Execute method gets all bookings for a user.
        :return: Response object containing the status of the operation.
        """
        self.logger.debug(f"Getting bookings for user {self.userId}.")
        bookings = self.booking_repository.GetBookingsForUser(self.userId)
        self.logger.debug(f"Retrieved [{0 if bookings is None else len(bookings)}] Bookings for user {self.userId} successfully.")

        return bookings if bookings is not None else []