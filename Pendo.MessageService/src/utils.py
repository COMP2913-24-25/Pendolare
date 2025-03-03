import logging
import json
import websockets
import asyncio
import ssl

logger = logging.getLogger(__name__)

async def test_websocket_connection(url, headers=None):
    """
    Test a WebSocket connection to diagnose issues
    
    Args:
        url: WebSocket URL to connect to
        headers: Optional headers dict
    """
    try:
        logger.info(f"Testing connection to {url}")
        
        # Create SSL context for wss:// connections
        ssl_context = None
        if url.startswith('wss://'):
            ssl_context = ssl.create_default_context()
            
        # Connect with extra headers if provided
        if headers:
            async with websockets.connect(
                url, 
                ssl=ssl_context,
                extra_headers=headers
            ) as websocket:
                logger.info("Connected successfully!")
                
                # Send test message
                test_msg = json.dumps({"type": "test", "content": "Hello from test client"})
                await websocket.send(test_msg)
                logger.info(f"Sent: {test_msg}")
                
                # Wait for response with timeout
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    logger.info(f"Received: {response}")
                except asyncio.TimeoutError:
                    logger.error("Timed out waiting for response")
        else:
            # Connect without headers
            async with websockets.connect(url, ssl=ssl_context) as websocket:
                logger.info("Connected successfully without headers!")
                
                # Send test message
                test_msg = json.dumps({"type": "test", "content": "Hello from test client"})
                await websocket.send(test_msg)
                logger.info(f"Sent: {test_msg}")
                
                # Wait for response with timeout
                try:
                    response = await asyncio.wait_for(websocket.recv(), timeout=5)
                    logger.info(f"Received: {response}")
                except asyncio.TimeoutError:
                    logger.error("Timed out waiting for response")
                    
    except Exception as e:
        logger.error(f"Error testing connection: {str(e)}")
