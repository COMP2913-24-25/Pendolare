import pytest
import os
import sys
from unittest.mock import patch, MagicMock
import logging
import json

# Derivied from: https://docs.python.org/3/howto/logging.html
@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Configure logging for tests"""
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    yield

# Derived from: https://docs.python.org/3/library/unittest.mock.html#patch-dict
@pytest.fixture(scope="session", autouse=True)
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        "ENV": "Testing",
        "LOG_LEVEL": "DEBUG",
        "WS_PORT": "9998",
        "HTTP_PORT": "9999",
        "USE_DATABASE": "false"
    }):
        yield

@pytest.fixture(scope="session", autouse=True)
def mock_config_provider():
    """Mock configuration provider for tests"""
    
    # Create a mock config with a sqlite memory database
    # Derived from: https://medium.com/@johnidouglasmarangon/how-to-setup-memory-database-test-with-pytest-and-sqlalchemy-ca2872a92708
    mock_config = {
        "Database": {
            "Provider": "sqlite",
            "Host": "localhost",
            "Port": 0,
            "Username": "test_user",
            "Password": "test_password",
            "Database": ":memory:"
        }
    }
    
    # Get the proper directory path for Docker environment
    config_dir = "/app/src/configuration"
    if not os.path.exists(config_dir):
        # Try relative path for local development
        config_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'src', 
            'configuration'
        ))
        os.makedirs(config_dir, exist_ok=True)
    
    # Write the mock config to a file
    config_path = os.path.join(config_dir, "appsettings.testing.json")
    try:
        with open(config_path, "w") as f:
            json.dump(mock_config, f)
        logging.info(f"Created test config at {config_path}")
    except Exception as e:
        logging.error(f"Could not write test config file: {e}")
    
    yield
    
    try:
        if os.path.exists(config_path):
            os.remove(config_path)
    except:
        pass

@pytest.fixture(scope="session", autouse=True)
def add_src_to_path():
    """Add src directory to Python path"""
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)

@pytest.fixture
def mock_db():
    """Create a mock database session"""
    from unittest.mock import MagicMock
    from sqlalchemy.orm import Session
    
    mock_session = MagicMock(spec=Session)
    
    yield mock_session

@pytest.fixture
def mock_repository():
    """Create a mock repository for integration tests"""
    with patch('src.app.repository') as mock_repo:
        yield mock_repo

@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket client"""
    class MockWebSocket:
        def __init__(self):
            self.sent_messages = []
            self.path = '/ws'
            self.remote_address = ('127.0.0.1', 9998)
            self.request_headers = {}
            
        async def send(self, message):
            self.sent_messages.append(message)
            return None
            
        async def recv(self):
            return '{"type": "test"}'
    
    return MockWebSocket()

@pytest.fixture
def create_message_handler():
    """Fixture to create message handler instances"""
    from src.message_handler import MessageHandler
    from unittest.mock import MagicMock
    
    def _create_handler(with_mock_repo=True):
        if with_mock_repo:
            mock_repo = MagicMock()
            return MessageHandler(repository=mock_repo), mock_repo
        return MessageHandler(repository=None), None
    
    return _create_handler
