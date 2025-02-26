from .models import Booking, User, Journey
from .db_provider import get_db

class BookingRepository():
    """
    This class is responsible for handling all the database operations related to bookings
    """

    def __init__(self):
        """
        Constructor for BookingRepository class.
        """
        self.db_session = next(get_db())

    def GetBookingsForUser(self, user_id):
        """
        GetBookingsForUser method returns all the bookings for a specific user.
        :param user_id: Id of the user.
        :return: List of bookings for the user.
        """
        return self.db_session.query(Booking).filter(UserId=user_id)
    
    def GetUser(self, user_id):
        """
        GetUser method returns the user for the specified user id.
        :param user_id: Id of the user.
        :return: User object.
        """
        return self.db_session.query(User).get(user_id)
    
    def GetJourney(self, journey_id):
        """
        GetJourney method returns the journey for the specified journey id.
        :param journey_id: Id of the journey.
        :return: Journey object.
        """
        return self.db_session.query(Journey).get(journey_id)
    
    def GetBookingById(self, booking_id):
        """
        GetBookingById method returns the booking for the specified booking id.
        :param booking_id: Id of the booking.
        :return: Booking object.
        """
        return self.db_session.query(Booking).get(booking_id)
    
    def GetExistingBooking(self, user_id, journey_id):
        """
        GetExistingBooking method returns the existing booking for the specified user and journey.
        :param user_id: Id of the user.
        :param journey_id: Id of the journey.
        :return: Booking object.
        """
        return self.db_session.query(Booking).filter(UserId=user_id, JourneyId=journey_id).first()
    
    def CreateBooking(self, booking):
        """
        CreateBooking method creates a new booking in the database.
        :param booking: Booking object to be created.
        """
        self.db_session.add(booking)
        self.db_session.commit()

    def UpdateBooking(self, booking):
        """
        UpdateBooking method updates an existing booking in the database.
        :param booking: Booking object to be updated.
        """
        existing_booking = self.GetBookingById(booking.id)

        if existing_booking is None:
            raise Exception("Booking not found")

        self.db_session.add(booking)
        self.db_session.commit()