import asyncio
import websockets
from websockets.http import Headers
import logging
import json
import os
import sys
import traceback
import time
import http
from datetime import datetime
from src.message_handler import MessageHandler
from aiohttp import web
from aiohttp.web import middleware
from aiohttp_cors import setup as cors_setup, ResourceOptions

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "DEBUG"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

WS_PORT = int(os.environ.get("WS_PORT", "5006"))
HTTP_PORT = int(os.environ.get("HTTP_PORT", "5007"))
message_handler = MessageHandler()

# HTTP routes for health checks
async def health_check(request):
    """HTTP endpoint for health checks"""
    return web.json_response({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "message-service"
    })

async def root_handler(request):
    """Root HTTP endpoint"""
    return web.json_response({
        "service": "Pendo Message Service", 
        "version": "1.0",
        "endpoints": {
            "health": "/health",
            "websocket": f"ws://localhost:{WS_PORT}/ws"
        }
    })

# Origin handler for WebSockets
def origin_check(origin, host):
    """Check if the origin is allowed to connect"""
    # Allow all origins in development, but you can implement restrictions here
    logger.debug(f"Origin check: origin={origin}, host={host}")
    return True

# WebSocket handler
async def websocket_handler(websocket):
    # Extract path from websocket object
    path = getattr(websocket, 'path', '/ws')
    client_id = id(websocket)
    remote = getattr(websocket, 'remote_address', 'unknown')
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

# Process headers for WebSocket connections
async def process_request(path, headers):
    logger.debug(f"WS connection request: path={path}, headers={headers}")
    
    origin = headers.get('Origin', None)
    host = headers.get('Host', None)
    
    if origin and host:
        if not origin_check(origin, host):
            logger.warning(f"Rejected connection from origin: {origin}")
            return http.HTTPStatus.FORBIDDEN, [], b"Forbidden origin"
    
    # Return None to proceed with the WebSocket handshake
    return None

# Setup HTTP server with CORS support
async def setup_http_server():
    @middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)
        except web.HTTPException as ex:
            return web.json_response({"error": str(ex)}, status=ex.status)
        except Exception as ex:
            logger.exception("Unexpected error")
            return web.json_response({"error": "Internal server error"}, status=500)

    app = web.Application(middlewares=[error_middleware])
    
    # Setup CORS
    cors = cors_setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "OPTIONS"]
        )
    })
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_get('/', root_handler)
    
    # Configure CORS on all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', HTTP_PORT)
    await site.start()
    logger.info(f"HTTP server started on port {HTTP_PORT}")
    return runner

# Setup WebSocket server
async def setup_ws_server():
    logger.info(f"Starting WebSocket server on port {WS_PORT} with improved handshake handling")
    
    server = await websockets.serve(
        websocket_handler,
        "0.0.0.0",
        WS_PORT,
        ping_interval=20,
        ping_timeout=60,
        close_timeout=60,
        process_request=process_request,
        # Accept subprotocols if presented by client
        subprotocols=["json"],
        # Log connection errors
        logger=logger
    )
    logger.info(f"WebSocket server started on port {WS_PORT}")
    return server

async def main():
    logger.info("Starting Message Service servers")
    
    try:
        # Start both HTTP and WebSocket servers
        http_runner = await setup_http_server()
        ws_server = await setup_ws_server()
        
        # Keep the servers running
        await asyncio.Future()
    except Exception as e:
        logger.error(f"Error starting servers: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    asyncio.run(main())
