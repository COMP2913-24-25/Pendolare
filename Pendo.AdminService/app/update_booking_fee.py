from fastapi import status
from sqlalchemy.orm import Session
from configuration_provider import ConfigurationProvider

class UpdateBookingFeeCommand:
    def __init__(self, db_session: Session, request, response, configuration_provider):
        self.db_session = db_session
        self.request = request
        self.response = response
        self.configuration_provider = configuration_provider

    def Execute(self):
        try:
            fee_margin = self.request.FeeMargin
            # Ensuring that the value is between 0.00 and 0.99
            if fee_margin < 0.00 or fee_margin > 0.99:
                self.response.status_code = status.HTTP_400_BAD_REQUEST
                return {"Error": "Fee margin must be between 0.00 and 0.99"}
            
            self.configuration_provider.UpdateValue(self.db_session, "Booking.FeeMargin", str(fee_margin))
            self.db_session.commit()

            return {"Status": "Booking fee margin updated successfully"}
        
        except Exception as e:
            self.response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return {"Error": str(e)}

