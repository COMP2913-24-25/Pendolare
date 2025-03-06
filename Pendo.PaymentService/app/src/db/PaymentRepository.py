from .PendoDatabase import *
from sqlalchemy.orm import joinedload, with_loader_criteria
from .PendoDatabaseProvider import get_db

class PaymentRepository():
    """
    This class is responsible for handling all the database operations related to bookings
    """

    def __init__(self):
        """
        Constructor for BookingRepository class.
        """
        self.db_session = next(get_db())

    def GetUserBalance(self, user_id):
        """
        GetUserBalance method returns the balance of a user for the specified user id.
        :param user_id: Id of the user.
        :return UserBalance object.
        """
        # if user exists, and no balance table, make one
        return self.db_session.query(UserBalance).get(user_id)
    
    def GetUser(self, user_id):
        """
        GetUser method returns the user for the specified user id.
        :param user_id: Id of the user.
        :return: User object.
        """
        return self.db_session.query(User).get(user_id)
    
    # def GetJourney(self, journey_id):
    #     """
    #     GetJourney method returns the journey for the specified journey id.
    #     :param journey_id: Id of the journey.
    #     :return: Journey object.
    #     """
    #     return self.db_session.query(Journey).get(journey_id)
    
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
                                        joinedload(Booking.BookingAmmendment),
                                        with_loader_criteria(BookingAmmendment, BookingAmmendment.DriverApproval and BookingAmmendment.PassengerApproval))\
                                    .all()
    
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
        BalanceSheet = self.db_session.GetUserBalance(user_id)
        
        if BalanceSheet is None:
            raise Exception("Balance Sheet not found for user")
        
        BalanceSheet.Pending += amount
        self.db_session.commit()

    def UpdateNonPendingBalance(self, user_id, amount):
        """
        UpdateNonPendingBalance returns the status of a transaction where a user's non-pending balance is updated
        :param user_id: Id of the user
        :param amount: Value to be increased of the non-pending balance
        """
        BalanceSheet = self.db_session.GetUserBalance(user_id)
        
        if BalanceSheet is None:
            raise Exception("Balance Sheet not found for user")
        
        BalanceSheet.NonPending += amount
        self.db_session.commit()


    # def UpdateBooking(self, booking):
    #     """
    #     UpdateBooking method updates an existing booking in the database.
    #     :param booking: Booking object to be updated.
    #     """
    #     existing_booking = self.GetBookingById(booking.id)

    #     if existing_booking is None:
    #         raise Exception("Booking not found")

    #     self.db_session.add(booking)
    #     self.db_session.commit()