import json
import pytest
from unittest.mock import MagicMock, AsyncMock
from src.message_handler import MessageHandler
import uuid
from datetime import datetime

# Derived from: 
# https://github.com/python-websockets/websockets/issues/282

class MockWebSocket:
    """Mock WebSocket for testing"""
    
    def __init__(self):
        self.sent_messages = []
    
    async def send(self, message):
        self.sent_messages.append(message)


@pytest.fixture
def message_handler():
    """Fixture to create a MessageHandler instance with mock repository"""
    # Derived from: https://stackoverflow.com/questions/17181687/mock-vs-magicmock
    mock_repo = MagicMock()
    return MessageHandler(repository=mock_repo), mock_repo


@pytest.mark.asyncio
async def test_register_user(message_handler):
    """Test registering a user"""
    handler, _ = message_handler
    user_id = str(uuid.uuid4())
    mock_websocket = MagicMock()
    
    handler.register_user(user_id, mock_websocket)
    
    assert user_id in handler.user_connections
    assert handler.user_connections[user_id] == mock_websocket
    assert user_id in handler.message_cache


@pytest.mark.asyncio
async def test_remove_user(message_handler):
    """Test removing a user"""
    handler, _ = message_handler
    user_id = str(uuid.uuid4())
    mock_websocket = MagicMock()
    
    # Register user first
    handler.register_user(user_id, mock_websocket)
    assert user_id in handler.user_connections
    
    # Test removal
    handler.remove_user(user_id)
    assert user_id not in handler.user_connections


@pytest.mark.asyncio
async def test_handle_chat_message(message_handler):
    """Test handling chat messages"""
    handler, _ = message_handler
    
    # Setup test data
    from_user = str(uuid.uuid4())
    to_user = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    content = "Hello, this is a test message"
    
    # Setup mock websockets
    from_socket = MagicMock()
    to_socket = MagicMock()
    
    # Register users
    handler.register_user(from_user, from_socket)
    handler.register_user(to_user, to_socket)
    
    # Setup conversation
    handler.conversations[conversation_id] = {from_user, to_user}
    
    # Replace _broadcast_to_conversation with an AsyncMock to support await
    handler._broadcast_to_conversation = AsyncMock()
    
    # Create message
    message = {
        "type": "chat",
        "from": from_user,
        "conversation_id": conversation_id,
        "content": content
    }
    
    # Call handler
    await handler._handle_chat_message(message)
    
    # Verify message was stored in memory
    assert conversation_id in handler.message_store
    assert len(handler.message_store[conversation_id]) == 1
    assert handler.message_store[conversation_id][0]["content"] == content
    
    # Verify _broadcast_to_conversation was called
    handler._broadcast_to_conversation.assert_called_once()


@pytest.mark.asyncio
async def test_handle_join_conversation(message_handler):
    """Test joining a conversation"""
    handler, mock_repo = message_handler
    
    # Setup test data
    user_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    
    # Setup mock websocket to avoid actual send
    mock_socket = MagicMock()
    async def mock_send(msg):
        pass
    mock_socket.send = mock_send
    
    # Register user
    handler.register_user(user_id, mock_socket)
    
    # Create message
    message = {
        "type": "join_conversation",
        "user_id": user_id,
        "conversation_id": conversation_id
    }
    
    # Replace _broadcast_to_conversation with an AsyncMock to support await
    handler._broadcast_to_conversation = AsyncMock()
    
    # Mock repository's get_messages_by_conversation_id to return serializable data
    test_messages = [
        {
            "MessageId": str(uuid.uuid4()),
            "ConversationId": conversation_id,
            "SenderId": "test-user-1",
            "MessageType": "chat",
            "Content": "Test message 1",
            "CreateDate": datetime.now().isoformat(),
        },
        {
            "MessageId": str(uuid.uuid4()),
            "ConversationId": conversation_id,
            "SenderId": "test-user-2",
            "MessageType": "chat",
            "Content": "Test message 2",
            "CreateDate": datetime.now().isoformat(),
        }
    ]
    mock_repo.get_messages_by_conversation_id.return_value = test_messages
    
    # Mock _handle_history_request to avoid actual call
    handler._handle_history_request = AsyncMock()
    
    # Call handler
    await handler._handle_join_conversation(message)
    
    # Verify user was added to conversation
    assert conversation_id in handler.conversations
    assert user_id in handler.conversations[conversation_id]
    
    # Verify _broadcast_to_conversation was called (to notify other users)
    handler._broadcast_to_conversation.assert_called_once()
    
    # Verify _handle_history_request was called with correct arguments
    handler._handle_history_request.assert_called_once()
    args = handler._handle_history_request.call_args[0]
    assert args[0] == mock_socket  # First arg should be the websocket
    assert args[1]["conversation_id"] == conversation_id  # Second arg should be message with conversation_id


@pytest.mark.asyncio
async def test_handle_history_request(message_handler):
    """Test handling a message history request"""
    handler, mock_repo = message_handler
    
    # Setup test data
    user_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    
    # Create test messages (stored in memory)
    test_messages = [
        {
            "type": "chat",
            "from": "test-user-1",
            "conversation_id": conversation_id,
            "content": "Test message 1",
            "timestamp": datetime.now().isoformat()
        },
        {
            "type": "chat",
            "from": "test-user-2",
            "conversation_id": conversation_id,
            "content": "Test message 2",
            "timestamp": datetime.now().isoformat()
        }
    ]
    
    # Store messages in handler memory cache
    handler.message_store[conversation_id] = test_messages
    
    # Setup mock websocket
    mock_socket = MagicMock()
    sent_messages = []
    
    # Mock send method that captures sent messages
    async def mock_send(msg):
        sent_messages.append(json.loads(msg))
    
    mock_socket.send = mock_send
    
    # Have the repository return the same test messages
    mock_repo.get_messages_by_conversation_id.return_value = test_messages
    
    # Create request
    request = {
        "conversation_id": conversation_id,
        "user_id": user_id
    }
    
    # Call handler
    await handler._handle_history_request(mock_socket, request)
    
    # Check response: expect 2 messages from memory cache/repository
    assert len(sent_messages) == 1
    assert sent_messages[0]["type"] == "history_response"
    assert len(sent_messages[0]["messages"]) == 2  # 2 messages expected
    assert sent_messages[0]["messages"][0]["content"] == "Test message 1"


@pytest.mark.asyncio
async def test_broadcast_to_conversation(message_handler):
    """Test broadcasting to a conversation"""
    handler, _ = message_handler
    
    # Setup test data
    conversation_id = str(uuid.uuid4())
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    user3_id = str(uuid.uuid4())
    
    # Setup conversation
    handler.conversations[conversation_id] = {user1_id, user2_id, user3_id}
    
    # Setup mock websockets
    mock_socket1 = MagicMock()
    mock_socket2 = MagicMock()
    mock_socket3 = MagicMock()
    
    sent_messages = {
        user1_id: [],
        user2_id: [],
        user3_id: []
    }
    
    # Mock send methods to capture sent messages
    async def mock_send1(msg):
        sent_messages[user1_id].append(msg)
    
    async def mock_send2(msg):
        sent_messages[user2_id].append(msg)
    
    async def mock_send3(msg):
        sent_messages[user3_id].append(msg)
    
    mock_socket1.send = mock_send1
    mock_socket2.send = mock_send2
    mock_socket3.send = mock_send3
    
    # Register users
    handler.register_user(user1_id, mock_socket1)
    handler.register_user(user2_id, mock_socket2)
    handler.register_user(user3_id, mock_socket3)
    
    # Create test message
    message = {
        "type": "chat",
        "content": "Test broadcast message",
        "from": user1_id
    }
    
    # Call handler to broadcast to all except user1
    await handler._broadcast_to_conversation(conversation_id, message, exclude_user=user1_id)
    
    # Check that user2 and user3 received the message and user1 the echo
    assert len(sent_messages[user1_id]) == 1
    assert len(sent_messages[user2_id]) == 1
    assert len(sent_messages[user3_id]) == 1
