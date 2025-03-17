from ..db.PaymentRepository import PaymentRepository
from ..returns.PaymentReturns import StatusResponse

class StripeWebhookCommand:
    """
    ViewBalanceCommand class is responsible for finding and returning the balance of a user.
    """

    def __init__(self, logger, UserId, Amount):
        """
        Constructor for ViewBalanceCommand class.
        :param UserId: Id for requested user balance
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger
        self.UserId = UserId
        self.Amount = Amount

    def Execute(self):
        """
        Execute method querys a user's balance.
        :return: both balances of the user.
        """
        try:
            user = self.PaymentRepository.GetUser(self.UserId)
            if user is None:
                raise Exception("User not found")

            self.logger.info("Got user", user)
            
            userBalance = self.PaymentRepository.GetUserBalance(self.UserId)
            if userBalance is None:
                newBalanceSheet = UserBalance(UserId = self.UserId)
                self.PaymentRepository.CreateUserBalance(newBalanceSheet)
                
            transaction = self.PayementRepository.GetTransaction(self.UserId, self.Amount, 3, 5)
            if transaction is None:
                raise Exception("Transaction not found")
            
            self.PaymentRepository.UpdateTransaction(transaction.TransactionId, self.Amount, 5, 5)
            self.PaymentRepository.UpdateNonPendingBalance(self.UserId, self.Amount)

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error fetching balance sheet. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))