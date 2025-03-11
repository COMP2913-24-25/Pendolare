from .requests import ApproveBookingAmmendmentRequest
from .booking_repository import BookingRepository
from .email_sender import generateEmailDataFromAmmendment
from datetime import datetime
from fastapi import status
from .statuses.booking_statii import BookingStatus

class ApproveBookingAmmendmentCommand:

    def __init__(self, 
                 ammendment_id, 
                 request : ApproveBookingAmmendmentRequest, 
                 response, 
                 logger, 
                 email_sender, 
                 dvla_client,
                 payment_service_client):
        self.ammendment_id = ammendment_id
        self.request = request
        self.response = response
        self.logger = logger
        self.booking_repository = BookingRepository()
        self.dvla_client = dvla_client
        self.email_sender = email_sender
        self.payment_service_client = payment_service_client

    def Execute(self):
        """
        Execute method approves a booking ammendment.
        """
        try:
            self.logger.debug(f"Approving booking ammendment {self.ammendment_id}: {self.request}")

            booking_ammendment, driver, passenger, journey = self.booking_repository.GetBookingAmmendment(self.ammendment_id)

            if booking_ammendment is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                raise Exception(f"Booking ammendment {self.ammendment_id} not found")
            
            booking = self.booking_repository.GetBookingById(booking_ammendment.BookingId)
            if booking is None:
                self.response.status_code = status.HTTP_404_NOT_FOUND
                raise Exception(f"Booking {booking_ammendment.BookingId} not found")
            
            if booking.BookingStatusId != 1:
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                raise Exception(f"Booking {booking_ammendment.BookingId} is not pending approval therefore cannot be ammended.")
            
            if booking_ammendment.CancellationRequest:
                if self.request.UserId != driver.UserId and self.request.UserId != passenger.UserId:
                    self.response.status_code = status.HTTP_401_UNAUTHORIZED
                    raise Exception(f"User {self.request.UserId} not authorised to cancel booking ammendment {self.ammendment_id}")
                
                self._applyAmmendment(booking_ammendment, passenger, driver, journey)
                return self._success("Booking ammendment fully approved and booking cancelled.")
            
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
            if self.response.status_code is None:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Status": "Error", "Message": str(e)}
    
    def _applyAmmendment(self, ammendment, passenger, driver, journey):
        email_data = generateEmailDataFromAmmendment(ammendment, driver, journey, self.dvla_client.GetVehicleDetails(journey.RegPlate))

        if ammendment.CancellationRequest:
            res = self.email_sender.SendBookingCancelled(passenger.Email, email_data)
            self.logger.debug(f"Email send result: {res}")
            self.booking_repository.UpdateBookingStatus(ammendment.BookingId, BookingStatus.Cancelled)
            self.logger.info(f"Booking {ammendment.BookingId} cancelled successfully.")

            # TODO: Check this with alex - surely we need to supply the bookingId???
            if not self.payment_service_client.RefundRequest(passenger.UserId):
                msg = "Error refunding user"
                self.logger.error(msg)
                raise Exception(msg)
            
            self.logger.info(f"User {passenger.UserId} refunded successfully.")
            return

        self.booking_repository.UpdateBookingStatus(ammendment.BookingId, BookingStatus.Confirmed)

        res = self.email_sender.SendBookingConfirmation(passenger.Email, email_data)
        self.logger.debug(f"Email send result: {res}")
        self.logger.info(f"Booking {ammendment.BookingId} confirmed successfully.")

    def _setApprovals(self, ammendment, driver, passenger):
        if self.request.UserId == driver.UserId and self.request.DriverApproval:
            ammendment.DriverApproval = True
            self.booking_repository.UpdateBookingAmmendment(ammendment)
            self.logger.info(f"Approved booking ammendment {self.ammendment_id} for driver successfully.")

        elif self.request.UserId == passenger.UserId and self.request.PassengerApproval:
            ammendment.PassengerApproval = True
            self.booking_repository.UpdateBookingAmmendment(ammendment)
            self.logger.info(f"Approved booking ammendment {self.ammendment_id} for passenger successfully.")
        else:
            self.response.status_code = status.HTTP_401_UNAUTHORIZED
            raise Exception(f"User {self.request.UserId} not authorised to approve booking ammendment {self.ammendment_id}")

    def _success(self, message):
        return {"Status": "Success", "Message": f"{message}"}