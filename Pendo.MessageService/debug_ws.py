import asyncio
import json
import logging
import os
import sys
import websockets
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Connection storage
connected = set()

async def echo(websocket, path):
    """Handle WebSocket connections."""
    try:
        logger.info(f"New connection from {websocket.remote_address}, path: {path}")
        logger.debug(f"Request headers: {websocket.request_headers}")
        
        # Add to connected set
        connected.add(websocket)
        logger.info(f"Total connections: {len(connected)}")
        
        # Send welcome message
        await websocket.send(json.dumps({
            "type": "welcome",
            "data": {
                "message": "Connected to Message Service",
                "timestamp": datetime.now().isoformat(),
                "path": path
            }
        }))
        
        # Listen for messages
        async for message in websocket:
            logger.info(f"Received message: {message}")
            try:
                data = json.loads(message)
                # Echo the message back
                await websocket.send(json.dumps({
                    "type": "echo",
                    "data": data,
                    "timestamp": datetime.now().isoformat()
                }))
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received: {message}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "data": {"message": "Invalid JSON format"},
                    "timestamp": datetime.now().isoformat()
                }))
    
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: {e}")
    except Exception as e:
        logger.exception(f"Error in WebSocket handler: {e}")
    finally:
        # Remove from connected set
        if websocket in connected:
            connected.remove(websocket)
            logger.info(f"Connection closed, total remaining: {len(connected)}")

async def main():
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 5006))
    
    # Log all environment variables to help with debugging
    logger.debug("Environment variables:")
    for key, value in os.environ.items():
        logger.debug(f"  {key}: {value}")

    # Print network info
    logger.info(f"Starting WebSocket server on port {port}")
    
    # Start the WebSocket server
    async with websockets.serve(echo, "0.0.0.0", port):
        logger.info(f"WebSocket server running at ws://0.0.0.0:{port}/ws")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
