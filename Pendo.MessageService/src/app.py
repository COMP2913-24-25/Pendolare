import asyncio
import websockets
import logging
import json
import os
from src.message_handler import MessageHandler
from src.http_server import start_http_server, update_status

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Get environment variables
KONG_GATEWAY_URL = os.environ.get("KONG_GATEWAY_URL", None)
SERVICE_NAME = os.environ.get("SERVICE_NAME", "message-service")
HTTP_PORT = int(os.environ.get("HTTP_PORT", 5007))  # Separate port for HTTP server

# Initialize message handler
handler = MessageHandler()

async def fallback_health_check(path, headers):
    """
    Simple health check handler for direct WebSocket requests
    This is a fallback in case the HTTP server is not accessible
    """
    if path == "/health":
        logger.info("Health check requested through WebSocket server")
        return 200, {"Content-Type": "text/plain"}, b"OK"
    return None  # Continue with normal WebSocket handling

async def websocket_handler(websocket, path):
    """Handle WebSocket connections"""
    logger.info(f"New connection established on path: {path}")
    update_status('connection_opened', True)
    
    remote_address = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}" if hasattr(websocket, 'remote_address') else "unknown"
    logger.info(f"Client connected from {remote_address}")
    
    # Log headers for debugging
    if hasattr(websocket, 'request_headers'):
        logger.debug(f"Connection headers: {websocket.request_headers}")
        
        if "x-forwarded-for" in websocket.request_headers:
            logger.info(f"Connection routed through proxy: {websocket.request_headers.get('x-forwarded-for')}")
    
    user_id = None
    
    try:
        async for message in websocket:
            logger.debug(f"Received message: {message[:100]}...")
            
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
                    continue
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON message received: {message}")
                continue
            
            # Process message
            try:
                await handler.handle_message(websocket, message)
                await websocket.send(json.dumps({"type": "ack", "status": "processed"}))
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
                update_status('error', str(e))
                await websocket.send(json.dumps({"type": "error", "message": f"Error: {str(e)}"}))
                
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed: {e.code} {e.reason}")
    except Exception as e:
        logger.error(f"Error in websocket handler: {str(e)}", exc_info=True)
        update_status('error', str(e))
    finally:
        if user_id:
            handler.remove_user(user_id)
        logger.info(f"Connection from {remote_address} closed")
        update_status('connection_closed', True)

async def main():
    """Main service entry point"""
    logger.info(f"Starting Message Service...")
    
    # Log important environment info
    logger.info(f"Kong Gateway URL: {KONG_GATEWAY_URL}")
    logger.info(f"Service Name: {SERVICE_NAME}")
    
    try:
        # Start the HTTP server for health checks and diagnostics
        http_runner = await start_http_server(port=HTTP_PORT)
        logger.info(f"HTTP server started on port {HTTP_PORT}")
        
        # Start WebSocket server
        # Note: The WebSocket server doesn't handle HTTP requests anymore,
        # but we keep the fallback health check just in case
        async with websockets.serve(
            websocket_handler, 
            "0.0.0.0", 
            5006,
            process_request=fallback_health_check
        ):
            logger.info("WebSocket server started on port 5006")
            update_status('websocket_server_status', 'running')
            await asyncio.Future()  # Run forever
    except Exception as e:
        logger.critical(f"Failed to start servers: {str(e)}", exc_info=True)
        update_status('error', f"Startup error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
