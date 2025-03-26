from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction, UserBalance
from ..returns.PaymentReturns import StatusResponse
import datetime

class CreatePayoutCommand:
    """
    CreatePayoutCommand class is responsible for resetting the balance of the user and sending the admin an email
    """

    def __init__(self, logger, UserId):
        """
        Constructor for CreatePayoutCommand class.
        :param UserId
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger

        self.UserId = UserId
        

    def Execute(self):
        """
        Execute method creates a transaction record after refunding items.
        :return: status of operation
        """

        try:
            
            # TODO: Complete Confirm endpoint - Catherine
            
            # call get balance

            # email user with payout amount (non-pending)
            # email admin with notice to payout / invoice to pay

            # reset balance to zero
            # log transaction in db

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error in Payout Balance. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))
        












   
   
   
