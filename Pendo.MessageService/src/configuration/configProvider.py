import json, os
from pathlib import Path
from .config import DbConfiguration, SendGridConfiguration, StripeConfiguration
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging

# Setup logging
logger = logging.getLogger(__name__)

class ConfigurationProvider:
    """
    ConfigurationProvider class is responsible for loading the application configuration.
    """

    def __init__(self, path: str = "appsettings.json"):
        self.path = Path(path)
        self.data = self._loadConfiguration()

        # Load database configuration
        db_data = self.data.get("Database") or self.data.get("DbConfiguration", {})
        self.database = DbConfiguration(**db_data)

        self.emailConfiguration = None
        self.StripeConfiguration = None

    def _loadConfiguration(self) -> dict:
        """
        Load the configuration from the appsettings.json file.
        Falls back to default values if file is not found.
        """
        if self.path.exists():
            try:
                with open(self.path, 'r') as file:
                    return json.load(file)
            except Exception as e:
                logger.error(f"Error reading configuration file: {e}")
                # Return default configuration
                return self._getDefaultConfiguration()
        
        # If in testing mode, don't raise an exception, just log and return default config
        environment = os.environ.get("ENV", "Production")
        if environment == "Testing":
            logger.warning(f"Configuration file not found at {self.path} in Testing environment. Using default configuration.")
            return self._getDefaultConfiguration()
        
        # In production mode, still raise error for missing config
        raise FileNotFoundError(f"Configuration file not found at {self.path}")
    
    def _getDefaultConfiguration(self) -> dict:
        """
        Returns a default configuration when file is not available.
        """
        return {
            "Database": {
                "Provider": "sqlite",
                "Host": "localhost",
                "Port": 0,
                "Username": "test_user",
                "Password": "test_password",
                "Database": ":memory:"
            }
        }

    def LoadEmailConfiguration(self, db_session: Session) -> SendGridConfiguration:
        """
        Load EmailConfiguration from the database and store it in the emailConfiguration member.
        Assumes the configuration key is 'Booking.EmailConfiguration' and that the 'Value'
        is a JSON string.
        """
        try:
            from ..db.PendoDatabase import Configuration
            config_row = db_session.query(Configuration).filter(Configuration.Key == "Booking.EmailConfiguration").first()

            if config_row:
                email_config_data = json.loads(config_row.Value)
                self.emailConfiguration = SendGridConfiguration(**email_config_data)
                return self.emailConfiguration
        except Exception as e:
            logger.error(f"Error loading email configuration: {e}")
            # Return mock configuration in case of error
            return SendGridConfiguration(
                apiKey="mock-api-key",
                fromEmail="test@example.com",
                pendingTemplateId="mock-template-id-1",
                confirmedTemplateId="mock-template-id-2",
                cancelledTemplateId="mock-template-id-3"
            )

        raise ValueError("Email configuration not found in the database.")

    def LoadStripeConfiguration(self, db_session: Session) -> StripeConfiguration:
        """
        Load StripeConfiguration from the database and store it in the StripeConfiguration member.
        Assumes the configuration key is 'Payment.StripeConfiguration' and that the 'Value'
        is a JSON string.
        """
        try:
            from ..db.PendoDatabase import Configuration
            config_row = db_session.query(Configuration).filter(Configuration.Key == "Payment.StripeConfiguration").first()

            if config_row:
                stripe_config_data = json.loads(config_row.Value)
                self.StripeConfiguration = StripeConfiguration(**stripe_config_data)
                return self.StripeConfiguration
        except Exception as e:
            logger.error(f"Error loading stripe configuration: {e}")
            # Return mock configuration in case of error
            return StripeConfiguration(
                secret="mock-secret-key",
                publishable="mock-publishable-key"
            )

        raise ValueError("Stripe configuration not found in the database.")