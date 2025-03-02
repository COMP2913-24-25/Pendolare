import asyncio
import websockets
import logging
import json
import os
import sys
import traceback
import time
import http
from aiohttp import web
from datetime import datetime
from src.message_handler import MessageHandler

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "DEBUG"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Configuration
WS_PORT = int(os.environ.get("WS_PORT", "5006"))
HTTP_PORT = int(os.environ.get("HTTP_PORT", "5007"))
message_handler = MessageHandler()

# HTTP Server for health checks and basic info
async def health_handler(request):
    """Handle health check requests"""
    return web.json_response({
        "status": "healthy",
        "service": "message-service",
        "timestamp": datetime.now().isoformat()
    })

async def ws_info_handler(request):
    """Provide info about WebSocket endpoints"""
    return web.json_response({
        "status": "info",
        "message": "This is a WebSocket server. Connect to the WebSocket endpoint for real-time communication.",
        "websocket_endpoint": f"ws://localhost:{WS_PORT}/ws",
        "timestamp": datetime.now().isoformat()
    })

async def setup_http_server():
    """Set up a simple HTTP server for health checks and info"""
    app = web.Application()
    app.router.add_get('/health', health_handler)
    app.router.add_get('/', health_handler)
    app.router.add_get('/ws-info', ws_info_handler)
    
    # Add middleware for logging
    @web.middleware
    async def log_middleware(request, handler):
        logger.info(f"HTTP Request: {request.method} {request.path} from {request.remote}")
        try:
            response = await handler(request)
            logger.info(f"HTTP Response: {response.status} for {request.path}")
            return response
        except Exception as e:
            logger.error(f"Error handling HTTP request: {str(e)}")
            return web.json_response(
                {"error": "Internal server error"},
                status=500
            )
    
    app.middlewares.append(log_middleware)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', HTTP_PORT)
    await site.start()
    logger.info(f"HTTP server started on port {HTTP_PORT}")
    return runner

# WebSocket server specific handlers

async def process_ws_request(path, request_headers):
    """Process WebSocket handshake requests"""
    try:
        logger.debug(f"WebSocket handshake request for path: {path}")
        
        # Convert headers to a dictionary for logging
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
        logger.debug(f"WebSocket handshake headers: {log_headers}")
        
        # Check for proper WebSocket upgrade
        connection = headers_dict.get("Connection", "").lower()
        upgrade = headers_dict.get("Upgrade", "").lower()
        
        if not connection or "upgrade" not in connection or upgrade != "websocket":
            logger.warning(f"Invalid WebSocket upgrade: Connection={connection}, Upgrade={upgrade}")
            return http.HTTPStatus.BAD_REQUEST, [
                ("Content-Type", "text/plain"),
            ], b"WebSocket connections only"
        
        # Valid WebSocket upgrade, proceed with handshake
        logger.info(f"Valid WebSocket handshake for path: {path}")
        return None
        
    except Exception as e:
        logger.error(f"Error in WebSocket handshake: {str(e)}")
        logger.error(traceback.format_exc())
        return http.HTTPStatus.INTERNAL_SERVER_ERROR, [
            ("Content-Type", "text/plain")
        ], b"Internal Server Error"

async def websocket_handler(websocket, path):
    """Handle WebSocket connections"""
    client_id = id(websocket)
    remote = websocket.remote_address if hasattr(websocket, "remote_address") else "unknown"
    logger.info(f"New WebSocket connection: ID={client_id}, Remote={remote}, Path={path}")
    
    try:
        # Send a welcome message
        await websocket.send(json.dumps({
            "type": "welcome",
            "message": f"Connected to Message Service",
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

async def setup_ws_server():
    """Set up the WebSocket server"""
    logger.info(f"Starting WebSocket server on port {WS_PORT}")
    
    # Only accept WebSocket connections to the /ws path
    async with websockets.serve(
        websocket_handler,
        "0.0.0.0",
        WS_PORT,
        process_request=process_ws_request,
        ping_interval=20,
        ping_timeout=60,
        close_timeout=60
    ):
        logger.info(f"WebSocket server started on port {WS_PORT}")
        # Keep the server running
        await asyncio.Future()

async def main():
    """Start both HTTP and WebSocket servers"""
    logger.info("Starting Message Service...")
    
    # Start both servers
    http_runner = await setup_http_server()
    ws_server = asyncio.create_task(setup_ws_server())
    
    try:
        # Keep running until interrupted
        await asyncio.Future()
    finally:
        # Clean up on exit
        await http_runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
