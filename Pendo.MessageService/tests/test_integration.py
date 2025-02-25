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
# Use Kong container name for gateway tests
KONG_HOST = os.getenv('KONG_HOST', 'kong')
KONG_ADMIN_URL = f"http://{KONG_HOST}:8001"
GATEWAY_URL = f"ws://{KONG_HOST}:8000/message/ws"

def check_kong_status():
    try:
        response = requests.get(f"{KONG_ADMIN_URL}/status")
        if response.status_code == 200:
            logger.info("Kong is up and running")
            return True
        logger.error(f"Kong status check failed with status code: {response.status_code}")
        return False
    except requests.RequestException as e:
        logger.error(f"Failed to connect to Kong: {str(e)}")
        return False

@pytest.mark.asyncio
async def test_direct_connection():
    async with websockets.connect(DIRECT_URL) as websocket:
        message = {
            "type": "user_message",
            "sender": "test_user",
            "recipient": "test_recipient",
            "content": "test message"
        }
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        assert response is not None
        data = json.loads(response)
        assert data["type"] == "user_message"
        assert data["sender"] == "test_user"

@pytest.mark.asyncio
async def test_gateway_connection():
    if not os.getenv('TEST_GATEWAY', 'false').lower() == 'true':
        pytest.skip("Gateway tests disabled")
    
    if not check_kong_status():
        pytest.fail("Kong is not accessible")

    logger.info(f"Attempting to connect to gateway at {GATEWAY_URL}")
    try:
        async with websockets.connect(GATEWAY_URL) as websocket:
            logger.info("Connected to gateway successfully")
            message = {
                "type": "user_message",
                "sender": "test_user",
                "recipient": "test_recipient",
                "content": "test message"
            }
            logger.info(f"Sending message: {message}")
            await websocket.send(json.dumps(message))
            logger.info("Waiting for response...")
            response = await websocket.recv()
            logger.info(f"Received response: {response}")
            assert response is not None
    except Exception as e:
        logger.error(f"Gateway connection failed: {str(e)}")
        raise
