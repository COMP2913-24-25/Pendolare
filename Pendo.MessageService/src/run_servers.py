import asyncio
import logging
import sys
import os

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Add current directory to path to ensure app can be imported
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Import the app module directly
try:
    from app import main as app_main
    logger.info("Successfully imported app module")
except ImportError as e:
    logger.error(f"Failed to import app module: {e}")
    raise

async def main():    
    logger.info("Starting WebSocket server from run_servers.py")
    # Start WebSocket server
    await app_main()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Servers stopped by user")
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True)
