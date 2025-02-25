# Provides configuration values for the application

import json
import os
from pathlib import Path

class ConfigurationProvider:

    def __init__(self, path: str = "appsettings.json"):
        self.path = Path(path)
        self.data = self._loadConfiguration()

    def _loadConfiguration(self) -> dict:
        if self.path.exists():
            with open(self.path, 'r') as file:
                return json.load(file)
        return {}
    
    def GetSection(self, key : str):
        return self.data.get(key, {})