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
            
            # input: CompletedBookingRequest
            # schema:
                # BookingId: UUID
                # LatestPrice: float

            PassengerId = self.PaymentRepository.GetBookingById(self.booking_id).UserId

            DriverId = self.PaymentRepository.GetBookingById(self.booking_id).journey_.UserId

            AdminFee = self.PaymentRepository.GetBookingById(self.booking_id).FeeMargin

            self.PaymentRepository.UpdateNonPendingBalance(PassengerId, -1 * LatestPrice)

            transaction = Transaction(
                        UserId = PassengerId, 
                        Value = float(LatestPrice),
                        CurrencyCode = "gbp",
                        TransactionStatusId = 1,
                        TransactionTypeId = 3,
                        CreateDate = datetime.datetime.now(),
                        UpdateDate = datetime.datetime.now()
                    )

            self.PaymentRepository.CreateTransaction(transaction)

            #admin fee?

            self.PaymentRepository.UpdatePendingBalance(DriverId, -1 * LatestPrice)

            transaction = Transaction(
                        UserId = DriverId, 
                        Value = float(LatestPrice),
                        CurrencyCode = "gbp",
                        TransactionStatusId = 1,
                        TransactionTypeId = 1,
                        CreateDate = datetime.datetime.now(),
                        UpdateDate = datetime.datetime.now()
                    )

            self.PaymentRepository.CreateTransaction(transaction)

            Margin = round(AdminFee * LatestPrice, 2)
            Price = NewPrice - Margin

            self.PaymentRepository.UpdateNonPendingBalance(DriverId, Price)

            transaction = Transaction(
                        UserId = DriverId, 
                        Value = float(Price),
                        CurrencyCode = "gbp",
                        TransactionStatusId = 1,
                        TransactionTypeId = 2,
                        CreateDate = datetime.datetime.now(),
                        UpdateDate = datetime.datetime.now()
                    )

            self.PaymentRepository.CreateTransaction(transaction)

            


            # decrease booker non-pending by most recent booking value from booking ammendment

            # undo pending addition of driver

            # increase non-pending balance of driver by journey value (minus fee stored in booking!)

            # store transactions in table

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error in Completed Booking. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))
        












   