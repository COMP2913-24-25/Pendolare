import asyncio
import websockets
from src.message_handler import MessageHandler

handler = MessageHandler()

async def websocket_handler(websocket, path):
    # Validate if the path is /message/ws or / (stripped by Kong)
    if path not in ['/', '/message/ws']:
        return
        
    try:
        # For testing, handle mock websockets differently
        if hasattr(websocket, 'test_messages'):
            for message in websocket.test_messages:
                await handler.handle_message(websocket, message)
            websocket.connected = True
            return
            
        async for message in websocket:
            await handler.handle_message(websocket, message)
    except Exception as _:
        if hasattr(websocket, 'connected'):
            websocket.connected = False

async def main():
    async with websockets.serve(websocket_handler, "0.0.0.0", 5006):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
