import asyncio
import websockets
import logging
import json
import os
from src.message_handler import MessageHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = MessageHandler()

# Get Kong Gateway URL from environment, if available
KONG_GATEWAY_URL = os.environ.get("KONG_GATEWAY_URL", None)
SERVICE_NAME = os.environ.get("SERVICE_NAME", "message-service")

async def health_handler(path, headers):
    """Handle health check requests"""
    if path == "/health":
        return 200, {"Content-Type": "text/plain"}, b"OK"
    return None  # Continue normal WebSocket processing

async def websocket_handler(websocket, path):
    logger.info(f"New connection established on path: {path}")
    
    # Extract client information for logging
    client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    logger.info(f"Client connected from {client_info}")
    
    # Log if the connection is coming through Kong (should have specific headers)
    if "x-forwarded-for" in websocket.request_headers:
        logger.info(f"Connection routed through Kong Gateway: {websocket.request_headers.get('x-forwarded-for')}")
    
    user_id = None
    
    try:
        async for message in websocket:
            logger.info(f"Received message: {message[:100]}...")  # Log first 100 chars
            
            try:
                data = json.loads(message)
                # Check if this is a registration message
                if 'register' in data and data['register']:
                    if 'user_id' in data:
                        user_id = data['user_id']
                        logger.info(f"User {user_id} registered")
                        handler.register_user(user_id, websocket)
            except json.JSONDecodeError:
                logger.error("Invalid JSON message received")
                continue
                
            await handler.handle_message(websocket, message)
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: {e.code} {e.reason}")
    except Exception as e:
        logger.error(f"Error in websocket handler: {str(e)}")
    finally:
        if user_id:
            handler.remove_user(user_id)
            logger.info(f"User {user_id} disconnected")
        logger.info("Connection closed")

async def main():
    # Log startup information including environment details
    logger.info(f"Starting Message Service...")
    if KONG_GATEWAY_URL:
        logger.info(f"Kong Gateway URL: {KONG_GATEWAY_URL}")
    logger.info(f"Service Name: {SERVICE_NAME}")
    
    # Start WebSocket server
    async with websockets.serve(
        websocket_handler, 
        "0.0.0.0", 
        5006,
        process_request=health_handler
    ):
        logger.info("WebSocket server started on port 5006")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
