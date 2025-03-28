# 
# ViewBalance endpoint implementation
# Author: Alexander McCall
#

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
        self.PaymentRepository = PaymentRepository()
        self.logger = logger
        self.UserId = UserId

    def Execute(self):
        """
        Execute method querys a user's balance.
        :return: both balances of the user.
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
                userBalance = self.PaymentRepository.GetUserBalance(self.UserId)

            weekly = self.PaymentRepository.GetWeeklyList(self.UserId)
            if weekly is None:
                raise Exception("Failed to get weekly balance")

            return ViewBalanceResponse(Status="success", NonPending=userBalance.NonPending, Pending=userBalance.Pending, Weekly=weekly)

        except Exception as e:
            self.logger.error(f"Error fetching balance sheet. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))