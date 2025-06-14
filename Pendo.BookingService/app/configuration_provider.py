import json
from pathlib import Path
from .configurations import DbConfiguration, SendGridConfiguration, PaymentServiceConfiguration
from sqlalchemy.orm import Session
from .models import Configuration 

class ConfigurationProvider:
    """
    ConfigurationProvider class is responsible for loading the application configuration.
    """

    def __init__(self, path: str = "appsettings.json"):
        self.path = Path(path)
        self.data = self._loadConfiguration()
        self.database = DbConfiguration(**self.data.get("DbConfiguration", {}))
        self.paymentServiceConfiguration = PaymentServiceConfiguration(**self.data.get("PaymentServiceConfiguration", {}))
        self.emailConfiguration = None

    def _loadConfiguration(self) -> dict:
        """
        Load the configuration from the appsettings.json file.
        """
        if self.path.exists():
            with open(self.path, 'r') as file:
                return json.load(file)
        raise FileNotFoundError(f"Configuration file not found at {self.path}")

    def LoadEmailConfiguration(self, db_session: Session) -> SendGridConfiguration:
        """
        Load EmailConfiguration from the database and store it in the emailConfiguration member.
        Assumes the configuration key is 'Booking.EmailConfiguration' and that the 'Value'
        is a JSON string.
        """
        config_row = db_session.query(Configuration).filter(Configuration.Key == "Booking.EmailConfiguration").first()
        db_session.close()

        if config_row:
            email_config_data = json.loads(config_row.Value)
            self.emailConfiguration = SendGridConfiguration(**email_config_data)
            return self.emailConfiguration

        raise ValueError("Email configuration not found in the database.")
    
    def GetSingleValue(self, db_session: Session, key: str) -> str:
        """
        Get a single value from the configuration.
        """
        return db_session.query(Configuration).filter(Configuration.Key == key).first().Value
