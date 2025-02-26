import asyncio
import websockets
import logging
import json
import os
from src.message_handler import MessageHandler

# Configure more detailed logging for debugging
logging.basicConfig(
    level=logging.DEBUG,  # Changed from INFO to DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Get Kong Gateway URL from environment, if available
KONG_GATEWAY_URL = os.environ.get("KONG_GATEWAY_URL", None)
SERVICE_NAME = os.environ.get("SERVICE_NAME", "message-service")

# Initialize message handler
handler = MessageHandler()

async def health_handler(path, headers):
    """Handle health check requests"""
    logger.debug(f"Received request to path: {path}")
    logger.debug(f"Headers: {headers}")
    
    if path == "/health":
        return 200, {"Content-Type": "text/plain"}, b"OK"
    
    # Log all requests for debugging
    if path in ["/ws", "/message/ws"]:
        logger.info(f"WebSocket request to {path}")
        # Check for WebSocket headers
        has_upgrade = False
        has_connection = False
        for header_name, header_value in headers.items():
            if header_name.lower() == 'upgrade' and 'websocket' in header_value.lower():
                has_upgrade = True
            if header_name.lower() == 'connection' and 'upgrade' in header_value.lower():
                has_connection = True
        
        if has_upgrade and has_connection:
            logger.info("Valid WebSocket handshake headers detected")
        else:
            logger.warning("Missing proper WebSocket handshake headers")
    
    return None  # Continue normal WebSocket processing

async def websocket_handler(websocket, path):
    logger.info(f"New connection established on path: {path}")
    
    # Extract client information for logging
    remote_address = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}" if hasattr(websocket, 'remote_address') else "unknown"
    logger.info(f"Client connected from {remote_address}")
    
    # Log all headers for debugging
    logger.info("Connection headers:")
    if hasattr(websocket, 'request_headers'):
        for name, value in websocket.request_headers.items():
            logger.info(f"  {name}: {value}")
        
        # Log if the connection is coming through Kong (should have specific headers)
        if "x-forwarded-for" in websocket.request_headers:
            logger.info(f"Connection routed through proxy: {websocket.request_headers.get('x-forwarded-for')}")
    
    user_id = None
    
    try:
        async for message in websocket:
            logger.debug(f"Received message: {message[:100]}...")  # Log first 100 chars
            
            try:
                data = json.loads(message)
                # Check if this is a registration message
                if 'register' in data and data['register']:
                    if 'user_id' in data:
                        user_id = data['user_id']
                        logger.info(f"User {user_id} registered")
                        handler.register_user(user_id, websocket)
                        
                        # Send welcome message
                        await websocket.send(json.dumps({
                            "type": "welcome",
                            "message": f"Welcome, {user_id}!"
                        }))
                        continue
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON message received: {message}")
                continue
            
            # Process the message
            try:
                await handler.handle_message(websocket, message)
                # Send acknowledgment
                await websocket.send(json.dumps({
                    "type": "ack",
                    "status": "processed"
                }))
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                await websocket.send(json.dumps({
                    "type": "error",
                    "message": f"Error processing message: {str(e)}"
                }))
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: {e.code} {e.reason}")
    except Exception as e:
        logger.error(f"Error in websocket handler: {str(e)}", exc_info=True)
    finally:
        if user_id:
            handler.remove_user(user_id)
            logger.info(f"User {user_id} disconnected")
        logger.info(f"Connection from {remote_address} closed")

async def main():
    # Log startup information including environment details
    logger.info(f"Starting Message Service...")
    if KONG_GATEWAY_URL:
        logger.info(f"Kong Gateway URL: {KONG_GATEWAY_URL}")
    logger.info(f"Service Name: {SERVICE_NAME}")
    
    # Log all environment variables for debugging
    logger.debug("Environment variables:")
    for key, value in os.environ.items():
        logger.debug(f"  {key}: {value}")
    
    # Start WebSocket server
    async with websockets.serve(
        websocket_handler, 
        "0.0.0.0", 
        5006,
        process_request=health_handler
    ):
        logger.info("WebSocket server started on port 5006")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
