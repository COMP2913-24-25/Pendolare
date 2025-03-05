from models import Booking

class BookingRepository:
    """
    A class used to house all the methods that interact with the Booking table in the database.
    """

    def __init__(self, db_session):
        """
        Constructor for BookingRepository class.
        """
        self.db_session = db_session

    def GetBookingById(self, booking_id):
        return self.db_session.query(Booking).get(booking_id)
    
    def GetBookingsInWindow(self, start_date, end_date):
        return self.db_session.query(Booking)\
            .filter(Booking.RideTime >= start_date, Booking.RideTime <= end_date, Booking.BookingStatusId == 4).all()
    
    #etc etc, add more methods here