from .booking_repository import BookingRepository, Booking

class GetBookingsCommand:
    """
    GetBookingsCommand class is responsible for getting all bookings for a user.
    """

    def __init__(self, request, logger):
        """
        Constructor for GetBookingCommand class.
        :param request: Request object containing the booking details.
        """
        self.booking_repository = BookingRepository()
        self.request = request
        self.logger = logger

    def Execute(self):
        """
        Execute method gets all bookings for a user.
        :return: Response object containing the status of the operation.
        """
        self.logger.debug(f"Getting bookings for user {self.request.UserId}.")
        bookings = self.booking_repository.GetBookingsForUser(self.request.UserId, driver_view=self.request.DriverView)
        self.logger.debug(f"Retrieved [{0 if bookings is None else len(bookings)}] Bookings for user {self.request.UserId} successfully.")

        return bookings if bookings is not None else []