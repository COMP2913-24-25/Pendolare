from .booking_repository import BookingRepository, Booking
from datetime import datetime

class CreateBookingCommand:
    """
    CreateBookingCommand class is responsible for creating a new booking.
    """

    def __init__(self, request, email_sender, logger):
        """
        Constructor for CreateBookingCommand class.
        :param request: Request object containing the booking details.
        """
        self.booking_repository = BookingRepository()
        self.email_sender = email_sender
        self.request = request
        self.logger = logger

    def Execute(self):
        """
        Execute method creates a new booking.
        :return: Response object containing the status of the operation.
        """
        try:
            user = self.booking_repository.GetUser(self.request.UserId)
            if user is None:
                raise Exception("User not found")
            
            journey = self.booking_repository.GetJourney(self.request.JourneyId)
            if journey is None:
                raise Exception("Journey not found")
            
            existing_booking = self.booking_repository.GetExistingBooking(user.UserId, journey.JourneyId)
            if existing_booking is not None:
                raise Exception("Booking already exists")
            
            booking = Booking(
                UserId=user.UserId,
                JourneyId=journey.JourneyId,
                BookingStatusId=1, #Pending - this should not change!
            )

            self.booking_repository.CreateBooking(booking)
            self.logger.debug(f"Booking DB object created successfully. BookingId: {booking.BookingId}")

            email_data = {
                "booking_id": f"{booking.BookingId}",
                "driver_name": "Get from journey",
                "pickup_location": "Get from journey",
                "pickup_time": "08:30 AM",
                "pickup_date": "2025-03-15",
                "dropoff_location": "Get from journey",
                "estimated_arrival": "09:15 AM",
                "vehicle_info": "Mazda MX-5 Blue"
            }

            self.email_sender.SendBookingPending(user.Email, email_data)
            self.logger.debug("Booking pending email sent successfully.")

            self.logger.info(f"Booking created successfully. BookingId: {booking.BookingId}")
            return {"Status": "Success", "createTime": datetime.now()}
        except Exception as e:
            self.logger.error(f"Error creating booking. Error: {str(e)}")
            return {"Status": "Failed", "Error": str(e)}
