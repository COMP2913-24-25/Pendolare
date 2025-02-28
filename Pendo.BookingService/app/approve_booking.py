from .requests import ApproveBookingRequest
from .booking_repository import BookingRepository
from .email_sender import generateEmailDataFromBooking

class ApproveBookingCommand:

    def __init__(self, booking_id, request, logger, email_sender, dvla_client):
        self.booking_id = booking_id
        self.logger = logger
        self.booking_repository = BookingRepository()
        self.dvla_client = dvla_client
        self.email_sender = email_sender

    def Execute(self):
        """
        Execute method approves a booking request, provided no ammenments are present.
        """
        try:
            ammendments = self.booking_repository.GetBookingAmmendments(self.booking_id)
            if len(ammendments) > 0:
                self.logger.debug(f"Booking {self.booking_id} has ammendments pending approval.")
                raise Exception(f"Booking {self.booking_id} has ammendments pending approval.")

            self.logger.debug(f"Booking {self.booking_id} approved successfully.")

            self.booking_repository.UpdateBookingStatus(self.booking_id, 2)
            self.logger.debug(f"Booking {self.booking_id} status updated to confirmed.")

            booking = self.booking_repository.GetBooking(self.booking_id)
            passenger = self.booking_repository.GetUser(booking.UserId)

            journey = self.booking_repository.GetJourney(booking.JourneyId)
            driver = self.booking_repository.GetUser(journey.UserId)

            email_data = generateEmailDataFromBooking(booking, driver, journey, self.dvla_client.GetVehicleDetails(journey.VehicleRegistration))
            self.email_sender.SendBookingConfirmation(passenger.Email, email_data)
            self.logger.debug(f"Booking confirmation email sent to {passenger.Email}.")
            return {"Status": "Success", "Message": "Booking approved successfully."}
        
        except Exception as e:
            self.logger.error(f"Error when attempting to approve booking {self.booking_id}: {e}")
            return {"Status": "Error", "Message": str(e)}
