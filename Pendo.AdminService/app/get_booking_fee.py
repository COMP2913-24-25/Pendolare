from fastapi import status

class GetBookingFeeCommand:
    """
    Command to retrieve the booking fee configuration.
    """
    def __init__(self, configuration_provider, response, db_session):
        """
        Initializes the GetBookingFeeCommand.

        Args:
            configuration_provider (ConfigurationProvider): Provider for accessing configuration values.
            response (Response): FastAPI response object.
            db_session (Session): SQLAlchemy database session.
        """
        self.configuration_provider = configuration_provider
        self.response = response
        self.db_session = db_session

    def Execute(self):
        """
        Executes the command to retrieve the booking fee from the configuration.

        Returns:
            Dict[str, str]: A dictionary containing the booking fee.

        Raises:
            Exception: If an error occurs during configuration retrieval.
        """
        try:
            rawValue = self.configuration_provider.GetSingleValue(self.db_session, "Booking.FeeMargin")
            return {"BookingFee": f"{float(rawValue) * 100:.2f}%"}
        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}