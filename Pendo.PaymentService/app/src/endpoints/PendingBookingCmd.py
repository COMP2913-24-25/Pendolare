from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction
from ..returns.PaymentReturns import StatusResponse, PaymentMethodResponse
from .ViewBalanceCmd import ViewBalanceCommand
import datetime

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
            print(pendingBooking.UserId)
            # ensure that booker has sufficient balance
            passenger = self.PaymentRepository.GetUserBalance()
            driver = self.PaymentRepository.GetUserBalance(pendingBooking.Journey_.UserId)
            margin = round(pendingBooking.FeeMargin * pendingBooking.Journey_.AdvertisedPrice, 2)
            price = pendingBooking.Journey_.AdvertisedPrice - margin
            
            if passenger.NonPending < pendingBooking.Journey_.AdvertisedPrice:
                raise Exception("Not enough user balance to set journey to pending")

            # increase advertiser pending balance by Booking value (minus fee!)
            status = self.PaymentRepository.UpdatePendingBalance(driver.UserId, price)

            advertiserPendingUpdate = Transaction(
                UserId=driver.UserId, 
                Value=price, 
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
        
