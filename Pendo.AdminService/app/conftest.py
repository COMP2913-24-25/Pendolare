import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_db_session():
    return MagicMock()

@pytest.fixture
def mock_configuration_provider():
    return MagicMock()