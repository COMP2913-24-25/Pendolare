import pytest
import json
from src.message_handler import MessageHandler, MessageType
from src.app import websocket_handler

@pytest.fixture
def message_handler():
    return MessageHandler()

@pytest.mark.asyncio
async def test_user_message(message_handler):
    mock_ws = MockWebSocket()
    message = {
        'type': 'user_message',
        'sender': 'user1',
        'recipient': 'user2',
        'content': 'Hello'
    }
    
    await message_handler.handle_message(mock_ws, json.dumps(message))
    assert mock_ws.sent_messages

@pytest.mark.asyncio
async def test_websocket_path():
    mock_ws = MockWebSocket()
    
    # Test with Kong stripped path
    await websocket_handler(mock_ws, '/')
    assert mock_ws.connected == True
    
    # Test with full path
    mock_ws.test_messages = ['{"type": "user_message", "sender": "test", "recipient": "test2", "content": "hello"}']
    await websocket_handler(mock_ws, '/message/ws')
    assert mock_ws.connected == True
    assert len(mock_ws.sent_messages) > 0
    
    # Test with invalid path
    mock_ws = MockWebSocket()
    await websocket_handler(mock_ws, '/invalid')
    assert mock_ws.connected == False

class MockWebSocket:
    def __init__(self):
        self.sent_messages = []
        self.connected = False
        self.test_messages = []
        
    async def send(self, message):
        self.sent_messages.append(message)
        self.connected = True
