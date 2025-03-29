# 
# PendingBooking endpoint implementation
# Author: Alexander McCall
#

from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction, UserBalance
from ..returns.PaymentReturns import StatusResponse, PaymentMethodResponse
import datetime

class PendingBookingCommand:
    """
    PendingBookingCommand class is responsible for creating a transaction record when a booking becomes pending.
    """

    def __init__(self, logger, BookingId, LatestAmount):
        """
        Constructor for PendingBookingCommand class.
        :param BookingId
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger
        self.BookingId = BookingId
        self.LatestAmount = LatestAmount

    def Execute(self):
        """
        Execute method creates a transaction record on pending booking
        :return: status of operation
        """

        try:
            # get booking
            self.logger.info("Getting booking...")
            pendingBooking = self.PaymentRepository.GetBookingById(self.BookingId)
            
            if pendingBooking is None:
                raise Exception("Booking not found")

            if pendingBooking.BookingStatus_.Status != "PrePending":
                raise Exception("Not a pending booking")

            self.logger.info("Got Booking")

            Driver = self.PaymentRepository.GetUser(pendingBooking.Journey_.UserId)
            Booker = self.PaymentRepository.GetUser(pendingBooking.UserId)

            if Driver is None:
                raise Exception("Driver not found")

            if Booker is None:
                raise Exception("Passenger not found")

            self.logger.info("Got both users")
            
            # find driver and booker, calculate price and margin
            DriverSheet = self.PaymentRepository.GetUserBalance(Driver.UserId)
            BookerSheet = self.PaymentRepository.GetUserBalance(Booker.UserId)
            Margin = round(float(pendingBooking.FeeMargin) * float(self.LatestAmount), 2)
            Price = self.LatestAmount - Margin

            if DriverSheet is None:
                self.logger.info("Driver has no balance sheet, creating")
                newBalanceSheetDriver = UserBalance(UserId = Driver.UserId)
                self.PaymentRepository.CreateUserBalance(newBalanceSheetDriver)
                DriverSheet = self.PaymentRepository.GetUserBalance(Driver.UserId)

            if BookerSheet is None:
                self.logger.info("Booker has no balance sheet, creating")
                newBalanceSheetBooker = UserBalance(UserId = Booker.UserId)
                self.PaymentRepository.CreateUserBalance(newBalanceSheetBooker)
                BookerSheet = self.PaymentRepository.GetUserBalance(Booker.UserId)

            self.logger.info("Got both balance sheets")

            # ensure that booker has sufficient balance
            if BookerSheet.NonPending < self.LatestAmount:
                raise Exception("Not enough user balance to set journey to pending")

            # increase advertiser pending balance by Booking value (minus fee!)
            Status = self.PaymentRepository.UpdatePendingBalance(Driver.UserId, Price)

            advertiserPendingUpdate = Transaction(
                UserId=Driver.UserId, 
                BookingId=self.BookingId,
                Value=Price, 
                CurrencyCode=pendingBooking.Journey_.CurrencyCode, 
                TransactionStatusId=1,
                TransactionTypeId=1,
                CreateDate=datetime.datetime.now(),
                UpdateDate=datetime.datetime.now())

            self.PaymentRepository.CreateTransaction(advertiserPendingUpdate)

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error in Pending Booking. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))
        
