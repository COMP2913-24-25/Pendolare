from .booking_repository import BookingRepository, Booking
from .email_sender import generateEmailDataFromBooking
from datetime import datetime
from .cron_checker import checkTimeValid
from sqlalchemy import DECIMAL, cast
from fastapi import status
from .statuses.booking_statii import BookingStatus
from .responses import StatusResponse
from .db_provider import get_db

class CreateBookingCommand:
    """
    CreateBookingCommand class is responsible for creating a new booking.
    """

    def __init__(self, 
                 request, 
                 response, 
                 email_sender, 
                 logger, 
                 dvla_client, 
                 configuration_provider,
                 payment_service_client):
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
        self.payment_service_client = payment_service_client

    def Execute(self):
        """
        Execute method creates a new booking.
        :return: Response object containing the status of the operation.
        """
        try:
            user = self.booking_repository.GetUser(self.request.UserId)
            if user is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                raise Exception("User not found")
            
            journey = self.booking_repository.GetJourney(self.request.JourneyId)
            if journey is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                raise Exception("Journey not found")
            
            #Check booking not in the past
            if self.request.JourneyTime < datetime.now():
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                raise Exception("Booking time cannot be in the past")
            
            if journey.JourneyType == 2 and not checkTimeValid(journey.Recurrance, self.request.JourneyTime):
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                raise Exception("Booking time is not valid for the commuter journey")
            
            existing_booking = self.booking_repository.GetExistingBooking(user.UserId, journey.JourneyId, self.request.JourneyTime)
            if existing_booking is not None:
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                raise Exception("Booking for this time and journey combination already exists")
            
            current_booking_fee = self.configuration_provider.GetSingleValue(next(get_db()), "Booking.FeeMargin")
            if current_booking_fee is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                raise Exception("Booking fee margin not found.")
            
            booking = Booking(
                UserId=user.UserId,
                JourneyId=journey.JourneyId,
                BookingStatusId=BookingStatus.PrePending,
                FeeMargin=cast(current_booking_fee, DECIMAL(18, 2)),
                RideTime=self.request.JourneyTime
            )

            self.booking_repository.CreateBooking(booking)
            self.logger.debug(f"Booking DB object created successfully. BookingId: {booking.BookingId}")

            # Notify payment service of new booking
            if not self.payment_service_client.PendingBookingRequest(booking.BookingId):
                self.response.status_code = status.HTTP_403_FORBIDDEN
                self.booking_repository.DeleteBooking(booking.BookingId)
                raise Exception("Payment service failed to process booking. User balance insufficient.")
            
            self.booking_repository.UpdateBookingStatus(booking.BookingId, BookingStatus.Pending)
            self.logger.debug("Booking status updated to pending successfully.")

            self.booking_repository.MarkJourneyBooked(booking)

            email_data = generateEmailDataFromBooking(booking, user, journey, self.dvla_client.GetVehicleDetails(journey.VehicleRegistration))

            self.email_sender.SendBookingPending(user.Email, email_data)
            self.logger.debug("Booking pending email sent successfully.")

            return StatusResponse(Message="Booking created successfully.")
        
        except Exception as e:
            self.logger.error(f"Error creating booking. Error: {str(e)}")
            if self.response.status_code is None:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                
            return StatusResponse(Status="Failed", Message=str(e))