from .booking_repository import BookingRepository, Booking
from .email_sender import generateEmailDataFromBooking
from datetime import datetime
from .cron_checker import checkTimeValid, getNextTimes
from sqlalchemy import DECIMAL, cast
from fastapi import status
from .statuses.booking_statii import BookingStatus
from .responses import StatusResponse
from .requests import CreateBookingRequest
from .db_provider import get_db
from .payment_service_api import PaymentServiceClient

class CreateBookingCommand:
    """
    CreateBookingCommand class is responsible for creating a new booking.
    """

    def __init__(self, 
                 request : CreateBookingRequest, 
                 response : StatusResponse, 
                 email_sender, 
                 logger, 
                 dvla_client, 
                 configuration_provider,
                 payment_service_client : PaymentServiceClient):
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
            
            if journey.JourneyType == 2 and journey.Recurrance is None:
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                raise Exception("Commuter journey must have a recurrance.")
            
            existing_booking = self.booking_repository.GetExistingBooking(user.UserId, journey.JourneyId)
            if existing_booking is not None:
                if journey.JourneyType == 2:
                    self._handleNewBookingWindow(existing_booking)
                else:
                    self.response.status_code = status.HTTP_400_BAD_REQUEST
                    raise Exception("Booking for this journey already exists")
            
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

            if journey.JourneyType == 2:
                if self.request.EndCommuterWindow is None:
                    self.response.status_code = status.HTTP_400_BAD_REQUEST
                    raise Exception("EndCommuterWindow must be provided for commuter journeys.")
                
                booking.BookedWindowEnd = self.request.EndCommuterWindow

            self.booking_repository.CreateBooking(booking)
            self.logger.debug(f"Booking DB object created successfully. BookingId: {booking.BookingId}")

            numJourneysInWindow = 1
            if journey.JourneyType == 2:
                numJourneysInWindow = len(getNextTimes(journey.Recurrance, booking.RideTime, booking.BookedWindowEnd, 9999))
                
            amount = journey.AdvertisedPrice * numJourneysInWindow
            
            # Apply discount if present for commuter journeys
            if journey.JourneyType == 2 and journey.DiscountID is not None:
                discount = self.booking_repository.db_session.query(Discounts).filter_by(DiscountID=journey.DiscountID).first()
                if discount is not None:
                    self.logger.info(f"Applying discount: {discount.DiscountPercentage * 100}% off for {discount.WeeklyJourneys} weekly journeys")
                    amount = amount * (1 - discount.DiscountPercentage)
                    
            print(journey.AdvertisedPrice, numJourneysInWindow, amount)
            print(booking.BookingId, booking.RideTime, booking.BookedWindowEnd)

            # Notify payment service of new booking
            if not self.payment_service_client.PendingBookingRequest(booking.BookingId, amount):
                 self.response.status_code = status.HTTP_403_FORBIDDEN
                 self.booking_repository.DeleteBooking(booking)
                 raise Exception("Payment service failed to process booking. User balance insufficient.")
            
            self.booking_repository.UpdateBookingStatus(booking.BookingId, BookingStatus.Pending)
            self.logger.debug("Booking status updated to pending successfully.")
            
            self.booking_repository.MarkJourneyBooked(booking)

            driver = self.booking_repository.GetUser(journey.UserId)

            email_data = generateEmailDataFromBooking(booking, driver, journey, self.dvla_client.GetVehicleDetails(journey.RegPlate))

            self.email_sender.SendBookingPending(user.Email, email_data)
            self.logger.debug("Booking pending email sent successfully.")

            return StatusResponse(Message="Booking created successfully.")
        
        except Exception as e:
            self.logger.error(f"Error creating booking. Error: {str(e)}")
            if self.response.status_code is None:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                
            return StatusResponse(Status="Failed", Message=str(e))
        
    def _handleNewBookingWindow(self, existing_booking):
        """
        Method to handle the creation of a new booking window for a commuter journey.
        :param existing_booking: Existing booking object.
        """
        if existing_booking.BookedWindowEnd is not None and existing_booking.BookedWindowEnd >= self.request.JourneyTime:
            self.logger.debug("Booking window has not passed. No action required")
            return

        self.logger.debug("Booking window has passed. Creating new booking window.")

        existing_booking.RideTime = self.request.JourneyTime
        existing_booking.BookedWindowEnd = self.request.EndCommuterWindow

        self.booking_repository.UpdateBooking(existing_booking)

        self.logger.debug("New booking window created successfully.")
