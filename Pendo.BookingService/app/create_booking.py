from .booking_repository import BookingRepository, Booking
from .email_sender import generateEmailDataFromBooking
from datetime import datetime
from .cron_checker import checkTimeValid
from sqlalchemy import DECIMAL, cast
from fastapi import status

class CreateBookingCommand:
    """
    CreateBookingCommand class is responsible for creating a new booking.
    """

    def __init__(self, request, response, email_sender, logger, dvla_client, configuration_provider):
        """
        Constructor for CreateBookingCommand class.
        :param request: Request object containing the booking details.
        """
        self.booking_repository = BookingRepository()
        self.email_sender = email_sender
        self.request = request
        self.logger = logger
        self.dvla_client = dvla_client
        self.configuration_provider = configuration_provider
        self.response = response

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
            
            if journey.JourneyTypeId == 2 and not checkTimeValid(journey.Recurrance, self.request.BookingTime):
                raise Exception("Booking time is not valid for the commuter journey")
            
            existing_booking = self.booking_repository.GetExistingBooking(user.UserId, journey.JourneyId, self.request.BookingTime)
            if existing_booking is not None:
                raise Exception("Booking for this time and journey combination already exists")
            
            current_booking_fee = self.configuration_provider.GetSingleValue("Booking.FeeMargin")
            if current_booking_fee is None:
                raise Exception("Booking fee margin not found.")
            
            booking = Booking(
                UserId=user.UserId,
                JourneyId=journey.JourneyId,
                BookingStatusId=1, #Pending - this should not change!
                FeeMargin=cast(current_booking_fee, DECIMAL(18, 2)),
            )

            self.booking_repository.CreateBooking(booking)
            self.logger.debug(f"Booking DB object created successfully. BookingId: {booking.BookingId}")

            email_data = generateEmailDataFromBooking(booking, user, journey, self.dvla_client.GetVehicleDetails(journey.VehicleRegistration))

            self.email_sender.SendBookingPending(user.Email, email_data)
            self.logger.debug("Booking pending email sent successfully.")
            return {"Status": "Success", "createTime": datetime.now()}
        except Exception as e:
            self.logger.error(f"Error creating booking. Error: {str(e)}")
            self.response.status_code = status.HTTP_400_BAD_REQUEST
            return {"Status": "Failed", "Error": str(e)}