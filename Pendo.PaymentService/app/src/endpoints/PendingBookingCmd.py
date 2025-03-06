from ..db.PaymentRepository import PaymentRepository

class PendingBookingCommand:
    """
    PendingBookingCommand class is responsible for creating a transaction record when a booking becomes pending.
    """

    def __init__(self, logger, BookingId):
        """
        Constructor for PendingBookingCommand class.
        :param UserId
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger
        self.BookingId = BookingId

    def Execute(self):
        """
        Execute method creates a transaction record on pending booking
        :return: both balances of the user.
        """
        # TODO: Complete PendingBooking endpoint

        try:
            # get booking
            pendingBooking = self.PaymentRepository.GetBookingById(self.BookingId)
            if pendingBooking is None:
                raise Exception("Booking not found")

            self.logger.info("Got Booking", pendingBooking)

            # ensure that booker has valid payment methods
            # pendingBooking.UserId

            # get fee
            # increase advertiser pending balance by Booking value (minus fee!)
            # pendingBooking.FeeMargin 


            return {"Status" : "success", 
                    "NonPending" : userBalance.NonPending,
                    "Pending" : userBalance.Pending}

        except Exception as e:
            self.logger.error(f"Error fetching balance sheet. Error: {str(e)}")
            return {"Status": "fail",
                    "Error" : str(e)}
        
