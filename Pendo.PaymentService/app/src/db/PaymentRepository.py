from .PendoDatabase import *
from sqlalchemy.orm import joinedload, with_loader_criteria
import datetime
from .PendoDatabaseProvider import get_db
from decimal import Decimal

class PaymentRepository():
    """
    This class is responsible for handling all the database operations related to bookings
    """

    def __init__(self):
        """
        Constructor for PaymentRepository class.
        """
        self.db_session = next(get_db())

    def __del__(self):
        """
        Destructor for PaymentRepository class.
        """
        self.db_session.close()

    def GetUserBalance(self, user_id):
        """
        GetUserBalance method returns the balance of a user for the specified user id.
        :param user_id: Id of the user.
        :return UserBalance object.
        """
        return self.db_session.query(UserBalance).filter(UserBalance.UserId == user_id).one_or_none()
    
    def GetUser(self, user_id):
        """
        GetUser method returns the user for the specified user id.
        :param user_id: Id of the user.
        :return: User object.
        """
        return self.db_session.query(User).get(user_id)
    
    def GetBookingById(self, booking_id):
        """
        GetBookingById method returns the booking for the specified booking id.
        :param booking_id: Id of the booking.
        :return: Booking object.
        """
        return self.db_session.query(Booking)\
                .filter(Booking.BookingId == booking_id)\
                .options(
                    joinedload(Booking.BookingStatus_),
                    joinedload(Booking.Journey_),
                    joinedload(Booking.BookingAmmendment, innerjoin=False),
                    with_loader_criteria(BookingAmmendment, (BookingAmmendment.DriverApproval & BookingAmmendment.PassengerApproval)))\
                .first()
    
    def CreateUserBalance(self, balance):
        """
        CreateUserBalance method creates a new user balance in the database.
        :param booking: Booking object to be created.
        """
        self.db_session.add(balance)
        self.db_session.commit()

    def UpdatePendingBalance(self, user_id, amount):
        """
        UpdatePendingBalance returns the status of a transaction where a user's pending balance is updated
        :param user_id: Id of the user
        :param amount: Value to be increased of the pending balance
        """
        BalanceSheet = self.GetUserBalance(user_id)
        
        if BalanceSheet is None:
            raise Exception("Balance Sheet not found for user")

        BalanceSheet.Pending += Decimal(amount)

        self.db_session.commit()

    def UpdateNonPendingBalance(self, user_id, amount):
        """
        UpdateNonPendingBalance returns the status of a transaction where a user's non-pending balance is updated
        :param user_id: Id of the user
        :param amount: Value to be increased of the non-pending balance
        """
        BalanceSheet = self.GetUserBalance(user_id)
        
        if BalanceSheet is None:
            raise Exception("Balance Sheet not found for user")
        
        BalanceSheet.NonPending += Decimal(amount)
        self.db_session.commit()

    def CreateTransaction(self, transaction):
        """
        CreateTransaction adds a pre-specified transaction to the database
        """
        self.db_session.add(transaction)
        self.db_session.commit()

    def GetTransaction(self, user_id = None, booking_id = None, amount = None, status = None, typeof = None):
        """
        GetTransaction searches the db for a speicifc transaction log given the appropiate parameters
        """
        return self.db_session.query(Transaction).filter(Transaction.UserId == user_id, Transaction.BookingId == booking_id, Transaction.Value == amount, Transaction.TransactionStatusId == status, Transaction.TransactionTypeId == typeof).first()
        
    def UpdateTransaction(self, transaction_id, amount, typeof, status):
        """
        UpdateTransaction allows for an update to an existing transaction
        """
        transactionToUpdate = self.db_session.query(Transaction).get(transaction_id)
        transactionToUpdate.Amount = amount
        transactionToUpdate.TransactionTypeId = typeof
        transactionToUpdate.TransactionStatusId = status
        transactionToUpdate.UpdateDate = datetime.datetime.now()
        
        self.db_session.commit()

    def GetAdminUsers(self):
        """
        GetAminUsers returns a list of all admins registered on the dashboard
        """
        return self.db_session.query(User).filter(User.UserTypeId == 2).all()