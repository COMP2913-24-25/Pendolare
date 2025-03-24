from ..returns.PaymentReturns import ViewBalanceResponse, StatusResponse, SingularPaymentMethod, PaymentMethodResponse
import stripe 

class PaymentMethodsCommand:
    """
    PaymentMethodsCommand class is responsible for finding and returning the payment methods of a user.
    """

    def __init__(self, logger, UserId, secret):
        """
        Constructor for PaymentMethodsCommand class.
        :param UserId: Id for requested user balance
        """
        self.logger = logger
        self.UserId = UserId
        self.stripe_secret = secret

    def Execute(self):
        """
        Execute method querys a user's payment method from stripe.
        :return: payment methods of the user.
        """
        try:            
            stripe.api_key = stripe_secret
        
            payment_methods = stripe.Customer.list_payment_methods(str(self.UserId))
            parsedMethods = []

            for method in payment_methods['data']:
                card = method.get("card", {})
                singularMethod = SingularPaymentMethod(
                    Brand=card.get("brand", ""),
                    Funding=card.get("funding", ""),
                    Last4=card.get("last4", ""),
                    Exp_month=card.get("exp_month", 0),
                    Exp_year=card.get("exp_year", 0),
                    PaymentType=method.get("type", "")
                )
                parsedMethods.append(singularMethod)    

            return PaymentMethodResponse(Status="success", Methods=parsedMethods)

        except Exception as e:
            self.logger.error(f"Error fetching payment methods. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))