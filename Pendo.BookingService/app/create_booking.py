from .booking_repository import BookingRepository, Booking
from .email_sender import generateEmailDataFromBooking
from datetime import datetime
from .cron_checker import checkTimeValid

class CreateBookingCommand:
    """
    CreateBookingCommand class is responsible for creating a new booking.
    """

    def __init__(self, request, email_sender, logger, dvla_client):
        """
        Constructor for CreateBookingCommand class.
        :param request: Request object containing the booking details.
        """
        self.booking_repository = BookingRepository()
        self.email_sender = email_sender
        self.request = request
        self.logger = logger
        self.dvla_client = dvla_client

    def Execute(self):
        """
        Execute method creates a new booking.
        :return: Response object containing the status of the operation.
        """
        try:
            user = self.booking_repository.GetUser(self.request.UserId)
            if user is None:
                raise Exception("User not found")
            
            journey = self.booking_repository.GetJourney(self.request.JourneyId)
            if journey is None:
                raise Exception("Journey not found")
            
            if not checkTimeValid(journey.CronExpression, self.request.BookingTime):
                raise Exception("Booking time is not valid for the journey")
            
            existing_booking = self.booking_repository.GetExistingBooking(user.UserId, journey.JourneyId, self.request.BookingTime)
            if existing_booking is not None:
                raise Exception("Booking for this time and journey combination already exists")
            
            booking = Booking(
                UserId=user.UserId,
                JourneyId=journey.JourneyId,
                BookingStatusId=1, #Pending - this should not change!
            )

            self.booking_repository.CreateBooking(booking)
            self.logger.debug(f"Booking DB object created successfully. BookingId: {booking.BookingId}")

            email_data = generateEmailDataFromBooking(booking, user, journey, self.dvla_client.GetVehicleDetails(journey.VehicleRegistration))

            self.email_sender.SendBookingPending(user.Email, email_data)
            self.logger.debug("Booking pending email sent successfully.")
            return {"Status": "Success", "createTime": datetime.now()}
        except Exception as e:
            self.logger.error(f"Error creating booking. Error: {str(e)}")
            return {"Status": "Failed", "Error": str(e)}