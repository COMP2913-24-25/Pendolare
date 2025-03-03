from .PaymentRepository import PaymentRepository

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
        Execute method creates a new booking.
        :return: both balances of the user.
        """
        try:
            user = self.PaymentRepository.GetUser(self.UserId)
            if user is None:
                raise Exception("User not found")

            self.logger.info("Got user", user)
            
            userBalance = self.PaymentRepository.GetUserBalance(self.UserId)
            if userBalance is None:
                raise Exception("Balance sheet not found")
            else:
                self.logger.info("Got balance sheet", userBalance)
                return userBalance

        except Exception as e:
            self.logger.error(f"Error creating booking. Error: {str(e)}")
            return {"Status": "Failed", "Error": str(e)}