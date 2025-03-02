import asyncio
import websockets
import logging
import json
import os
import sys
import traceback
import time
from datetime import datetime

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "DEBUG"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

WS_PORT = int(os.environ.get("WS_PORT", "5006"))

# Simplified process_request function without Kong-specific checks
async def process_request(path, request_headers):
    # Ensure the request is a websocket upgrade request.
    upgrade = request_headers.get("Upgrade", "").lower()
    if upgrade != "websocket":
        logger.warning("Non-websocket request received. Rejecting.")
        return 426, [("Content-Type", "text/plain")], b"Upgrade Required"
    return None  # Proceed with handshake

async def websocket_handler(websocket, path):
    client_id = id(websocket)
    logger.info(f"New WebSocket connection: ID={client_id}, Path={path}")
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
                await websocket.send(json.dumps({
                    "type": "heartbeat",
                    "timestamp": datetime.now().isoformat()
                }))
                last_heartbeat = current_time
            try:
                msg = await asyncio.wait_for(websocket.recv(), timeout=heartbeat_interval)
                logger.info(f"Received from client {client_id}: {msg}")
                await websocket.send(f"ECHO: {msg}")
            except asyncio.TimeoutError:
                continue
    except websockets.exceptions.ConnectionClosed as e:
        logger.info(f"Connection closed for client {client_id}: code={e.code}, reason='{e.reason}'")
    except Exception as e:
        logger.error(f"Error handling websocket for client {client_id}: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        logger.info(f"WebSocket connection ended: {client_id}")

async def main():
    logger.info(f"Starting without SSL (WS)")
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
