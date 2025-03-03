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
import ssl
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

# Set websockets logger to DEBUG for detailed handshake information
websockets_logger = logging.getLogger('websockets')
websockets_logger.setLevel(logging.DEBUG)

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
    # Get hostname from request or use localhost
    host = request.headers.get('Host', f'localhost:{HTTP_PORT}')
    ws_host = host.split(':')[0]  # Remove port if present
    
    # Use the same protocol (http/https) for the WebSocket URL
    ws_protocol = "wss" if request.url.scheme == "https" else "ws"
    ws_port = WS_PORT
    
    return web.json_response({
        "service": "Pendo Message Service", 
        "version": "1.0",
        "endpoints": {
            "health": "/health",
            "websocket": f"{ws_protocol}://{ws_host}:{ws_port}/ws",
            "websocket_azure": f"{ws_protocol}://{host}/ws"
        }
    })

async def debug_handler(request):
    """Endpoint to help debug connection issues"""
    headers = dict(request.headers)
    
    # Clean sensitive info
    if 'Authorization' in headers:
        headers['Authorization'] = '[REDACTED]'
        
    client_info = {
        "remote": request.remote,
        "scheme": request.scheme,
        "host": request.host,
        "path": request.path,
        "query": dict(request.query),
        "headers": headers,
        "forwarded": headers.get('X-Forwarded-For', 'None'),
        "forwarded_proto": headers.get('X-Forwarded-Proto', 'None'),
        "server_hostname": os.environ.get('HOSTNAME', 'unknown')
    }
    
    return web.json_response({
        "debug_info": client_info,
        "timestamp": datetime.now().isoformat(),
        "ports": {
            "http": HTTP_PORT,
            "ws": WS_PORT
        }
    })

async def ws_info_handler(request):
    """WebSocket Info HTTP endpoint - provides info to help clients connect"""
    host = request.headers.get('Host', f'localhost:{HTTP_PORT}')
    ws_host = host.split(':')[0]  # Remove port if present
    x_forwarded_proto = request.headers.get('X-Forwarded-Proto', request.scheme)
    
    # Calculate the correct WebSocket URL
    ws_protocol = "wss" if x_forwarded_proto == "https" else "ws"
    
    # Check if port is specified in host header 
    if ':' in host:
        ws_url = f"{ws_protocol}://{host}/ws"
    else:
        # If running in Azure, don't include the port in the URL
        ws_url = f"{ws_protocol}://{host}/ws"
    
    return web.json_response({
        "websocket_url": ws_url,
        "service_info": {
            "name": "Pendo Message Service",
            "version": "1.0"
        },
        "client_info": {
            "ip": request.remote,
            "host": host,
            "protocol": x_forwarded_proto
        },
        "headers_to_include": {
            "Origin": host
        }
    })

# Origin handler for WebSockets
def origin_check(origin, host):
    """Check if the origin is allowed to connect"""
    logger.debug(f"Origin check: origin={origin}, host={host}")
    # Allow all origins for now
    return True

# Process headers for WebSocket connections
async def process_request(path, headers):
    """
    Process the HTTP request before the WebSocket handshake
    Args:
        path: The requested path
        headers: The HTTP headers
    """
    try:
        logger.debug(f"WebSocket handshake request: path={path}")
        logger.debug(f"Headers: {dict(headers.items())}")
        
        origin = headers.get('Origin', None)
        host = headers.get('Host', None)
        
        if origin and host:
            if not origin_check(origin, host):
                logger.warning(f"Rejected connection from origin: {origin}")
                return http.HTTPStatus.FORBIDDEN, [], b"Forbidden origin"
        
        # Accept the connection
        return None
    except Exception as e:
        logger.error(f"Error during WebSocket handshake: {str(e)}")
        return http.HTTPStatus.INTERNAL_SERVER_ERROR, [], b"Internal server error"

# WebSocket handler
async def websocket_handler(websocket):
    # Extract path and headers
    path = getattr(websocket, 'path', '/ws')
    client_id = id(websocket)
    remote = getattr(websocket, 'remote_address', 'unknown')
    request_headers = getattr(websocket, 'request_headers', {})
    
    logger.info(f"New WebSocket connection: ID={client_id}, Remote={remote}, Path={path}")
    
    try:
        # Log request headers for debugging
        if request_headers:
            logger.debug(f"Client {client_id} headers: {dict(request_headers.items())}")
        
        # Send a welcome message
        await websocket.send(json.dumps({
            "type": "welcome",
            "message": f"Connected to Message Service via path: {path}",
            "timestamp": datetime.now().isoformat(),
            "client_info": {
                "id": client_id,
                "remote": str(remote),
                "path": path
            }
        }))
        
        last_heartbeat = time.time()
        heartbeat_interval = 10  # seconds - reduced for faster response
        
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
    
    # Setup CORS - allow all origins
    cors = cors_setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"]
        )
    })
    
    # Add routes
    app.router.add_get('/health', health_check)
    app.router.add_get('/', root_handler)
    app.router.add_get('/debug', debug_handler)
    app.router.add_get('/ws-info', ws_info_handler)
    
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
    logger.info(f"Starting WebSocket server on port {WS_PORT} with Azure compatibility")
    
    # Create server with specific settings for Azure environment
    server = await websockets.serve(
        websocket_handler,
        "0.0.0.0",
        WS_PORT,
        # Increase timeouts for Azure environment
        ping_interval=30,
        ping_timeout=120,
        close_timeout=60,
        max_size=10 * 1024 * 1024,  # 10MB message size limit
        max_queue=64,  # Allow more messages in queue
        process_request=process_request,
        # Enable compression
        compression=None,
        # Accept all subprotocols
        subprotocols=['json'],
        # Set the logger for connection issues
        logger=logger,
        # Extra options that should help with Azure
        open_timeout=30,
        origin=None,  # Don't verify origin (handled in process_request)
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
