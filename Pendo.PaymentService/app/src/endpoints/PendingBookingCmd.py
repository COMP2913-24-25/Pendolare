from ..db.PaymentRepository import PaymentRepository

class PendingBookingCommand:
    """
    PendingBookingCommand class is responsible for creating a transaction record when a booking becomes pending.
    """

    def __init__(self, logger, UserId):
        """
        Constructor for PendingBookingCommand class.
        :param UserId
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger
        self.UserId = UserId

    def Execute(self):
        """
        Execute method creates a transaction record on pending booking
        :return: both balances of the user.
        """