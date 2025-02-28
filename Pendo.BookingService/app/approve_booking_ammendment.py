from .requests import ApproveBookingAmmendmentRequest
from .booking_repository import BookingRepository
from .email_sender import generateEmailDataFromAmmendment
from datetime import datetime

class ApproveBookingAmmendmentCommand:

    def __init__(self, ammendment_id, request : ApproveBookingAmmendmentRequest, logger, email_sender, dvla_client):
        self.ammendment_id = ammendment_id
        self.request = request
        self.logger = logger
        self.booking_repository = BookingRepository()
        self.dvla_client = dvla_client
        self.email_sender = email_sender

    def Execute(self):
        """
        Execute method approves a booking ammendment.
        """
        try:
            self.logger.debug(f"Approving booking ammendment {self.ammendment_id}: {self.request}")

            booking_ammendment, driver, passenger, journey = self.booking_repository.GetBookingAmmendment(self.ammendment_id)

            if booking_ammendment is None:
                raise Exception(f"Booking ammendment {self.ammendment_id} not found")
            
            self._setApprovals(booking_ammendment, driver, passenger)

            if booking_ammendment.DriverApproval and booking_ammendment.PassengerApproval:
                self.logger.debug(f"Booking ammendment {self.ammendment_id} fully approved. Updating booking...")

                self._applyAmmendment(booking_ammendment, passenger, driver, journey)
                if booking_ammendment.CancellationRequest:
                    return self._success("Booking ammendment fully approved and booking cancelled.")
                return self._success("Booking ammendment fully approved and applied to booking. Booking set to confirmed.")

            if booking_ammendment.DriverApproval:
                self.logger.debug(f"Booking ammendment {self.ammendment_id} driver approved. Waiting for passenger approval...")
                return self._success("Driver approved booking ammendment")
            
            if booking_ammendment.PassengerApproval:
                self.logger.debug(f"Booking ammendment {self.ammendment_id} passenger approved. Waiting for driver approval...")
                return self._success("Passenger approved booking ammendment")

        except Exception as e:
            self.logger.error(f"Error approving booking ammendment {self.ammendment_id}: {e}")
            return {"Status": "Error", "Message": str(e)}
    
    def _applyAmmendment(self, ammendment, passenger, driver, journey):
        email_data = generateEmailDataFromAmmendment(ammendment, driver, journey, self.dvla_client.GetVehicleDetails(journey.VehicleRegistration))

        if ammendment.CancellationRequest:
            self.booking_repository.UpdateBookingStatus(ammendment.BookingId, 3)
            self.logger.debug(f"Booking {ammendment.BookingId} cancelled successfully.")
            return
    
        ## call payment service and charge passenger

        self.booking_repository.UpdateBookingStatus(ammendment.BookingId, 2)

        self.email_sender.SendBookingConfirmation(passenger.Email, email_data) #Should we send an email to the driver too?
        self.logger.debug(f"Booking {ammendment.BookingId} confirmed successfully.")

    def _setApprovals(self, ammendment, driver, passenger):
        if self.request.UserId == driver.UserId and self.request.DriverApproval:
            ammendment.DriverApproval = True
            self.booking_repository.UpdateBookingAmmendment(ammendment)
            self.logger.debug(f"Approved booking ammendment {self.ammendment_id} for driver successfully.")

        elif self.request.UserId == passenger.UserId and self.request.PassengerApproval:
            ammendment.PassengerApproval = True
            self.booking_repository.UpdateBookingAmmendment(ammendment)
            self.logger.debug(f"Approved booking ammendment {self.ammendment_id} for passenger successfully.")
        else:
            raise Exception(f"User {self.request.UserId} not authorised to approve booking ammendment {self.ammendment_id}")

    def _success(self, message):
        return {"Status": "Success", "Message": f"{message}"}