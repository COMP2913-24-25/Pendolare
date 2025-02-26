import asyncio
import logging
import json
import os
import sys
import websockets
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("websocket-debugger")

async def connect_to_service(uri, num_messages=3, interval=2):
    """Connect to WebSocket service and send test messages"""
    logger.info(f"Attempting to connect to {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info(f"Successfully connected to {uri}")
            
            # Register user
            register_message = {
                "register": True,
                "user_id": f"debug-client-{datetime.now().timestamp()}"
            }
            await websocket.send(json.dumps(register_message))
            logger.info(f"Sent registration message: {register_message}")
            
            # Send test messages
            for i in range(num_messages):
                message = {
                    "type": "test_message",
                    "content": f"Test message {i+1}",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(message))
                logger.info(f"Sent message: {message}")
                
                try:
                    # Wait for response with timeout
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    logger.info(f"Received response: {response}")
                except asyncio.TimeoutError:
                    logger.warning("No response received within timeout")
                
                # Wait between messages
                await asyncio.sleep(interval)
                
            logger.info("Test completed successfully")
            
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"Connection closed with code {e.code}: {e.reason}")
    except Exception as e:
        logger.error(f"Connection error: {str(e)}")

def test_direct_connection():
    """Test direct connection to the message service (without Kong)"""
    service_fqdn = os.environ.get("MESSAGE_SERVICE_FQDN")
    
    if not service_fqdn:
        logger.error("MESSAGE_SERVICE_FQDN environment variable not set")
        return
    
    uri = f"wss://{service_fqdn}/ws"
    asyncio.run(connect_to_service(uri))

def test_kong_connection():
    """Test connection through Kong Gateway"""
    kong_fqdn = os.environ.get("KONG_GATEWAY_URL")
    
    if not kong_fqdn:
        logger.error("KONG_GATEWAY_URL environment variable not set")
        return
    
    # Remove https:// if present
    if kong_fqdn.startswith("https://"):
        kong_fqdn = kong_fqdn[8:]
    
    uri = f"wss://{kong_fqdn}/ws"
    asyncio.run(connect_to_service(uri))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "kong":
        logger.info("Testing connection through Kong Gateway")
        test_kong_connection()
    else:
        logger.info("Testing direct connection to message service")
        test_direct_connection()
