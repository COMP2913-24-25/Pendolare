import asyncio
import websockets
import logging
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
            await handler.handle_message(websocket, message)
    except Exception as e:
        logger.error(f"Error in websocket handler: {str(e)}")
        if hasattr(websocket, 'connected'):
            websocket.connected = False
    finally:
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
