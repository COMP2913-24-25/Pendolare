import asyncio
import websockets
import logging
import sys
import os
import json
from datetime import datetime

# Configure logging to be container-friendly
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    stream=sys.stdout
)
logger = logging.getLogger("websocket_debug")

async def test_websocket_connection(url):
    logger.info(f"[{datetime.now()}] Testing connection to: {url}")
    
    try:
        # Connect with debug headers
        async with websockets.connect(
            url, 
            open_timeout=15,
            close_timeout=15,
            extra_headers={
                'Connection': 'Upgrade',
                'Upgrade': 'websocket',
                'User-Agent': 'Azure-Debug-Script/1.0'
            }
        ) as ws:
            logger.info(f"Connection established successfully!")
            
            # Send a test message
            test_msg = json.dumps({"type": "ping", "message": "Hello from debug script"})
            logger.info(f"Sending: {test_msg}")
            await ws.send(test_msg)
            
            # Wait for response
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=10.0)
                logger.info(f"Received response: {response}")
                
                # Keep connection open briefly
                await asyncio.sleep(5)
                
                # Try sending one more message
                logger.info("Sending second message...")
                await ws.send(json.dumps({"type": "echo", "message": "Testing echo functionality"}))
                response = await asyncio.wait_for(ws.recv(), timeout=5.0)
                logger.info(f"Echo response: {response}")
            except asyncio.TimeoutError:
                logger.error("Timeout waiting for response")
                
    except Exception as e:
        logger.error(f"Error: {e.__class__.__name__}: {e}")
        return False
        
    logger.info("Test completed successfully")
    return True

async def main():
    # Get the Kong Gateway and Message Service FQDNs
    service_fqdn = os.environ.get("MESSAGE_SERVICE_FQDN")
    kong_fqdn = os.environ.get("KONG_GATEWAY_FQDN")
    
    logger.info(f"Service FQDN: {service_fqdn}")
    logger.info(f"Kong FQDN: {kong_fqdn}")
    
    # Try direct connection first (from inside the container)
    direct_success = False
    if service_fqdn:
        logger.info("=== TESTING DIRECT CONNECTION ===")
        direct_url = f"ws://localhost:5006/ws"
        logger.info(f"Testing direct WebSocket: {direct_url}")
        direct_success = await test_websocket_connection(direct_url)
    
    # Try Kong connection 
    if kong_fqdn:
        logger.info("\n=== TESTING KONG CONNECTION ===")
        kong_url = f"wss://{kong_fqdn}/message/ws"
        logger.info(f"Testing Kong WebSocket: {kong_url}")
        await test_websocket_connection(kong_url)
    
    # If direct connection didn't work, try with proper domain
    if not direct_success and service_fqdn:
        logger.info("\n=== TESTING SERVICE VIA FQDN ===")
        ws_url = f"wss://{service_fqdn}/ws"
        logger.info(f"Testing WebSocket via domain: {ws_url}")
        await test_websocket_connection(ws_url)

if __name__ == "__main__":
    asyncio.run(main())
