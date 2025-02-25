# Provides configuration values for the application

import json
from pathlib import Path
from .db_configuration import DbConfiguration

class ConfigurationProvider:

    def __init__(self, path: str = "appsettings.json"):
        self.path = Path(path)
        self.data = self._loadConfiguration()

        self.database = DbConfiguration(**self.data.get("DbConfiguration", {}))

    def _loadConfiguration(self) -> dict:
        if self.path.exists():
            with open(self.path, 'r') as file:
                return json.load(file)
        return FileNotFoundError(f"Configuration file not found at {self.path}")