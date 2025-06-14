import json, os
from pathlib import Path
from .config import DbConfiguration, SendGridConfiguration, StripeConfiguration
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..db.PendoDatabase import Configuration

class ConfigurationProvider:
    """
    ConfigurationProvider class is responsible for loading the application configuration.
    """

    def __init__(self, path: str = "appsettings.json"):
        self.path = Path(path)
        self.data = self._loadConfiguration()
        self.database = DbConfiguration(**self.data.get("DbConfiguration", {}))
        self.emailConfiguration = None
        self.StripeConfiguration = None

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
        Assumes the configuration key is 'Payment.EmailConfiguration' and that the 'Value'
        is a JSON string.
        """
        config_row = db_session.query(Configuration).filter(Configuration.Key == "Payment.EmailConfiguration").first()

        if config_row:
            email_config_data = json.loads(config_row.Value)
            self.emailConfiguration = SendGridConfiguration(**email_config_data)
            return self.emailConfiguration

        raise ValueError("Email configuration not found in the database.")

    def LoadStripeConfiguration(self, db_session: Session) -> StripeConfiguration:
        """
        Load StripeConfiguration from the database and store it in the StripeConfiguration member.
        Assumes the configuration key is 'Payment.StripeConfiguration' and that the 'Value'
        is a JSON string.
        """
        config_row = db_session.query(Configuration).filter(Configuration.Key == "Payment.StripeConfiguration").first()

        if config_row:
            stripe_config_data = json.loads(config_row.Value)
            self.StripeConfiguration = StripeConfiguration(**stripe_config_data)
            return self.StripeConfiguration

        raise ValueError("Stripe configuration not found in the database.")