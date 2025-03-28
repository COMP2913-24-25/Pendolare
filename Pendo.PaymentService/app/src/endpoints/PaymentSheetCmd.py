from ..returns.PaymentReturns import PaymentSheetResponse, StatusResponse
from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabaseProvider import configProvider
from ..db.PendoDatabase import Transaction
import stripe, datetime

class PaymentSheetCommand:
    """
    PaymentSheetCommand class is responsible for querying a user from stripe, if non-existant then creating them, and setting up a payment intent with the value specified.
    """

    def __init__(self, logger, UserId, Amount, Secret):
        """
        Constructor for PaymentSheetCommand class.
        :param UserId: Id for requested user balance
        :param Amount: Amount to be charged / added to balance
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger
        self.UserId = UserId
        self.Amount = int(Amount*100)
        self.Secret = Secret

    def Execute(self):
        """
        Execute method querys a user's stripe profile, and creates a payment intent with the amount specified
        :return: payment methods of the user.
        """
        try:            
            stripe.api_key = self.Secret

            user = self.PaymentRepository.GetUser(self.UserId)
            if user is None:
                raise Exception("User not found")

            # fetch customer
            customer = stripe.Customer.retrieve(str(user.UserId))

            if customer is not None:
                return self.CreateIntents(user)

        except stripe.error.InvalidRequestError as e:
            # handle the "No such customer" error
            if "No such customer" in str(e):
                # customer doesn't exist
                
                customer = stripe.Customer.create(
                    id = user.UserId, 
                    name = user.FirstName + " " + user.LastName,
                    email = user.Email
                )

                return self.CreateIntents(user)
                
            else:
                self.logger.error(f"An invalid request error occurred: {e}")
                return StatusResponse(Status="fail", Error=str(e))

        except stripe.error.StripeError as e:
            # handle other Stripe-related errors
            self.logger.error(f"A Stripe error occurred: {e}")
            return StatusResponse(Status="fail", Error=str(e))

        except Exception as e:
            self.logger.error(f"Error creating PaymentSheet. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))

    def CreateIntents(self, user):

        ephemeralKey = stripe.EphemeralKey.create(
            customer = user.UserId,
            stripe_version = "2020-03-02"
        )

        paymentIntent = stripe.PaymentIntent.create(
            amount = self.Amount,
            currency = "gbp",
            payment_method_types=["card"],
            customer = user.UserId,
            receipt_email = user.Email,
            setup_future_usage = "on_session", 
            use_stripe_sdk = True
        )

        transaction = Transaction(
            UserId = user.UserId, 
            Value = float(self.Amount / 100),
            CurrencyCode = "gbp",
            TransactionStatusId = 3,
            TransactionTypeId = 5,
            CreateDate = datetime.datetime.now(),
            UpdateDate = datetime.datetime.now()
        )

        self.PaymentRepository.CreateTransaction(transaction)
        
        return PaymentSheetResponse(
            Status="success", 
            PaymentIntent=paymentIntent.client_secret, 
            EphemeralKey=ephemeralKey.secret, 
            CustomerId=user.UserId, 
            PublishableKey=configProvider.StripeConfiguration.publishable
        )