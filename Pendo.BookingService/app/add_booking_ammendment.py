from .requests import AddBookingAmmendmentRequest
from .booking_repository import BookingRepository
from .models import BookingAmmendment
from fastapi import status
from datetime import datetime
from .statuses.booking_statii import BookingStatus

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

            # Only validate start time if this is not a cancellation request
            if not self.request.CancellationRequest and self.request.StartTime is not None:
                if self.request.StartTime < datetime.now():
                    self.response.status_code = status.HTTP_400_BAD_REQUEST
                    raise Exception("Start time cannot be in the past")

            bookingAmendment = self._createBookingAmendment()
            self.booking_repository.AddBookingAmmendment(bookingAmendment)
            self.logger.debug(f"Added booking amendment for booking {self.request.BookingId} successfully.")

            return {"Status": "Success", "BookingAmmendmentId": f"{bookingAmendment.BookingAmmendmentId}"}
        except Exception as e:
            self.logger.error(f"Error adding booking amendment for booking {self.request.BookingId}: {e}")
            if self.response.status_code is None:
                self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Status": "Error", "Message": str(e)}

    def _assertBookingExists(self):
        booking = self.booking_repository.GetBookingById(self.request.BookingId)
        if booking is None:
            self.response.status_code = status.HTTP_404_NOT_FOUND
            raise Exception(f"Booking {self.request.BookingId} not found")
        
        if not ((self.request.CancellationRequest and booking.BookingStatusId == BookingStatus.Confirmed) or booking.BookingStatusId == BookingStatus.Pending):
            self.response.status_code = status.HTTP_400_BAD_REQUEST
            msg = f"Booking {self.request.BookingId} is not pending therefore cannot be ammended." \
                if not self.request.CancellationRequest else f"Booking {self.request.BookingId} is not confirmed or pending therefore cannot be cancelled."
            
            self.logger.error(msg)
            raise Exception(msg)

    def _createBookingAmendment(self):
        return BookingAmmendment(
            BookingId=self.request.BookingId,
            ProposedPrice=self.request.ProposedPrice,
            StartName=self.request.StartName,
            StartLong=self.request.StartLong,
            StartLat=self.request.StartLat,
            EndName=self.request.EndName,
            EndLat=self.request.EndLat,
            StartTime=self.request.StartTime,
            CancellationRequest=self.request.CancellationRequest,
            DriverApproval=self.request.DriverApproval,
            PassengerApproval=self.request.PassengerApproval,
            Recurrance=self.request.Recurrance
        )
