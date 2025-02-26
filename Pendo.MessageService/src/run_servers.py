import asyncio
import logging
import sys
from src import app, http_server

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

async def main():
    # Start HTTP server for test client in a separate thread
    httpd, thread = http_server.run_server_in_thread(port=5007)
    if not httpd:
        logger.error("Failed to start HTTP server, exiting")
        return
    
    logger.info("HTTP server is running in a background thread")
    
    # Start WebSocket server in the main thread
    await app.main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Servers stopped by user")
