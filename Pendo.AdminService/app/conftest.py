import pytest
from unittest.mock import MagicMock

@pytest.fixture
def configuration_provider_mock():
    return MagicMock()

@pytest.fixture
def response_mock():
    return MagicMock()

@pytest.fixture
def db_session_mock():
    return MagicMock()

@pytest.fixture
def request_mock():
    return MagicMock()

@pytest.fixture
def logger_mock():
    return MagicMock()