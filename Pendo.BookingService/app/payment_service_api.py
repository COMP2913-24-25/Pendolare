import requests
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from uuid import UUID

class PaymentServiceClient:
    """
    PaymentServiceClient is a client for the payment service API.
    """

    def __init__(self, paymentServiceConfiguration, logger):
        self.paymentServiceConfiguration = paymentServiceConfiguration
        self.logger = logger

    def PendingBookingRequest(self, bookingId, amount):
        """
        Calls the /PendingBooking endpoint to notify the payment service of a new booking.
        """
        self.logger.info(f"Sending pending booking request to payment service for booking {bookingId}")

        request = {
            "BookingId": bookingId,
            "LatestPrice": amount
        }

        self.logger.debug(f"Sending pending booking request to payment service: {request}")
        response = requests.post(f"{self.paymentServiceConfiguration.paymentServiceUrl}/PendingBooking", json=request)
        self.logger.debug(f"Received response from payment service: {response.json()}")

        return self._processResponse(response)

    def CompletedBookingRequest(self, bookingId, latestPrice):
        """
        Calls the /CompletedBooking endpoint to notify the payment service of a completed booking and charge the user.
        """
        self.logger.info(f"Sending completed booking request to payment service for booking {bookingId}")

        request = {
            "BookingId": bookingId,
            "LatestPrice": latestPrice
        }

        self.logger.debug(f"Sending completed booking request to payment service: {request}")
        
        response = requests.post(f"{self.paymentServiceConfiguration.paymentServiceUrl}/CompletedBooking", json=request)
        self.logger.debug(f"Received response from payment service: {response.json()}")

        return self._processResponse(response)
    
    def RefundRequest(self, userId, bookingId, bookingTime, requestTime, refundAmount):
        """
        Calls the /Refund endpoint to refund a user.
        """
        self.logger.info(f"Sending refund request to payment service for user {userId}")

        request = { 
            "BookingId": bookingId, 
            "CancelledById": userId, 
            "LatestPrice": refundAmount,
            "CancellationTime": requestTime,
            "JourneyTime": bookingTime
             }

        self.logger.debug(f"Sending refund request to payment service: {request}")
        response = requests.post(f"{self.paymentServiceConfiguration.paymentServiceUrl}/RefundPayment", json=request)
        self.logger.debug(f"Received response from payment service: {response.json()}")

        return self._processResponse(response)

    def _processResponse(self, response):
        """
        _processResponse method processes the response from the payment service.
        """
        response = response.json()

        if "Status" not in response:
            msg = "Invalid response from payment service"
            self.logger.error(msg)
            raise Exception(msg)
        
        # This should be an error code really but we'll just check for the string for now.
        if response["Error"] == "Not enough user balance to set journey to pending":
            self.logger.warn("User balance insufficient to create pending booking")
            return False
        
        if response["Status"].lower() != "success":
            msg = f"Payment service returned an error: {response['Error']}"
            self.logger.error(msg)
            raise Exception(msg)
        
        self.logger.info("Payment service request successful.")
        return True