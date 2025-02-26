import asyncio
import websockets
import logging
import json
import os
import sys
import pathlib
import traceback
from src.message_handler import MessageHandler
import http.server
import socketserver
import threading
import socket
import time
import random
from datetime import datetime

logging.basicConfig(
    level=os.environ.get('LOG_LEVEL', 'DEBUG'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create a global variable for the HTML content and HTTP port
TEST_CLIENT_HTML = None
HTTP_SERVER_PORT = None

# Get environment variables
WS_PORT = int(os.environ.get("WS_PORT", "5006"))
HTTP_PORT = int(os.environ.get("HTTP_PORT", "5007"))  # Make HTTP port configurable
IS_BEHIND_TLS_PROXY = os.environ.get("BEHIND_TLS_PROXY", "false").lower() == "true"

try:
    handler = MessageHandler()
except Exception as e:
    logger.error(f"Failed to initialise MessageHandler: {str(e)}")
    logger.error(traceback.format_exc())
    sys.exit(1)

# Get Kong Gateway URL from environment, if available
KONG_GATEWAY_URL = os.environ.get("KONG_GATEWAY_URL", None)
SERVICE_NAME = os.environ.get("SERVICE_NAME", "message-service")

# Log startup configuration
logger.info(f"Starting with environment: KONG_GATEWAY_URL={KONG_GATEWAY_URL}, SERVICE_NAME={SERVICE_NAME}")

# HTTP Server for serving static files derived using Generative AI
class TestClientHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global TEST_CLIENT_HTML
        
        if self.path == "/" or self.path == "/test-client" or self.path == "/test-client.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            
            if TEST_CLIENT_HTML:
                content = TEST_CLIENT_HTML
            else:
                # Try to load the test client HTML from the filesystem
                try:
                    file_path = pathlib.Path(__file__).parent / "test-client.html"
                    if not file_path.exists():
                        file_path = pathlib.Path("/app/src/test-client.html")
                    
                    with open(file_path, "rb") as f:
                        content = f.read()
                    TEST_CLIENT_HTML = content
                except Exception as e:
                    content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head><title>Error</title></head>
                    <body>
                        <h1>Error Loading Test Client</h1>
                        <p>{str(e)}</p>
                    </body>
                    </html>
                    """.encode('utf-8')
            
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == "/kong-test" or self.path == "/kong-test-client" or self.path == "/kong-test-client.html":
            # Serve the Kong-specific test client
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            
            try:
                file_path = pathlib.Path(__file__).parent / "kong-test-client.html"
                if not file_path.exists():
                    file_path = pathlib.Path("/app/src/kong-test-client.html")
                
                with open(file_path, "rb") as f:
                    content = f.read()
                
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                content = f"""
                <!DOCTYPE html>
                <html>
                <head><title>Error</title></head>
                <body>
                    <h1>Error Loading Kong Test Client</h1>
                    <p>{str(e)}</p>
                </body>
                </html>
                """.encode('utf-8')
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            content = b"OK"
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            super().do_GET()

    def log_message(self, format, *args):
        # Redirect log messages to our logger
        logger.debug(f"HTTP: {format % args}")

# Enhanced TCP Server class that allows address reuse
class ReuseAddressServer(socketserver.TCPServer):
    allow_reuse_address = True

# Start HTTP server in a separate thread with port fallback
def start_http_server():
    global HTTP_SERVER_PORT
    
    # Try to bind to the specified port or use fallbacks
    original_port = HTTP_PORT
    port = original_port
    max_attempts = 5
    
    for attempt in range(max_attempts):
        try:
            logger.info(f"Attempting to start HTTP server on port {port} (attempt {attempt+1}/{max_attempts})")
            
            # Print detailed network information for debugging
            logger.info("Network interfaces:")
            try:
                for iface, addrs in socket.getaddrinfo('', port, family=socket.AF_INET, type=socket.SOCK_STREAM):
                    logger.info(f"  {iface}: {addrs}")
            except Exception as e:
                logger.error(f"Error getting address info: {str(e)}")
            
            # Use the enhanced server class
            httpd = ReuseAddressServer(("0.0.0.0", port), TestClientHTTPHandler)
            HTTP_SERVER_PORT = port
            logger.info(f"HTTP server successfully started on port {port}")
            httpd.serve_forever()
            break
        except OSError as e:
            logger.warning(f"Port {port} is in use or cannot be bound: {str(e)}")
            
            if attempt < max_attempts - 1:
                # Try a different port next time
                port = original_port + random.randint(1, 100)
                logger.info(f"Will try alternate port {port}")
                time.sleep(1)  # Small delay before retry
            else:
                logger.error("Could not bind to any port after maximum attempts")
                return

async def health_handler(path, headers):
    """Handle health check requests for WebSocket server"""
    logger.info(f"Received request for path: {path}")
    
    # DEBUG: Log all headers to help diagnose issues
    logger.debug(f"Request headers for {path}:")
    for name, value in headers.items():
        logger.debug(f"  {name}: {value}")
    
    # Special handling for Azure Container Apps - may have different headers
    forwarded_proto = headers.get("X-Forwarded-Proto", "").lower()
    original_proto = headers.get("X-Original-Proto", "").lower()
    
    # If we detect we're behind a TLS proxy, log it
    if IS_BEHIND_TLS_PROXY or "https" in forwarded_proto or "wss" in original_proto:
        logger.info("Detected TLS termination at proxy")
    
    # Check for WebSocket handshake headers regardless of path
    connection_header = headers.get("Connection", "").lower()
    upgrade_header = headers.get("Upgrade", "").lower()
    
    # If it's a WebSocket upgrade request, log it and pass through
    if "upgrade" in connection_header and "websocket" in upgrade_header:
        logger.info(f"WebSocket handshake detected for path: {path}")
        return None  # Let the WebSocket handler take it
    
    # Handle health check path
    if path == "/health" or path == "/message/health":
        return 200, {"Content-Type": "text/plain"}, b"OK"
    
    # For unknown paths, log and redirect to HTTP server or return 404
    logger.warning(f"Unknown path requested: {path}")
    port = HTTP_SERVER_PORT if HTTP_SERVER_PORT else HTTP_PORT
    return 307, {"Location": f"http://localhost:{port}/test-client"}, b"Redirecting to test client"

async def websocket_handler(websocket, path):
    client_id = id(websocket)
    try:
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
    except Exception:
        client_info = "unknown"
    
    logger.info(f"New WebSocket connection: ID={client_id}, Path={path}, Client={client_info}")
    
    # DEBUG: Log all request headers
    try:
        logger.debug(f"WebSocket request headers:")
        for name, value in websocket.request_headers.items():
            logger.debug(f"  {name}: {value}")
    except Exception as e:
        logger.error(f"Could not log request headers: {e}")
    
    try:
        # Send welcome message with path information
        await websocket.send(json.dumps({
            "type": "welcome",
            "message": f"Connected to Message Service via path: {path}",
            "timestamp": datetime.now().isoformat()
        }))
        
        # Echo handler
        async for message in websocket:
            logger.info(f"Received from client {client_id}: {message}")
            
            # Try parsing as JSON first
            try:
                msg_data = json.loads(message)
                if isinstance(msg_data, dict) and msg_data.get("type") == "ping":
                    await websocket.send(json.dumps({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }))
                    continue
            except json.JSONDecodeError:
                # Not JSON, treat as plain text
                pass
            
            # Echo the message back
            response = f"ECHO: {message}"
            await websocket.send(response)
            logger.info(f"Sent to client {client_id}: {response}")
            
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"WebSocket connection closed for client {client_id}: code={e.code}, reason='{e.reason}'")
    except Exception as e:
        logger.error(f"Error handling WebSocket for client {client_id}: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        logger.info(f"WebSocket connection ended: {client_id}")

async def main():
    # Log startup information
    logger.info(f"Starting Message Service...")
    
    # Start HTTP server for static content in a separate thread
    http_server_thread = threading.Thread(target=start_http_server, daemon=True)
    http_server_thread.start()
    
    # Small delay to let the HTTP server start and discover its port
    await asyncio.sleep(1)
    
    # Start WebSocket server
    async with websockets.serve(
        websocket_handler, 
        "0.0.0.0", 
        WS_PORT,
        process_request=health_handler,
        ping_interval=20,       # Send ping every 20 seconds
        ping_timeout=20,        # Wait 20 seconds for pong
        close_timeout=20,       # Wait 20 seconds for close to complete
        max_size=10_485_760,    # 10MB max message size
        max_queue=32            # Queue up to 32 messages
    ):
        http_port = HTTP_SERVER_PORT if HTTP_SERVER_PORT else HTTP_PORT
        logger.info(f"WebSocket server started on port {WS_PORT}")
        logger.info(f"Access the test client at: http://localhost:{http_port}/test-client")
        logger.info(f"WebSocket endpoints: ws://localhost:{WS_PORT}/ws or via Kong at ws://localhost:8000/message/ws")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
