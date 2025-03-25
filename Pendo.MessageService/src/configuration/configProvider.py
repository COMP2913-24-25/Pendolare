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