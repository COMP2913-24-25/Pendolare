import asyncio
import websockets
import logging
import json
import os
from src.message_handler import MessageHandler
from src.diagnostics import handle_diagnostics_request, update_stats

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Get environment variables
KONG_GATEWAY_URL = os.environ.get("KONG_GATEWAY_URL", None)
SERVICE_NAME = os.environ.get("SERVICE_NAME", "message-service")

# Initialize message handler
handler = MessageHandler()

async def process_request(path, headers):
    """Process HTTP requests including health checks and diagnostics"""
    logger.debug(f"Received request to path: {path}")
    
    # Health check endpoint
    if path == "/health":
        return 200, {"Content-Type": "text/plain"}, b"OK"
    
    # New diagnostics endpoints
    diagnostic_response = await handle_diagnostics_request(path)
    if diagnostic_response:
        return diagnostic_response
    
    # WebSocket logging for debugging
    if path in ["/ws", "/message/ws"]:
        logger.info(f"WebSocket request to {path}")
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
    """Handle WebSocket connections"""
    logger.info(f"New connection established on path: {path}")
    remote_address = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}" if hasattr(websocket, 'remote_address') else "unknown"
    logger.info(f"Client connected from {remote_address}")
    
    # Update stats
    update_stats('connection_open')
    
    # Log headers for debugging
    logger.debug("Connection headers:")
    if hasattr(websocket, 'request_headers'):
        for name, value in websocket.request_headers.items():
            logger.debug(f"  {name}: {value}")
        
        if "x-forwarded-for" in websocket.request_headers:
            logger.info(f"Connection routed through proxy: {websocket.request_headers.get('x-forwarded-for')}")
    
    user_id = None
    
    try:
        async for message in websocket:
            logger.debug(f"Received message: {message[:100]}...")
            update_stats('message_received')
            
            try:
                data = json.loads(message)
                if 'register' in data and data['register'] and 'user_id' in data:
                    user_id = data['user_id']
                    logger.info(f"User {user_id} registered")
                    handler.register_user(user_id, websocket)
                    
                    await websocket.send(json.dumps({
                        "type": "welcome",
                        "message": f"Welcome, {user_id}!"
                    }))
                    update_stats('message_sent')
                    continue
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON message received: {message}")
                continue
            
            # Process message
            try:
                await handler.handle_message(websocket, message)
                await websocket.send(json.dumps({"type": "ack", "status": "processed"}))
                update_stats('message_sent')
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                update_stats('connection_fail', error=str(e))
                await websocket.send(json.dumps({"type": "error", "message": f"Error: {str(e)}"}))
                update_stats('message_sent')
                
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: {e.code} {e.reason}")
        update_stats('connection_close')
    except Exception as e:
        logger.error(f"Error in websocket handler: {str(e)}", exc_info=True)
        update_stats('connection_fail', error=str(e))
    finally:
        if user_id:
            handler.remove_user(user_id)
        logger.info(f"Connection from {remote_address} closed")
        update_stats('connection_close')

async def main():
    """Main service entry point"""
    logger.info(f"Starting Message Service...")
    if KONG_GATEWAY_URL:
        logger.info(f"Kong Gateway URL: {KONG_GATEWAY_URL}")
    logger.info(f"Service Name: {SERVICE_NAME}")
    
    # Start WebSocket server
    async with websockets.serve(websocket_handler, "0.0.0.0", 5006, process_request=process_request):
        logger.info("WebSocket server started on port 5006")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
