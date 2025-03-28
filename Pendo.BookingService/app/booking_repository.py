from .models import Booking, User, Journey, BookingAmmendment, Configuration
from sqlalchemy.orm import joinedload, with_loader_criteria
from .db_provider import get_db
from datetime import datetime
from .statuses.booking_statii import BookingStatus

class BookingRepository():
    """
    This class is responsible for handling all the database operations related to bookings
    """

    def __init__(self):
        """
        Constructor for BookingRepository class.
        """
        self.db_session = next(get_db())

    def __del__(self):
        """
        Destructor for BookingRepository class.
        
        Disposes the database session.
        Needed to prevent https://docs.sqlalchemy.org/en/20/errors.html#error-3o7r
        """
        self.db_session.close()

    def GetBookingsForUser(self, user_id, booking_id = None, driver_view = False):
        """
        GetBookingsForUser method returns all the bookings for a specific user.
        :param user_id: Id of the user.
        :return: List of bookings for the user, along with journey (altered by any ammendments) and booking status.
        """
        filters = [Booking.BookingStatusId != BookingStatus.PrePending]
        if booking_id:
            filters.append(Booking.BookingId == booking_id)

        if not driver_view:
            filters.append(Booking.UserId == user_id)
        else:
            filters.append(Journey.UserId == user_id)

        return_dto = []
        bookings = self.db_session.query(Booking)\
            .join(Booking.Journey_)\
            .filter(*filters)\
            .options(
                joinedload(Booking.BookingStatus_),
                joinedload(Booking.User_),
                joinedload(Booking.Journey_).joinedload(Journey.User_),
                joinedload(Booking.BookingAmmendment, innerjoin=False),
                with_loader_criteria(BookingAmmendment, (BookingAmmendment.DriverApproval & BookingAmmendment.PassengerApproval)))\
            .all()
        
        for booking in bookings:
            startTime, startName, startLong, startLat, endName, endLong, endLat, rideTime, price, reccurance = (None,) * 10

            if booking.BookingAmmendment:
                for amendment in sorted(booking.BookingAmmendment, key=lambda x: x.CreateDate):
                    startTime = self.setIfNotNull(amendment.StartTime)
                    startName = self.setIfNotNull(amendment.StartName)
                    startLong = self.setIfNotNull(amendment.StartLong)
                    startLat = self.setIfNotNull(amendment.StartLat)
                    endName = self.setIfNotNull(amendment.EndName)
                    endLong = self.setIfNotNull(amendment.EndLong)
                    endLat = self.setIfNotNull(amendment.EndLat)
                    rideTime = self.setIfNotNull(amendment.StartTime)
                    price = self.setIfNotNull(amendment.ProposedPrice)
                    reccurance = self.setIfNotNull(amendment.Recurrance)

            return_dto.append({
                "Booking": {
                    "BookingId": booking.BookingId,
                    "User": booking.User_,
                    "FeeMargin": booking.FeeMargin,
                    "RideTime": self.setDefaultIfNotNull(rideTime, booking.RideTime),
                    "BookedWindowEnd": booking.BookedWindowEnd,
                },
                "BookingStatus": {
                    "StatusId": booking.BookingStatusId,
                    "Status": booking.BookingStatus_.Status,
                    "Description": booking.BookingStatus_.Description
                },
                "Journey": {
                    "JourneyId": booking.JourneyId,
                    "User": booking.Journey_.User_,
                    "StartTime" : self.setDefaultIfNotNull(startTime, booking.RideTime),
                    "StartName": self.setDefaultIfNotNull(startName, booking.Journey_.StartName),
                    "StartLong": self.setDefaultIfNotNull(startLong, booking.Journey_.StartLong),
                    "StartLat": self.setDefaultIfNotNull(startLat, booking.Journey_.StartLat),
                    "EndName": self.setDefaultIfNotNull(endName, booking.Journey_.EndName),
                    "EndLong": self.setDefaultIfNotNull(endLong, booking.Journey_.EndLong),
                    "EndLat": self.setDefaultIfNotNull(endLat, booking.Journey_.EndLat),
                    "Price": self.setDefaultIfNotNull(price, booking.Journey_.AdvertisedPrice),
                    "JourneyStatusId": booking.Journey_.JourneyStatusId,
                    "JourneyType": booking.Journey_.JourneyType,
                    "Recurrance": self.setDefaultIfNotNull(reccurance, booking.Journey_.Recurrance)
                }
            })

        return return_dto

    
    def setDefaultIfNotNull(self, value, default):
        return value if value is not None else default
    
    def setIfNotNull(self, value):
        return value if value is not None else None
    
    def GetUser(self, user_id):
        """
        GetUser method returns the user for the specified user id.
        :param user_id: Id of the user.
        :return: User object.
        """
        return self.db_session.query(User).get(user_id)
    
    def GetJourney(self, journey_id) -> Journey:
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
        res = self.db_session.query(Booking)\
            .join(BookingAmmendment, Booking.BookingId == BookingAmmendment.BookingId, isouter=True)\
            .filter_by(Booking.BookingId == booking_id)
        
        return None if len(res) == 0 else res[0]
    
    def GetExistingBooking(self, user_id, journey_id):
        """
        GetExistingBooking method returns the existing booking for the specified user and journey.
        :param user_id: Id of the user.
        :param journey_id: Id of the journey.
        :return: Booking object.
        """
        return self.db_session.query(Booking).filter(Booking.UserId == user_id, Booking.JourneyId == journey_id).first()
    
    def CreateBooking(self, booking):
        """
        CreateBooking method creates a new booking in the database.
        :param booking: Booking object to be created.
        """
        self.db_session.add(booking)
        self.db_session.commit()

    def DeleteBooking(self, booking):
        """
        DeleteBooking method deletes a booking from the database.
        :param booking: Booking object to be deleted.
        """
        booking = self.GetBookingById(booking.BookingId)
        self.db_session.delete(booking)
        self.db_session.commit()

    def MarkJourneyBooked(self, booking):
        """
        MarkJourneyBooked method marks the journey as booked in the database.
        """
        journey = self.GetJourney(booking.JourneyId)
        journey.JourneyStatusId = 2
        self.db_session.commit()

    def ApproveBooking(self, booking_id):
        """
        ApproveBooking method sets 'DriverApproval' to true on a booking request.
        :param booking_id: Id of the booking.
        """
        booking = self.GetBookingById(booking_id)

        if booking is None:
            raise Exception(f"Booking {booking_id} not found")
        
        if booking.DriverApproval:
            raise Exception(f"Booking {booking_id} already approved")
        
        booking.DriverApproval = True
        booking.UpdatedDate = datetime.now()
        self.db_session.commit()

        return booking


    def UpdateBookingStatus(self, bookingId, bookingStatusId):
        """
        UpdateBooking method updates an existing booking in the database.
        :param booking: Booking object to be updated.
        """
        booking = self.GetBookingById(bookingId)

        if booking is None:
            raise Exception("Booking not found")
        
        booking.BookingStatusId = bookingStatusId
        booking.UpdateDate = datetime.now()
        self.db_session.commit()

    def AddBookingAmmendment(self, booking_ammendment):
        """
        AddBookingAmmendment method adds a new booking ammendment in the database.
        :param booking_ammendment: BookingAmmendment object to be added.
        """
        self.db_session.add(booking_ammendment)
        self.db_session.commit()

    def GetBookingAmmendment(self, booking_ammendment_id):
        """
        GetBookingAmmendment method returns the booking ammendment for the specified booking ammendment id.
        :param booking_ammendment_id: Id of the booking ammendment.
        :return BookingAmmendment object, Driver object, Passenger object, Journey object.
        """
        ammendment = self.db_session.query(BookingAmmendment).get(booking_ammendment_id)
        booking = self.GetBookingById(ammendment.BookingId)

        passenger = self.GetUser(booking.UserId)
        journey = self.GetJourney(booking.JourneyId)
        driver = self.GetUser(journey.UserId)

        return ammendment, driver, passenger, journey
    
    def GetBookingAmmendments(self, booking_id):
        """
        GetBookingAmmendments method returns all the booking ammendments for a booking.
        :param booking_id: Id of the booking.
        :return: List of BookingAmmendment objects.
        """
        return self.db_session.query(BookingAmmendment).filter(BookingAmmendment.BookingId == booking_id).all()
    
    def UpdateBookingAmmendment(self, booking_ammendment):
        """
        UpdateBookingAmmendment method updates an existing booking ammendment in the database.
        :param booking_ammendment: BookingAmmendment object to be updated.
        """
        booking_ammendment.UpdateDate = datetime.now()
        self.db_session.commit()

    def UpdateBooking(self, booking):
        """
        UpdateBooking method updates an existing booking in the database.
        :param booking: Booking object to be updated.
        """
        booking.UpdateDate = datetime.now()
        self.db_session.commit()

    def CalculateDriverRating(self, driver_id):
        """
        CalculateDriverRating method calculates the driver rating based on the bookings.
        :param driver_id: Id of the driver.
        :return: Driver rating.
        """
        driver = self.GetUser(driver_id)
        if driver is None:
            raise Exception(f"Driver {driver_id} not found")

        now = datetime.now()

        pending_count = self.db_session.query(Booking)\
            .join(Journey, Booking.JourneyId == Journey.JourneyId)\
            .filter(Journey.UserId == driver_id, 
                    Booking.BookingStatusId == BookingStatus.PendingCompletion or Booking.BookingStatusId == BookingStatus.Completed, 
                    Booking.RideTime < now)\
            .count()

        completed_count = self.db_session.query(Booking)\
            .join(Journey, Booking.JourneyId == Journey.JourneyId)\
            .filter(Journey.UserId == driver_id, Booking.BookingStatusId == BookingStatus.Completed)\
            .count()

        total_bookings = pending_count + completed_count
        rating = completed_count / float(total_bookings) if total_bookings > 0 else -1.0

        driver.UserRating = rating
        self.db_session.commit()