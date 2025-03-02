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

# Add parent directory to sys.path if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the app module
try:
    from src.app import main as app_main
    logger.info("Successfully imported app module from src package")
except ImportError:
    # Try direct import as fallback
    sys.path.insert(0, current_dir)
    from app import main as app_main
    logger.info("Successfully imported app module directly")

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
