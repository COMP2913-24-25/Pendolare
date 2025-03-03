from .requests import AddBookingAmmendmentRequest
from .booking_repository import BookingRepository
from .models import BookingAmmendment
from fastapi import status

class AddBookingAmmendmentCommand:
    def __init__(self, request: AddBookingAmmendmentRequest, response, logger):
        self.request = request
        self.response = response
        self.logger = logger
        self.booking_repository = BookingRepository()

    def Execute(self):
        try:
            self.logger.debug(f"Adding booking amendment for booking {self.request.BookingId}: {self.request}")
            self._assertBookingExists()

            bookingAmendment = self._createBookingAmendment()
            self.booking_repository.AddBookingAmmendment(bookingAmendment)
            self.logger.debug(f"Added booking amendment for booking {self.request.BookingId} successfully.")

            return {"Status": "Success", "BookingAmmendmentId": f"{bookingAmendment.BookingAmmendmentId}"}
        except Exception as e:
            self.logger.error(f"Error adding booking amendment for booking {self.request.BookingId}: {e}")
            return {"Status": "Error", "Message": str(e)}

    def _assertBookingExists(self):
        booking = self.booking_repository.GetBookingById(self.request.BookingId)
        if booking is None:
            self.response.status_code = status.HTTP_404_NOT_FOUND
            raise Exception(f"Booking {self.request.BookingId} not found")

    def _createBookingAmendment(self):
        return BookingAmmendment(
            BookingId=self.request.BookingId,
            ProposedPrice=self.request.ProposedPrice,
            StartName=self.request.StartName,
            StartLong=self.request.StartLong,
            StartLat=self.request.StartLat,
            EndName=self.request.EndName,
            EndLat=self.request.EndLat,
            CancellationRequest=self.request.CancellationRequest,
            DriverApproval=self.request.DriverApproval,
            PassengerApproval=self.request.PassengerApproval
        )