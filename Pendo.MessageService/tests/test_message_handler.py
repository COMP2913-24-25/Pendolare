import pytest
import json
import time
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
    sent_data = json.loads(mock_ws.sent_messages[0])
    assert sent_data['type'] == 'user_message_sent'

@pytest.mark.asyncio
async def test_user_registration(message_handler):
    mock_ws = MockWebSocket()
    message = {
        'register': True,
        'user_id': 'user1'
    }
    
    await message_handler.handle_message(mock_ws, json.dumps(message))
    assert 'user1' in message_handler.connections

@pytest.mark.asyncio
async def test_message_caching(message_handler):
    # Register first user
    sender_ws = MockWebSocket()
    message_handler.register_user('sender', sender_ws)
    
    # Send a message to a non-connected user
    message = {
        'type': 'user_message',
        'sender': 'sender',
        'recipient': 'offline_user',
        'content': 'Hello offline user'
    }
    
    await message_handler.handle_message(sender_ws, json.dumps(message))
    
    # Verify message was cached
    assert 'offline_user' in message_handler.message_cache
    assert len(message_handler.message_cache['offline_user']) == 1
    
    # Connect the offline user and check if they receive the cached message
    recipient_ws = MockWebSocket()
    register_message = {
        'register': True,
        'user_id': 'offline_user'
    }
    
    await message_handler.handle_message(recipient_ws, json.dumps(register_message))
    
    # Check that the history response was sent
    assert len(recipient_ws.sent_messages) == 1
    history_response = json.loads(recipient_ws.sent_messages[0])
    assert history_response['type'] == 'history_response'
    assert len(history_response['messages']) == 1

@pytest.mark.asyncio
async def test_history_request(message_handler):
    # Setup: register user and add some messages
    user_ws = MockWebSocket()
    message_handler.register_user('test_user', user_ws)
    
    # Add messages to cache manually
    message_handler.message_cache['test_user'] = [
        {
            'type': 'user_message',
            'sender': 'other_user',
            'recipient': 'test_user',
            'content': 'Message 1',
            'timestamp': '2023-01-01T10:00:00'
        },
        {
            'type': 'user_message',
            'sender': 'other_user',
            'recipient': 'test_user',
            'content': 'Message 2',
            'timestamp': '2023-01-01T10:05:00'
        }
    ]
    
    # Request history
    history_request = {
        'type': 'history_request',
        'user_id': 'test_user'
    }
    
    await message_handler.handle_message(user_ws, json.dumps(history_request))
    
    # Check response
    assert len(user_ws.sent_messages) == 1
    history = json.loads(user_ws.sent_messages[0])
    assert history['type'] == 'history_response'
    assert len(history['messages']) == 2

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
