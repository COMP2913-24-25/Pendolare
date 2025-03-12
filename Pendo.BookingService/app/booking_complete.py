from .booking_repository import BookingRepository
from fastapi import status
from .responses import StatusResponse
from .statuses.booking_statii import BookingStatus

class BookingCompleteCommand:
    """
    BookingCompleteCommand class is a command object for completing a booking.
    """

    def __init__(self, bookingId, request, response, logger, payment_service_client):
        self.bookingId = bookingId
        self.request = request
        self.response = response
        self.logger = logger
        self.booking_repository = BookingRepository()
        self.payment_service_client = payment_service_client

    def Execute(self) -> StatusResponse:
        """
        Sets a booking to complete once confirmed by both driver and passenger.
        """
        try:
            user = self.booking_repository.GetUser(self.request.UserId)

            if user is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                msg = f"User {self.request.UserId} not found"
                self.logger.error(msg)
                return StatusResponse(Status="Failed", Message=msg)
            
            booking = self.booking_repository.GetBookingById(self.bookingId)

            if booking is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                msg = f"Booking {self.bookingId} not found"
                self.logger.error(msg)
                return StatusResponse(Status="Failed", Message=msg)
            
            journey = self.booking_repository.GetJourney(booking.JourneyId)

            if user.UserId == journey.UserId:
                if booking.BookingStatusId == BookingStatus.Confirmed:
                    self.logger.debug("Driver has confirmed booking. Setting booking to pending completion.")
                    self.booking_repository.UpdateBookingStatus(self.bookingId, BookingStatus.PendingCompletion)
                    return StatusResponse(Message="Booking set pending completion. Waiting for passenger to confirm.")
                
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                msg = "Booking is not confirmed. Cannot complete booking."
                self.logger.error(msg)
                return StatusResponse(Status="Failed", Message=msg)
            
            if user.UserId == booking.UserId:
                if booking.BookingStatusId not in (BookingStatus.PendingCompletion, BookingStatus.Confirmed):
                    self.response.status_code = status.HTTP_400_BAD_REQUEST
                    msg = "Booking is not pending completion / confirmed. Cannot complete booking."
                    self.logger.error(msg)
                    return StatusResponse(Status="Failed", Message=msg)
                
                if self.request.Completed:
                    self.logger.debug("Passenger has confirmed booking happened. Completing booking.")
                    self.booking_repository.UpdateBookingStatus(self.bookingId, BookingStatus.Completed)

                    self.logger.info(f"Sending completed booking request to payment service for booking {self.bookingId}")
                    if not self.payment_service_client.CompletedBookingRequest(self.bookingId):
                        msg = "Payment service returned an error, rolloing booking back to not completed."
                        self.logger.error(msg)

                        self.logger.debug("Rolling back booking to 'Not Completed'.")
                        self.booking_repository.UpdateBookingStatus(self.bookingId, BookingStatus.NotCompleted)
                        return StatusResponse(Status="Failed", Message=msg)

                    return StatusResponse(Message="Booking completed successfully.")
                
                self.logger.debug("Passenger has said booking did not happen. Setting booking to 'Not Completed'.")
                self.booking_repository.UpdateBookingStatus(self.bookingId, BookingStatus.NotCompleted)
                return StatusResponse(Message="Booking set to not completed.")
            
            self.response.status_code = status.HTTP_401_UNAUTHORIZED
            msg = f"User {self.request.UserId} not authorised to complete booking {self.bookingId}"
            self.logger.error(msg)
            return StatusResponse(Status="Failed", Message=msg)
        
        except Exception as e:
            self.logger.error(f"Error completing booking {self.bookingId}: {e}")
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            return StatusResponse(Status="Failed", Message="Error completing booking.")