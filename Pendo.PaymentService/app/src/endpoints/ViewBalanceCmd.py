from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import UserBalance
from ..returns.PaymentReturns import ViewBalanceResponse, StatusResponse

class ViewBalanceCommand:
    """
    ViewBalanceCommand class is responsible for finding and returning the balance of a user.
    """

    def __init__(self, logger, UserId):
        """
        Constructor for ViewBalanceCommand class.
        :param UserId: Id for requested user balance
        """
        self.Payment_Repository = PaymentRepository()
        self.logger = logger
        self.UserId = UserId

    def Execute(self):
        """
        Execute method querys a user's balance.
        :return: both balances of the user.
        """
        try:
            user = self.Payment_Repository.GetUser(self.UserId)
            if user is None:
                raise Exception("User not found")

            self.logger.info("Got user", user)
            
            userBalance = self.Payment_Repository.GetUserBalance(self.UserId)
            if userBalance is None:
                newBalanceSheet = UserBalance(UserId = self.UserId)
                self.Payment_Repository.CreateUserBalance(newBalanceSheet)
                userBalance = self.Payment_Repository.GetUserBalance(self.UserId)

            return ViewBalanceResponse(Status="success", NonPending=userBalance.NonPending, Pending=userBalance.Pending)

        except Exception as e:
            self.logger.error(f"Error fetching balance sheet. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))