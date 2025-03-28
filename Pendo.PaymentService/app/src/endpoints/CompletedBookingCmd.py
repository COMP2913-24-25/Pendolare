from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction, UserBalance
from ..returns.PaymentReturns import StatusResponse
import datetime
from decimal import Decimal


class CompletedBookingCommand:
    """
    CompletedBookingCommand class is responsible for taking payment once a booking has been completed.
    """

    def __init__(self, logger, BookingId, LatestPrice):
        """
        Constructor for CompletedBookingCommand class.
        :param BookingId
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger

        self.BookingId = BookingId
        self.LatestPrice = LatestPrice
        

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

            booking = self.PaymentRepository.GetBookingById(self.BookingId)
            if not booking:
                self.logger.error(f"Booking not found: {self.BookingId}")
                return StatusResponse(Status="fail", Error="Booking not found")

            try:
                if not hasattr(booking, 'Journey_') or not booking.Journey_:
                    self.logger.error(f"Journey information missing for booking: {self.BookingId}")
                    return StatusResponse(Status="fail", Error="Journey information not available")

                DriverId = booking.Journey_.UserId
            except AttributeError as e:
                self.logger.error(f"Cannot extract driver ID. Error: {e}")
                return StatusResponse(Status="fail", Error="Driver information not available")

            if not DriverId:
                self.logger.error(f"Driver ID is None or empty for booking: {self.BookingId}")
                return StatusResponse(Status="fail", Error="Driver information not available")

            PassengerId = booking.UserId
            AdminFee = booking.FeeMargin

            LatestPrice = Decimal(str(self.LatestPrice))

            self.PaymentRepository.UpdateNonPendingBalance(PassengerId, -1 * LatestPrice)

            passenger_transaction = Transaction(
                UserId = PassengerId, 
                Value = LatestPrice,
                CurrencyCode = "gbp",
                TransactionStatusId = 1,
                TransactionTypeId = 3,
                CreateDate = datetime.datetime.now(),
                UpdateDate = datetime.datetime.now()
            )

            self.PaymentRepository.CreateTransaction(passenger_transaction)

            self.PaymentRepository.UpdatePendingBalance(DriverId, -1 * LatestPrice)

            driver_transaction = Transaction(
                UserId = DriverId, 
                Value = LatestPrice,
                CurrencyCode = "gbp",
                TransactionStatusId = 1,
                TransactionTypeId = 1,
                CreateDate = datetime.datetime.now(),
                UpdateDate = datetime.datetime.now()
            )

            self.PaymentRepository.CreateTransaction(driver_transaction)

            Margin = round(AdminFee * LatestPrice, 2)
            Price = LatestPrice - Margin

            self.PaymentRepository.UpdateNonPendingBalance(DriverId, Price)

            driver_final_transaction = Transaction(
                UserId = DriverId, 
                Value = Price,
                CurrencyCode = "gbp",
                TransactionStatusId = 1,
                TransactionTypeId = 2,
                CreateDate = datetime.datetime.now(),
                UpdateDate = datetime.datetime.now()
            )

            self.PaymentRepository.CreateTransaction(driver_final_transaction)
            self.PaymentRepository.UpdateBookingStatus(self.BookingId, 4)

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error in Completed Booking. BookingId: {self.BookingId}, Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))