from fastapi import status
from sqlalchemy.orm import Session

class UpdateBookingFeeCommand:
    def __init__(self, db_session: Session, request, response, configuration_provider, logger):
        self.db_session = db_session
        self.request = request
        self.response = response
        self.configuration_provider = configuration_provider
        self.logger = logger

    def Execute(self):
        try:
            self.logger.info("Updating booking fee margin")
            fee_margin = self.request.FeeMargin

            if fee_margin < 0.00 or fee_margin > 0.99:
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                error = "Fee margin must be between 0.00 and 0.99"
                self.logger.error(error)
                return {"Error": error}

            self.configuration_provider.UpdateValue(self.db_session, "Booking.FeeMargin", str(fee_margin))
            self.db_session.commit()

            self.logger.info("Booking fee margin updated successfully")
            return {"Status": "Booking fee margin updated successfully"}
        
        except Exception as e:
            self.db_session.rollback()
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.logger.error(str(e))
            return {"Error": str(e)}