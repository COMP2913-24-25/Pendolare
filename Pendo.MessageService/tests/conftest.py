import pytest
import asyncio
import websockets
import json
import logging
from src.message_handler import MessageHandler

class MockWebSocket:
    def __init__(self):
        self.sent_messages = []
        self.connected = False
        self.test_messages = []
        
    async def send(self, message):
        self.sent_messages.append(message)
        self.connected = True
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.connected = False

@pytest.fixture
def mock_websocket():
    return MockWebSocket()

@pytest.fixture
def message_handler():
    return MessageHandler()
