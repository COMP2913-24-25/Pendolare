from .requests import ApproveBookingRequest
from .booking_repository import BookingRepository
from .email_sender import generateEmailDataFromBooking
from fastapi import status

class ApproveBookingCommand:

    def __init__(self, booking_id, request, response, logger, email_sender, dvla_client):
        self.booking_id = booking_id
        self.request = request
        self.response = response
        self.logger = logger
        self.booking_repository = BookingRepository()
        self.dvla_client = dvla_client
        self.email_sender = email_sender

    def Execute(self):
        """
        Execute method approves a booking request, provided no ammenments are present.
        """
        try:
            booking = self.booking_repository.GetBookingById(self.booking_id)
            if booking is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                raise Exception(f"Booking {self.booking_id} not found.")

            ammendments = self.booking_repository.GetBookingAmmendments(self.booking_id)
            if len(ammendments) > 0:
                self.logger.debug(f"Booking {self.booking_id} has ammendments pending approval.")
                self.response.status_code = status.HTTP_401_UNAUTHORIZED
                raise Exception(f"Booking {self.booking_id} has ammendments pending approval.")
            
            passenger = self.booking_repository.GetUser(booking.UserId)

            journey = self.booking_repository.GetJourney(booking.JourneyId)
            driver = self.booking_repository.GetUser(journey.UserId)

            if driver.UserId != self.request.UserId:
                self.response.status_code = status.HTTP_401_UNAUTHORIZED
                raise Exception(f"User {self.request.UserId} is not authorised to approve booking {self.booking_id}")

            self.logger.debug(f"Booking {self.booking_id} approved successfully.")
            self.booking_repository.UpdateBookingStatus(self.booking_id, 2)
            self.logger.debug(f"Booking {self.booking_id} status updated to confirmed.")

            email_data = generateEmailDataFromBooking(booking, driver, journey, self.dvla_client.GetVehicleDetails(journey.RegPlate))

            self.email_sender.SendBookingConfirmation(passenger.Email, email_data)
            self.logger.debug(f"Booking confirmation email sent to {passenger.Email}.")
            return {"Status": "Success", "Message": "Booking approved successfully."}
        
        except Exception as e:
            self.logger.error(f"Error when attempting to approve booking {self.booking_id}: {e}")
            if self.response.status_code is None:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Status": "Error", "Message": str(e)}
