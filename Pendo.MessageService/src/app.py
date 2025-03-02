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

# Simple HTTP handler for health checks and other HTTP requests
async def http_handler(request_path):
    logger.info(f"HTTP request received: {request_path}")
    
    if request_path == "/health" or request_path == "/":
        return http.HTTPStatus.OK, [("Content-Type", "application/json")], json.dumps({
            "status": "healthy",
            "timestamp": datetime.now().isoformat()
        }).encode()
    
    # Handle WebSocket endpoint information for debugging
    if request_path == "/ws-info":
        return http.HTTPStatus.OK, [("Content-Type", "application/json")], json.dumps({
            "status": "info",
            "message": "This is a WebSocket server. Connect to /ws endpoint for WebSocket communication.",
            "websocket_endpoint": "/ws",
            "timestamp": datetime.now().isoformat()
        }).encode()
    
    # For any other path, return 404
    return http.HTTPStatus.NOT_FOUND, [("Content-Type", "text/plain")], b"Not Found - Use /ws for WebSocket connections or /health for health checks"

async def process_request(path, request_headers):
    try:
        logger.debug(f"Processing request for path: {path}")
        
        # Convert headers to a dictionary for logging, handling various header formats
        headers_dict = {}
        try:
            if hasattr(request_headers, 'raw_items'):
                headers_dict = dict(request_headers.raw_items())
            elif hasattr(request_headers, 'items'):
                headers_dict = dict(request_headers.items())
            else:
                headers_dict = dict(request_headers)
        except Exception as e:
            logger.warning(f"Could not convert headers to dictionary: {str(e)}")
        
        # Log important headers for debugging
        important_headers = ['Connection', 'Upgrade', 'Sec-WebSocket-Key', 
                            'User-Agent', 'Host', 'X-Forwarded-For']
        log_headers = {k: headers_dict.get(k) for k in important_headers if k in headers_dict}
        logger.debug(f"Request headers for {path}: {log_headers}")
        
        # Only paths starting with /ws should be treated as WebSocket connections
        if path.startswith("/ws"):
            # Check for WebSocket upgrade
            connection = headers_dict.get("Connection", "").lower()
            upgrade = headers_dict.get("Upgrade", "").lower()
            
            if connection and "upgrade" in connection and upgrade == "websocket":
                logger.info(f"Valid WebSocket upgrade request for {path}")
                return None  # Proceed with WebSocket handshake
            else:
                logger.warning(f"Invalid WebSocket request to {path}. Connection: {connection}, Upgrade: {upgrade}")
                return http.HTTPStatus.UPGRADE_REQUIRED, [
                    ("Content-Type", "text/plain"),
                    ("Connection", "Upgrade"),
                    ("Upgrade", "websocket")
                ], b"Upgrade to WebSocket required"
        
        # For all other paths, handle as HTTP
        return await http_handler(path)
        
    except Exception as e:
        logger.error(f"Error in process_request: {str(e)}")
        logger.error(traceback.format_exc())
        return http.HTTPStatus.INTERNAL_SERVER_ERROR, [("Content-Type", "text/plain")], b"Internal Server Error"

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
