# 
# RequestPayout endpoint implementation
# Author: Alexander McCall
#
from ..db.PaymentRepository import PaymentRepository
from ..db.PendoDatabase import Transaction, UserBalance
from ..returns.PaymentReturns import StatusResponse
from ..EmailSender import MailSender, generateEmailData
import datetime

class CreatePayoutCommand:
    """
    CreatePayoutCommand class is responsible for resetting the balance of the user and sending the admin an email
    """

    def __init__(self, logger, UserId, sendGridConfig):
        """
        Constructor for CreatePayoutCommand class.
        :param UserId
        """
        self.PaymentRepository = PaymentRepository()
        self.logger = logger

        self.UserId = UserId
        self.sendGridConfig = sendGridConfig

        self.mailer = MailSender(self.sendGridConfig)


    def Execute(self):
        """
        Execute method creates a transaction record after refunding items.
        :return: status of operation
        """

        try:
            # get user and balance sheet
            user = self.PaymentRepository.GetUser(self.UserId)

            if user is None:
                raise Exception("User not found")

            self.logger.info("Got user")
            
            userSheet = self.PaymentRepository.GetUserBalance(user.UserId)

            if userSheet is None:
                self.logger.info("User has no balance sheet, creating")
                newBalanceSheetBooker = UserBalance(UserId = user.UserId)
                self.PaymentRepository.CreateUserBalance(newBalanceSheetBooker)
                userSheet = self.PaymentRepository.GetUserBalance(user.UserId)

            self.logger.info("Got balance sheets")
            
            emailData = generateEmailData(user, userSheet.NonPending)
            self.mailer.SendPayoutEmail(user.Email, emailData)
            self.logger.info("Sent Payout email to user ")

            admins = self.PaymentRepository.GetAdminUsers()
            for admin in admins:
                self.mailer.SendPayoutEmail(admin.Email, emailData)
                self.logger.info("Sent Payout email to admin")

            self.PaymentRepository.UpdateNonPendingBalance(user.UserId, (-1 * userSheet.NonPending))

            advertiserPendingUpdate = Transaction(
                UserId=user.UserId, 
                Value=userSheet.NonPending, 
                CurrencyCode="GBP", 
                TransactionStatusId=1,
                TransactionTypeId=1,
                CreateDate=datetime.datetime.now(),
                UpdateDate=datetime.datetime.now())

            self.PaymentRepository.CreateTransaction(advertiserPendingUpdate)

            return StatusResponse(Status="success")

        except Exception as e:
            self.logger.error(f"Error in Payout Balance. Error: {str(e)}")
            return StatusResponse(Status="fail", Error=str(e))