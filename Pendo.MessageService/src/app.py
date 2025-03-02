import asyncio
import websockets
import logging
import json
import os
import sys
import traceback
import time
import http
from datetime import datetime
from src.message_handler import MessageHandler

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "DEBUG"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

WS_PORT = int(os.environ.get("WS_PORT", "5006"))
message_handler = MessageHandler()

# Simple HTTP handler for health checks
async def http_handler(request_path):
    if request_path == "/health" or request_path == "/":
        return http.HTTPStatus.OK, [("Content-Type", "application/json")], json.dumps({
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }).encode()
    return http.HTTPStatus.NOT_FOUND, [("Content-Type", "text/plain")], b"Not Found"

async def process_request(path, request_headers):
    # Log all headers for debugging
    logger.debug(f"Received headers for path {path}: {dict(request_headers)}")
    
    # Check if this is a health check request
    if not path.startswith("/ws"):
        return await http_handler(path)
        
    # Handle WebSocket upgrade
    connection = request_headers.get("Connection", "").lower()
    upgrade = request_headers.get("Upgrade", "").lower()
    
    if "upgrade" in connection and upgrade == "websocket":
        logger.info(f"Valid WebSocket upgrade request received for path: {path}")
        # Check for proxy headers
        forwarded_for = request_headers.get("X-Forwarded-For")
        forwarded_proto = request_headers.get("X-Forwarded-Proto")
        if forwarded_for or forwarded_proto:
            logger.info(f"Request proxied from {forwarded_for}, protocol {forwarded_proto}")
        return None  # Proceed with WebSocket handshake
    
    logger.warning(f"Invalid WebSocket request. Connection: {connection}, Upgrade: {upgrade}")
    return http.HTTPStatus.UPGRADE_REQUIRED, [
        ("Content-Type", "text/plain"),
        ("Connection", "Upgrade"),
        ("Upgrade", "websocket")
    ], b"Upgrade to WebSocket required"

async def websocket_handler(websocket, path):
    client_id = id(websocket)
    remote = websocket.remote_address if hasattr(websocket, "remote_address") else "unknown"
    logger.info(f"New WebSocket connection: ID={client_id}, Remote={remote}, Path={path}")
    
    try:
        # Send a welcome message
        await websocket.send(json.dumps({
            "type": "welcome",
            "message": f"Connected to Message Service via path: {path}",
            "timestamp": datetime.now().isoformat()
        }))
        
        last_heartbeat = time.time()
        heartbeat_interval = 15  # seconds
        
        while True:
            current_time = time.time()
            if current_time - last_heartbeat > heartbeat_interval:
                try:
                    await websocket.send(json.dumps({
                        "type": "heartbeat",
                        "timestamp": datetime.now().isoformat()
                    }))
                    last_heartbeat = current_time
                except websockets.exceptions.ConnectionClosed:
                    logger.info(f"Connection closed during heartbeat for client {client_id}")
                    break
            
            try:
                # Wait for message with timeout to allow heartbeat checks
                msg = await asyncio.wait_for(websocket.recv(), timeout=heartbeat_interval)
                logger.debug(f"Received from client {client_id}: {msg[:200]}...")
                
                # Process the message using message handler
                try:
                    await message_handler.handle_message(websocket, msg)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON received from client {client_id}")
                    await websocket.send(json.dumps({
                        "type": "error", 
                        "message": "Invalid JSON format"
                    }))
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "message": "Server error processing message"
                    }))
                    
            except asyncio.TimeoutError:
                # This is expected - just for heartbeat check
                continue
            except websockets.exceptions.ConnectionClosed as e:
                logger.info(f"Connection closed for client {client_id}: code={e.code}, reason='{e.reason}'")
                break
    except Exception as e:
        logger.error(f"Unexpected error handling websocket for client {client_id}: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        # Clean up user connection if registered
        for user_id, conn in list(message_handler.user_connections.items()):
            if conn == websocket:
                message_handler.remove_user(user_id)
                break
        logger.info(f"WebSocket connection ended: {client_id}")

async def main():
    logger.info(f"Starting WebSocket server on port {WS_PORT}")
    
    async with websockets.serve(
        websocket_handler,
        "0.0.0.0",
        WS_PORT,
        process_request=process_request,
        ping_interval=20,
        ping_timeout=60,
        close_timeout=60
    ):
        logger.info(f"WebSocket server started on port {WS_PORT}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
