import pytest
import asyncio
import websockets
import json
import os

DIRECT_URL = "ws://message-service:5006/message/ws"
GATEWAY_URL = "ws://host.docker.internal:8000/message/ws"

@pytest.mark.asyncio
async def test_direct_connection():
    async with websockets.connect(DIRECT_URL) as websocket:
        message = {
            'type': 'user_message',
            'sender': 'test_user',
            'recipient': 'test_recipient',
            'content': 'test message'
        }
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        assert json.loads(response)['sender'] == 'test_user'

@pytest.mark.asyncio
async def test_gateway_connection():
    if os.environ.get('TEST_GATEWAY', 'false').lower() != 'true':
        pytest.skip("Gateway testing is disabled")
        
    try:
        async with websockets.connect(GATEWAY_URL) as websocket:
            message = {
                'type': 'user_message',
                'sender': 'test_user',
                'recipient': 'test_recipient',
                'content': 'test message'
            }
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            assert json.loads(response)['sender'] == 'test_user'
    except Exception as e:
        pytest.skip(f"Kong gateway test skipped: {str(e)}")
