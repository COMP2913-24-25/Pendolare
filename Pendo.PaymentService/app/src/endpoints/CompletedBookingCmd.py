from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction, UserBalance
from ..returns.PaymentReturns import StatusResponse
import datetime

class CompletedBookingCommand:
    """
    CompletedBookingCommand class is responsible for taking payment once a booking has been completed.
    """

    def __init__(self, logger, BookingId):
        """
        Constructor for CompletedBookingCommand class.
        :param BookingId
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger

        self.BookingId = BookingId
        

    def Execute(self):
        """
        Execute method creates a transaction record after refunding items.
        :return: status of operation
        """

        try:
            
            # TODO: Complete Confirm endpoint - Catherine
            
            # input: bookingID

            # decrease booker non-pending by most recent booking value from booking ammendment

            # undo pending addition of driver

            # increase non-pending balance of driver by journey value (minus fee stored in booking!)

            # store transactions in table

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error in Completed Booking. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))
        












   