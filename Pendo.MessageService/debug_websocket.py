import asyncio
import websockets
import logging
import sys
import argparse

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("websocket_debug")

async def test_websocket_connection(url):
    logger.info(f"Attempting to connect to WebSocket at: {url}")
    
    try:
        # Connect with verbose error handling
        async with websockets.connect(url, open_timeout=10, extra_headers={
            'Connection': 'Upgrade',
            'Upgrade': 'websocket',
            'Sec-WebSocket-Version': '13'
        }) as ws:
            logger.info(f"Connection established to {url}")
            
            # Send a test message
            test_msg = "PING_TEST"
            logger.info(f"Sending message: {test_msg}")
            await ws.send(test_msg)
            
            # Wait for response
            logger.info("Waiting for response...")
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=5.0)
                logger.info(f"Received response: {response}")
            except asyncio.TimeoutError:
                logger.error("Timeout waiting for response")
            
            # Keep connection alive briefly
            await asyncio.sleep(1)
            
    except websockets.exceptions.InvalidStatusCode as e:
        logger.error(f"Invalid status code: {e.status_code}")
        logger.error(f"Response headers: {e.headers}")
        logger.error(f"Response body: {e.body}")
    except websockets.exceptions.InvalidMessage as e:
        logger.error(f"Invalid message: {e}")
    except websockets.exceptions.ConnectionClosed as e:
        logger.error(f"Connection closed unexpectedly: code={e.code}, reason={e.reason}")
    except Exception as e:
        logger.error(f"Error occurred: {type(e).__name__}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="WebSocket Connection Debugger")
    parser.add_argument("--direct", action="store_true", help="Test direct connection to the message service")
    parser.add_argument("--kong", action="store_true", help="Test connection through Kong Gateway")
    args = parser.parse_args()
    
    if not (args.direct or args.kong):
        logger.info("No connection type specified, testing both direct and Kong Gateway connections")
        args.direct = True
        args.kong = True
    
    # URLs for testing
    direct_url = "wss://message-service.greensand-8499b34e.uksouth.azurecontainerapps.io/ws"
    kong_url = "wss://kong-gateway.greensand-8499b34e.uksouth.azurecontainerapps.io/message/ws"

    async def run_tests():
        if args.direct:
            logger.info("Testing direct connection to message service...")
            await test_websocket_connection(direct_url)
        
        if args.kong:
            logger.info("Testing connection through Kong Gateway...")
            await test_websocket_connection(kong_url)
    
    asyncio.run(run_tests())
