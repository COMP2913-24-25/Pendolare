import pytest
import asyncio
import websockets
import os
import json
import logging
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use service name for direct connection within Docker network
DIRECT_URL = "ws://message-service:5006/message/ws"

@pytest.mark.asyncio
async def test_direct_connection():
    """Test direct connection to the message service"""
    try:
        logger.info(f"Connecting directly to message service at {DIRECT_URL}")
        async with websockets.connect(DIRECT_URL) as websocket:
            # Register as a test user
            registration = {
                'register': True,
                'user_id': 'test_user_direct'
            }
            await websocket.send(json.dumps(registration))
            
            # Send a ping message
            ping = {
                'type': 'user_message',
                'sender': 'test_user_direct',
                'recipient': 'echo',
                'content': 'ping'
            }
            await websocket.send(json.dumps(ping))
            
            # Expect a confirmation response
            response = await websocket.recv()
            response_data = json.loads(response)
            assert response_data['type'] == 'user_message_sent'
            assert response_data['recipient'] == 'echo'
            
            logger.info("Direct connection test passed")
    except Exception as e:
        logger.error(f"Direct connection test failed: {e}")
        raise

async def receive_until_type(websocket, expected_type):
    """
    Receive messages from the websocket until a message of the expected type is received.
    Return the message of the expected type.
    """
    while True:
        message = await websocket.recv()
        message_data = json.loads(message)
        if message_data['type'] == expected_type:
            return message_data
        logger.info(f"Skipping message of type {message_data['type']}")

@pytest.mark.asyncio
async def test_message_exchange():
    """Test message exchange between two clients"""
    # Connect first client
    async with websockets.connect(DIRECT_URL) as client1:
        # Register first user
        await client1.send(json.dumps({
            'register': True,
            'user_id': 'client1'
        }))
        
        # Connect second client
        async with websockets.connect(DIRECT_URL) as client2:
            # Register second user
            await client2.send(json.dumps({
                'register': True,
                'user_id': 'client2'
            }))
            
            # Client 1 sends message to client 2
            await client1.send(json.dumps({
                'type': 'user_message',
                'sender': 'client1',
                'recipient': 'client2',
                'content': 'Hello from client 1'
            }))
            
            # Client 1 expects confirmation, but might get history first
            response1_data = await receive_until_type(client1, 'user_message_sent')
            assert response1_data['recipient'] == 'client2'
            
            # Client 2 should receive the message
            message_data = await receive_until_type(client2, 'user_message')
            assert message_data['sender'] == 'client1'
            assert message_data['content'] == 'Hello from client 1'
            
            # Client 2 replies to client 1
            await client2.send(json.dumps({
                'type': 'user_message',
                'sender': 'client2',
                'recipient': 'client1',
                'content': 'Hello from client 2'
            }))
            
            # Client 2 expects confirmation
            response2_data = await receive_until_type(client2, 'user_message_sent')
            assert response2_data['recipient'] == 'client1'
            
            # Client 1 should receive the reply
            reply_data = await receive_until_type(client1, 'user_message')
            assert reply_data['sender'] == 'client2'
            assert reply_data['content'] == 'Hello from client 2'

@pytest.mark.asyncio
async def test_message_history():
    """Test message history functionality"""
    # Connect first client and send a message
    async with websockets.connect(DIRECT_URL) as client1:
        # Register first user
        await client1.send(json.dumps({
            'register': True, 
            'user_id': 'history_client1'
        }))
        
        # Connect second client
        async with websockets.connect(DIRECT_URL) as client2:
            # Register second user
            await client2.send(json.dumps({
                'register': True,
                'user_id': 'history_client2'
            }))
            
            # Client 1 sends two messages to client 2
            await client1.send(json.dumps({
                'type': 'user_message',
                'sender': 'history_client1',
                'recipient': 'history_client2',
                'content': 'First message'
            }))
            
            # Wait for confirmation
            await client1.recv()
            
            # Client 2 should receive the message
            await client2.recv()
            
            await client1.send(json.dumps({
                'type': 'user_message',
                'sender': 'history_client1',
                'recipient': 'history_client2',
                'content': 'Second message'
            }))
            
            # Wait for confirmation
            await client1.recv()
            
            # Client 2 should receive the message
            await client2.recv()
            
        # Client 2 disconnected, now reconnect
        async with websockets.connect(DIRECT_URL) as client2_new:
            # Register with same ID to get history
            await client2_new.send(json.dumps({
                'register': True,
                'user_id': 'history_client2'
            }))
            
            # Should receive history response with missed messages
            history = await client2_new.recv()
            history_data = json.loads(history)
            
            assert history_data['type'] == 'history_response'
            assert len(history_data['messages']) >= 2
            
            # Request explicit history
            await client2_new.send(json.dumps({
                'type': 'history_request',
                'user_id': 'history_client2'
            }))
            
            # Should receive full history
            full_history = await client2_new.recv()
            full_history_data = json.loads(full_history)
            
            assert full_history_data['type'] == 'history_response'
            assert len(full_history_data['messages']) >= 2
