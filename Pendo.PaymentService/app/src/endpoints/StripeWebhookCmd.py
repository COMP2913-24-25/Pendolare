# 
# StripeWebhook endpoint implementation
# Author: Alexander McCall
#

from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import UserBalance
from ..returns.PaymentReturns import StatusResponse

class StripeWebhookCommand:
    """
    StripeWebhookCommand class is responsible for handling the response from stripe after a successful charge.
    """

    def __init__(self, logger, UserId, Amount):
        """
        Constructor for StripeWebhookCommand class.
        :param UserId: Id to update balance of
        :param Amount: Value to increase by
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger
        self.UserId = UserId
        self.Amount = Amount

    def Execute(self):
        """
        Execute method updates transaction log and updates a user's balance
        :return: status on completion.
        """
        try:
            user = self.PaymentRepository.GetUser(self.UserId)
            if user is None:
                raise Exception("User not found")

            self.logger.info("Got user")
            
            userBalance = self.PaymentRepository.GetUserBalance(self.UserId)
            if userBalance is None:
                newBalanceSheet = UserBalance(UserId = self.UserId)
                self.PaymentRepository.CreateUserBalance(newBalanceSheet)
            
            #  user_id = None, booking_id = None, amount = None, status = None, typeof = None
            transaction = self.PaymentRepository.GetTransaction(self.UserId, None, self.Amount, 3, 5)
            if transaction is None:
                raise Exception("Transaction not found")
            
            self.PaymentRepository.UpdateTransaction(transaction.TransactionId, self.Amount, 5, 5)
            self.PaymentRepository.UpdateNonPendingBalance(self.UserId, self.Amount)

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error fetching balance sheet. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))