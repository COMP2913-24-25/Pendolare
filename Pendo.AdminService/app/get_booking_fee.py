from fastapi import status

class GetBookingFeeCommand:
    def __init__(self, configuration_provider, response, db_session):
        self.configuration_provider = configuration_provider
        self.response = response
        self.db_session = db_session

    def Execute(self):
        """
        Get the booking fee from the configuration.
        """
        try:
            rawValue = self.configuration_provider.GetSingleValue(self.db_session, "Booking.FeeMargin")
            return {"BookingFee": f"{float(rawValue) * 100:.2f}%"}
        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}