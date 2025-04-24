import pytest
import json
import uuid
import asyncio
import websockets
from datetime import datetime
from unittest.mock import patch
from src import app
from src.message_handler import MessageHandler
import pytest_asyncio


@pytest_asyncio.fixture
async def server_setup():
    """Setup a test websocket server for testing"""
    # Mock repository
    mock_repo = None
    
    # Create and initialise handler with mock repository
    message_handler = MessageHandler(repository=mock_repo)
    
    # Patch the global message handler in app.py
    # Derived from: https://stackoverflow.com/questions/69192748/pytest-mocking-class-instance-passed-as-an-argument
    with patch('src.app.message_handler', message_handler):
        # Start server with test port
        server = await websockets.serve(
            app.websocket_handler,
            "localhost",
            9998
        )
        
        test_data = {
            "server": server,
            "message_handler": message_handler,
            "uri": "ws://localhost:9998/ws"
        }
        
        yield test_data
        
        # Cleanup
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_websocket_connection(server_setup):
    """Test connecting to the WebSocket server"""
    data = server_setup
    uri = data["uri"]
    
    async with websockets.connect(uri) as websocket:
        # Should receive welcome message
        response = await websocket.recv()
        data = json.loads(response)
        
        assert data["type"] == "welcome"
        assert "Connected to Pendo Message Service" in data["message"]


@pytest.mark.asyncio
async def test_user_registration(server_setup):
    """Test registering a user through the WebSocket"""
    data = server_setup
    uri = data["uri"]
    message_handler = data["message_handler"]
    user_id = str(uuid.uuid4())
    
    async with websockets.connect(uri) as websocket:
        # Skip welcome message
        await websocket.recv()
        
        # Register user
        await websocket.send(json.dumps({
            "register": True,
            "user_id": user_id
        }))
        
        # Yield to allow registration to complete
        await asyncio.sleep(0.1)

        assert user_id in message_handler.user_connections


@pytest.mark.asyncio
async def test_chat_message_exchange(server_setup):
    """Test sending and receiving chat messages between users"""
    data = server_setup
    uri = data["uri"]
    message_handler = data["message_handler"]
    
    user1_id = str(uuid.uuid4())
    user2_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    
    # Initialise conversation
    message_handler.conversations[conversation_id] = set([user1_id, user2_id])
    
    # Connect first user
    async with websockets.connect(uri) as user1_ws:
        await user1_ws.recv()
        
        # Register user1
        await user1_ws.send(json.dumps({
            "register": True,
            "user_id": user1_id
        }))
        
        # Connect second user
        async with websockets.connect(uri) as user2_ws:
            await user2_ws.recv()
            
            # Register user2
            await user2_ws.send(json.dumps({
                "register": True,
                "user_id": user2_id
            }))
            
            # Yield to allow registration to complete
            await asyncio.sleep(0.1)
            
            # Send message from user1 to conversation
            test_message = f"Hello at {datetime.now().isoformat()}"
            await user1_ws.send(json.dumps({
                "type": "chat",
                "from": user1_id,
                "conversation_id": conversation_id,
                "content": test_message
            }))
            
            # Wait for message to be processed
            await asyncio.sleep(0.1)
            
            # User2 should receive the message
            response = await user2_ws.recv()
            data = json.loads(response)
            
            assert data["type"] == "chat"
            assert data["from"] == user1_id
            assert data["conversation_id"] == conversation_id
            assert data["content"] == test_message


@pytest.mark.asyncio
async def test_join_conversation(server_setup):
    """Test joining a conversation"""
    data = server_setup
    uri = data["uri"]
    message_handler = data["message_handler"]
    
    user_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    
    async with websockets.connect(uri) as websocket:
        await websocket.recv()
        
        await websocket.send(json.dumps({
            "register": True,
            "user_id": user_id
        }))
        
        await asyncio.sleep(0.1)
        
        await websocket.send(json.dumps({
            "type": "join_conversation",
            "conversation_id": conversation_id,
            "user_id": user_id
        }))
        
        response = await websocket.recv()
        data = json.loads(response)
        
        assert data["type"] == "conversation_joined"
        assert data["conversation_id"] == conversation_id
        
        assert user_id in message_handler.conversations[conversation_id]


@pytest.mark.asyncio
async def test_request_message_history(server_setup):
    """Test requesting message history"""
    data = server_setup
    uri = data["uri"]
    message_handler = data["message_handler"]
    
    user_id = str(uuid.uuid4())
    conversation_id = str(uuid.uuid4())
    
    # Create some test messages
    message_handler.message_store[conversation_id] = [
        {
            "type": "chat",
            "from": "test-user",
            "conversation_id": conversation_id,
            "content": "Test message 1",
            "timestamp": "2023-01-01T12:00:00Z"
        },
        {
            "type": "chat",
            "from": "test-user",
            "conversation_id": conversation_id,
            "content": "Test message 2",
            "timestamp": "2023-01-01T12:05:00Z"
        }
    ]
    
    async with websockets.connect(uri) as websocket:
        await websocket.recv()
        
        await websocket.send(json.dumps({
            "register": True,
            "user_id": user_id
        }))
        
        await asyncio.sleep(0.1)
        
        await websocket.send(json.dumps({
            "type": "history_request",
            "conversation_id": conversation_id,
            "user_id": user_id
        }))
        
        response = await websocket.recv()
        data = json.loads(response)
        
        assert data["type"] == "history_response"
        assert "messages" in data
        assert len(data["messages"]) == 2
