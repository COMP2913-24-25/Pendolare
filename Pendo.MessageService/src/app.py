import asyncio
import websockets
import logging
import json
import os
import sys
import traceback
import time
from datetime import datetime
from src.message_handler import MessageHandler
from src.db.MessageRepository import MessageRepository
from aiohttp import web
from aiohttp_cors import setup as cors_setup, ResourceOptions


"""
Code derived from websockets documentation & example code
Reference: https://websockets.readthedocs.io/en/stable/topics/index.html
"""

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "DEBUG"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Set websockets logger to DEBUG for detailed handshake information
websockets_logger = logging.getLogger('websockets')
websockets_logger.setLevel(logging.DEBUG)

WS_PORT = int(os.environ.get("WS_PORT", "9010"))
HTTP_PORT = int(os.environ.get("HTTP_PORT", "9011"))

# Initialize database repository
USE_DATABASE = os.environ.get("USE_DATABASE", "true").lower() == "true"
repository = None
if USE_DATABASE:
    try:
        repository = MessageRepository() 
        logger.info("Database repository initialized")
    except Exception as e:
        logger.error(f"Failed to initialize database repository: {str(e)}")
        logger.error(traceback.format_exc())

# Initialize message handler with repository
message_handler = MessageHandler(repository=repository)

async def health_check(request):
    """HTTP endpoint for health checks"""

    # Return healthy status with timestamp
    return web.json_response({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "message-service"
    })

async def root_handler(request):
    """Root HTTP endpoint"""
    # Extract host and protocol for WebSocket URL
    host = request.headers.get('Host', f'localhost:{HTTP_PORT}')
    ws_host = host.split(':')[0]
    ws_protocol = "wss" if request.url.scheme == "https" else "ws"
    
    # Return service information
    return web.json_response({
        "service": "Pendo Message Service", 
        "version": "1.0",
        "endpoints": {
            "health": "/health",
            "websocket": f"{ws_protocol}://{ws_host}:{WS_PORT}/ws"
        }
    })

async def user_conversations_handler(request):
    """
    HTTP endpoint to get user conversations.
    
    Expects a JSON body with:
        - UserId (str)
    """
    # Parse JSON body
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid JSON body"}, status=400)
    
    user_id = data.get("UserId")
    if not user_id:
        return web.json_response({"error": "UserId is not in the request body"}, status=400)
    
    try:
        # First check if repository exists in app context (for testing)
        repo = request.app.get('repository', repository)
        if repo is None:
            return web.json_response({"error": "Repository not available"}, status=500)
            
        # Fetch user conversations from repository and return as JSON
        conversations = repo.get_user_conversations(user_id)
        conv_list = []
        for conv in conversations:
            conv_list.append({
                "ConversationId": str(conv.ConversationId),
                "Type": conv.Type,
                "CreateDate": conv.CreateDate.isoformat(),
                "UpdateDate": conv.UpdateDate.isoformat(),
                "Name": conv.Name
            })
        return web.json_response({"conversations": conv_list})
    except Exception as e:
        logger.error(f"Error fetching user conversations: {str(e)}")
        return web.json_response({"error": str(e)}, status=500)

async def create_conversation_handler(request):
    """
    HTTP endpoint to create a conversation with participants.

    Expects a JSON body with:
      - UserId (str)
      - ConversationType (str)
      - name (str, optional)
      - participants (list of UUID strings)
    """
    # Parse JSON body
    try:
        data = await request.json()
    except Exception:
        return web.json_response({"error": "Invalid JSON body"}, status=400)
    
    # Validate required fields
    conversation_type = data.get("ConversationType")
    if not conversation_type:
        return web.json_response({"error": "ConversationType is required"}, status=400)
    
    participants = data.get("participants")
    if not participants or not isinstance(participants, list):
        return web.json_response({"error": "participants must be a list"}, status=400)
    
    name = data.get("name")
    
    # Create conversation with participants
    try:
        # First check if repository exists in app context (for testing)
        repo = request.app.get('repository', repository)
        if repo is None:
            return web.json_response({"error": "Repository not available"}, status=500)
            
        conversation = repo.create_conversation_with_participants(conversation_type, participants, name)
        response_data = {
            "ConversationId": str(conversation.ConversationId),
            "Type": conversation.Type,
            "CreateDate": conversation.CreateDate.isoformat(),
            "UpdateDate": conversation.UpdateDate.isoformat(),
            "Name": conversation.Name or f"Conv-{conversation.ConversationId}"
        }
        return web.json_response(response_data)
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        return web.json_response({"error": str(e)}, status=500)

async def websocket_handler(websocket):
    """Handle incoming WebSocket connections"""
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
            "message": f"Connected to Pendo Message Service via path: {path}",
            "timestamp": datetime.now().isoformat(),
            "client_info": {
                "id": client_id,
                "remote": str(remote),
                "path": path
            }
        }))
        
        last_heartbeat = time.time()
        heartbeat_interval = 15
        
        while True:
            current_time = time.time()
            if current_time - last_heartbeat > heartbeat_interval:
                # Send a heartbeat message to check for disconnect
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
                continue
            except websockets.exceptions.ConnectionClosed as e:
                logger.info(f"Connection closed for client {client_id}: code={e.code}, reason='{e.reason}'")
                break
    except Exception as e:
        logger.error(f"Unexpected error handling websocket for client {client_id}: {str(e)}")
        logger.error(traceback.format_exc())
    # Cleanup on exit
    finally:
        # Remove user from message handler
        for user_id, conn in list(message_handler.user_connections.items()):
            if conn == websocket:
                message_handler.remove_user(user_id)
                break
        logger.info(f"WebSocket connection ended: {client_id}")

async def setup_http_server():
    """
    Setup HTTP server with CORS support
    Derived from: https://github.com/aio-libs/aiohttp-cors
    """
    app = web.Application()
    
    cors = cors_setup(app, defaults={
        "*": ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"]
        )
    })
    
    # Register HTTP endpoints
    app.router.add_get('/', root_handler)
    app.router.add_get('/health', health_check)
    app.router.add_post('/user-conversations', user_conversations_handler)
    app.router.add_post('/create-conversation', create_conversation_handler)
    
    # Add CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)
    
    # Start HTTP server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', HTTP_PORT)
    await site.start()
    logger.info(f"HTTP server started on port {HTTP_PORT}")

    return runner

async def setup_ws_server():
    """Setup WebSocket server"""
    # Create WebSocket server
    server = await websockets.serve(
        websocket_handler,
        "0.0.0.0",
        WS_PORT,
        ping_interval=30,
        ping_timeout=120,
        close_timeout=60,
        max_size=10 * 1024 * 1024,
        max_queue=64,
        compression=None,
        logger=logger
    )
    logger.info(f"WebSocket server started on port {WS_PORT}")
    return server

async def main():
    """Main entry point for starting servers"""
    logger.info("Starting Message Service servers")
    
    try:
        # Start HTTP and WebSocket servers
        await setup_http_server()
        await setup_ws_server()
        
        # Keep running until cancelled
        await asyncio.Future()
    except Exception as e:
        logger.error(f"Error starting servers: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    asyncio.run(main())
