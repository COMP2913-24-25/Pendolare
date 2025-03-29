from .booking_repository import BookingRepository
from .email_sender import generateEmailDataFromBooking
from fastapi import status
from .responses import StatusResponse
from .cron_checker import getNextTimes
from .models import Booking
from .statuses.booking_statii import BookingStatus
from .requests import ConfirmAtPickupRequest

class ConfirmAtPickupCommand:

    def __init__(self, booking_id: str, request : ConfirmAtPickupRequest, response, configuration_provider, email_sender, logger, dvla_client):
        self.booking_id = booking_id
        self.booking_repository = BookingRepository()
        self.request = request
        self.response = response
        self.configuration_provider = configuration_provider
        self.email_sender = email_sender
        self.logger = logger
        self.dvla_client = dvla_client

    def Execute(self):
        """
        Confirms the booking at pickup by sending an email to the passenger.
        Additionally, updates the booking status to 'Pending Completion'.
        """
        try:
            booking : Booking = self.booking_repository.GetBookingById(self.booking_id)

            if booking is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                self.logger.warn(f"Booking not found for booking id: {self.booking_id}")
                return StatusResponse(Status="Failed", Message="Booking not found")
            
            if booking.BookingStatusId != 2:
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                self.logger.warn(f"Booking is not in confirmed status for booking id: {self.booking_id}")

                return StatusResponse(Status="Failed", Message="Booking is not in confirmed status")
            
            journey = self.booking_repository.GetJourney(booking.JourneyId)
            if journey is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                self.logger.warn(f"Journey not found for booking id: {self.booking_id}")
                
                return StatusResponse(Status="Failed", Message="Journey not found")
            
            if self.request.UserId != journey.UserId:
                self.response.status_code = status.HTTP_401_UNAUTHORIZED
                self.logger.warn(f"User not authorized to confirm booking for booking id: {self.booking_id}")

                return StatusResponse(Status="Failed", Message="User not authorised to confirm booking")
            
            passenger = self.booking_repository.GetUser(booking.UserId)
            driver = self.booking_repository.GetUser(journey.UserId)
            vehicle = self.dvla_client.GetVehicleDetails(journey.RegPlate)

            self.logger.debug(f"Confirming booking for booking id: {self.booking_id}")

            times = None
            if journey.JourneyType == 2:
                times = getNextTimes(journey.Recurrance, self.request.JourneyTime, booking.BookedWindowEnd, 999)

            startTimeOverride = times[0] if times is not None and len(times) > 0 else self.request.JourneyTime

            res = self.email_sender.SendBookingArrivalEmail(passenger.Email, generateEmailDataFromBooking(booking, driver, journey, vehicle, startTimeOverride))
            self.logger.debug(f"Booking arrival email sent to {passenger.Email} for booking id: {self.booking_id} with response: {res}")

            if journey.JourneyType == 2:

                if len(times) == 0:
                    self.logger.error(f"No times found for recurring journey with booking id: {self.booking_id}")
                    return StatusResponse(Status="Failed", Message="No times found for recurring journey")

                if len(times) == 1:
                    self.logger.debug("Updating booking status to 'PendingComplettion' as only on last time before booking window end.")
                    self.booking_repository.UpdateBookingStatus(self.booking_id, BookingStatus.PendingCompletion)
                    return StatusResponse(Message="Booking confirmed successfully.")

                self.logger.info("Commuter journey staying in confirmed status as not at end of window.")
                return StatusResponse(Message="Booking confirmed successfully.")

            self.logger.debug("Updating booking status to 'Pending Completion'")
            self.booking_repository.UpdateBookingStatus(self.booking_id, 4)
            self.logger.debug(f"Booking status updated to 'Pending Completion' for booking id: {self.booking_id}")

            return StatusResponse(Message="Booking confirmed successfully.")

        except Exception as e:
            if self.response.status_code is None:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return StatusResponse(Status="Failed", Message=str(e))