import json
from pathlib import Path
from sqlalchemy.orm import Session
from models import Configuration
from configurations import DbConfiguration

class ConfigurationProvider:
    """
    ConfigurationProvider class is responsible for loading the application configuration.
    """

    def __init__(self, path: str = "appsettings.development.json"):
        self.path = Path(path)
        self.data = self._loadConfiguration()
        self.database = DbConfiguration(**self.data.get("DbConfiguration", {}))

    def _loadConfiguration(self) -> dict:
        """
        Load the configuration from the appsettings.json file.
        """
        if self.path.exists():
            with open(self.path, 'r') as file:
                return json.load(file)
        raise FileNotFoundError(f"Configuration file not found at {self.path}")
    
    def GetSingleValue(self, db_session: Session, key: str) -> str:
        """
        Get a single value from the configuration.
        """
        return db_session.query(Configuration).filter(Configuration.Key == key).first().Value
    
    def UpdateValue(self, db_session: Session, key: str, value: str):
        """
        Update a single value in the configuration.
        """
        config = db_session.query(Configuration).filter(Configuration.Key == key).first()
        config.Value = value
        db_session.commit()
