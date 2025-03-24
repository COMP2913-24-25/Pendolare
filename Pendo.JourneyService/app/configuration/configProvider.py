import json, os
from pathlib import Path
from .config import DbConfiguration
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..PendoDatabase import Configuration

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