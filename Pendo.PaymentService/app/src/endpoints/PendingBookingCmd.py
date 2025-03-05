from ..db.PaymentRepository import PaymentRepository

class PendingBookingCommand:
    """
    PendingBookingCommand class is responsible for creating a transaction record when a booking becomes pending.
    """

    def __init__(self, logger, JourneyId):
        """
        Constructor for PendingBookingCommand class.
        :param UserId
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger
        self.JourneyId = JourneyId

    def Execute(self):
        """
        Execute method creates a transaction record on pending booking
        :return: both balances of the user.
        """
        # TODO: Complete PendingBooking endpoint

        # increase advertiser pending balance by journey value (minus fee!)
        try:
            # get journey
            pendingJourney = self.PaymentRepository.GetJourney(self.JourneyId)
            if pendingJourney is None:
                raise Exception("Journey not found")

            self.logger.info("Got journey", user)

            # get fee

            # 


            return {"Status" : "success", 
                    "NonPending" : userBalance.NonPending,
                    "Pending" : userBalance.Pending}

        except Exception as e:
            self.logger.error(f"Error fetching balance sheet. Error: {str(e)}")
            return {"Status": "fail",
                    "Error" : str(e)}
        
