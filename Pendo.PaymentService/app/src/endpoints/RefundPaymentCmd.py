from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction, UserBalance
from ..returns.PaymentReturns import StatusResponse
from datetime import datetime, timedelta

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

            # check if the id is the driver or passenger.

            UserType = self.PaymentRepository.GetUserType(self.CancelledById, self.BookingId)


            DriverId = self.PaymentRepository.GetBookingById(self.booking_id).journey_.UserId

            PassengerId = self.PaymentRepository.GetBookingById(self.booking_id).UserId

            TransactionId = self.GetTransaction(DriverId, bookingId, None, None, None)

            AdminFee = self.PaymentRepository.GetBookingById(self.booking_id).FeeMargin

            

            #Need to make this the right price (may be different from the latest agreed price! and includes a deduction of the admin fee)
            #Fee is the FeeMargin in Booking table

            self.PaymentRepository.UpdatePendingBalance(DriverId, -1 * LatestPrice)


            #Create transaction

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

            
            # reduce driver pending - undo the pendingaddition by it's whole amount
                # this value will be stored as a pending addition type in relation to the bookingid and userid in the transaction table
                # (may be different from the latest agreed price! and includes a deduction of the admin fee)
                # record reduction in transaction table


            if UserType == "Passenger":
                TimeDifference = JourneyTime - CancellationTime
                if TimeDifference > timedelta(minutes=15):
                    #Do nothing?

                    print("Cancellation more than 15 minutes before journey time")
                else:
                    RefundableAmount = LatestPrice * 0.75
                    
                    #Transaction updated

                    self.PaymentRepository.UpdateNonPendingBalance(PassengerId, -1 * RefundableAmount)

                    transaction = Transaction(
                        UserId = PassengerId, 
                        Value = float(RefundableAmount),
                        CurrencyCode = "gbp",
                        TransactionStatusId = 1,
                        TransactionTypeId = 3,
                        CreateDate = datetime.datetime.now(),
                        UpdateDate = datetime.datetime.now()
                    )

                    self.PaymentRepository.CreateTransaction(transaction)

                    NewPrice = 0.75 * LatestPrice
                    Margin = round(AdminFee * NewPrice, 2)
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


                    #UpdatedPassengerNonPendingBalance = self.GetUserBalance(PassengerId).NonPending

                    #self.CreateTransaction(TransactionId, -1 * RefundableAmount, NonPendingAddition, Finalised)

                    ##self.UpdateNonPendingBalance(DriverId, RefundableAmount + AdminFee)

                    #UpdatedDriverPendingBalance = self.GetUserBalance(DriverId).NonPending

                    ##self.UpdateTransaction(TransactionId, RefundableAmount + AdminFee, NonPendingAddition, Finalised)






                   


                
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
        












   