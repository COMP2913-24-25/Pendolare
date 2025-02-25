import asyncio
import websockets
import logging
import json
from src.message_handler import MessageHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = MessageHandler()

async def websocket_handler(websocket, path):
    logger.info(f"New connection attempt. Path: {path}")
    
    # Validate if the path is /message/ws or / (stripped by Kong)
    if path not in ['/', '/message/ws']:
        logger.warning(f"Invalid path: {path}")
        return
        
    user_id = None
    
    try:
        logger.info("Connection established")
        # For testing, handle mock websockets differently
        if hasattr(websocket, 'test_messages'):
            for message in websocket.test_messages:
                await handler.handle_message(websocket, message)
            websocket.connected = True
            return
            
        async for message in websocket:
            logger.info(f"Received message: {message}")
            
            # Check if this is a registration message
            try:
                data = json.loads(message)
                if 'register' in data and data['register']:
                    if 'user_id' in data:
                        user_id = data['user_id']
                        logger.info(f"User {user_id} registered")
                        handler.register_user(user_id, websocket)
            except json.JSONDecodeError:
                logger.error("Invalid JSON message received")
                continue
                
            await handler.handle_message(websocket, message)
    except Exception as e:
        logger.error(f"Error in websocket handler: {str(e)}")
        if hasattr(websocket, 'connected'):
            websocket.connected = False
    finally:
        if user_id:
            handler.remove_user(user_id)
            logger.info(f"User {user_id} disconnected")
        logger.info("Connection closed")

async def main():
    # Start WebSocket server
    async with websockets.serve(
        websocket_handler, 
        "0.0.0.0", 
        5006,
        process_request=lambda path, headers: None
    ):
        logger.info("WebSocket server started on port 5006")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
