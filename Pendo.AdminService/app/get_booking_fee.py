from fastapi import status

class GetBookingFeeCommand:
    """
    Command to retrieve the booking fee configuration.
    """
    def __init__(self, configuration_provider, response, db_session, logger):
        """
        Initializes the GetBookingFeeCommand.

        Args:
            configuration_provider (ConfigurationProvider): Provider for accessing configuration values.
            response (Response): FastAPI response object.
            db_session (Session): SQLAlchemy database session.
            logger (Logger): Logger instance.
        """
        self.configuration_provider = configuration_provider
        self.response = response
        self.db_session = db_session
        self.logger = logger

    def Execute(self):
        """
        Executes the command to retrieve the booking fee from the configuration.

        Returns:
            Dict[str, str]: A dictionary containing the booking fee.

        Raises:
            Exception: If an error occurs during configuration retrieval.
        """
        try:
            self.logger.info("Retrieving booking fee from configuration")

            rawValue = self.configuration_provider.GetSingleValue(self.db_session, "Booking.FeeMargin")

            self.logger.info(f"Booking fee is {rawValue}")

            return {"BookingFee": f"{float(rawValue) * 100:.2f}%"}
        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.logger.error(f"Error retrieving booking fee: {e}")
            return {"Error": str(e)}