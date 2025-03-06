from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction
from ..returns.PaymentReturns import StatusResponse, PaymentMethodResponse

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
            self.logger.info("Getting booking...")
            pendingBooking = self.PaymentRepository.GetBookingById(self.BookingId)
            if pendingBooking is None:
                raise Exception("Booking not found")

            self.logger.info("Got Booking", pendingBooking)

            # ensure that booker has valid payment methods
            response = PaymentMethodResponse(Status="Success", Methods=["Credit Card", "PayPal", "Bank Transfer"])
            
            if len(response.Methods) == 0:
                raise Exception("No saved payment methods for booking user")
            
            print(pendingBooking)
            # get fee
            # increase advertiser pending balance by Booking value (minus fee!)
            # pendingBooking.FeeMargin 
            # advertiserPendingUpdate = Transaction(UserId=)


            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error fetching balance sheet. Error: {str(e)}")
            return {"Status": "fail",
                    "Error" : str(e)}
        
