from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction, UserBalance
from ..returns.PaymentReturns import StatusResponse
import datetime

class RefundPaymentCommand:
    """
    RefundPaymentCommand class is responsible for refunding a transaction where the booking did not take place.
    """

    def __init__(self, logger, BookingId, CancelledById, LatestPrice, CancellationTime, JourneyTime):
        """
        Constructor for RefundPaymentCommand class.
        :param RefundPaymentRequest
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger

        self.BookingId = BookingId
        self.CancelledById = CancelledById
        self.LatestPrice = LatestPrice
        self.CancellationTime = CancellationTime
        self.JourneyTime = JourneyTime
        

    def Execute(self):
        """
        Execute method creates a transaction record after refunding items.
        :return: status of operation
        """

        try:

            # TODO: Complete refund endpoint - Catherine

            # input: RefundPayementRequest
            # schema:
                # BookingId: UUID
                # CancelledById: UUID
                # LatestPrice: float
                # CancellationTime: datetime
                # JourneyTime: datetime

            # see PendingBookingCmd for useful examples!
            
            # reduce driver pending - undo the pendingaddition by it's whole amount
                # this value will be stored as a pending addition type in relation to the bookingid and userid in the transaction table
                # (may be different from the latest agreed price! and includes a deduction of the admin fee)
                # record reduction in transaction table
                
            # if passenger cancelled

                # less than 15 mins before start?
                    # fullRefund = False
                    # calculate 75% of latest price
                    
                    # subtract 75% of latest price from passenger's non-pending amount
                    # add 75% of latest price (minus the admin fee) to driver's non-pending

                    # record both transactions in table

                # more than 15 mins before start?
                    # do nothing, no payment has ever been taken from them, as payment is only taken after a booking is complete

            # return great success!!

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error in Refund Booking. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))
        












   