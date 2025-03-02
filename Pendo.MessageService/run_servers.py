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

# Print debugging information
logger.debug(f"Current directory: {os.getcwd()}")
logger.debug(f"Directory contents: {os.listdir('.')}")
logger.debug(f"Python path: {sys.path}")

# Add src directory to path
src_dir = os.path.join(os.getcwd(), 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)
    logger.debug(f"Added {src_dir} to Python path")
    logger.debug(f"Updated Python path: {sys.path}")

# Import the app module
try:
    sys.path.insert(0, 'src')
    from src.app import main as app_main
    logger.info("Successfully imported app module from src package")
except ImportError as e:
    logger.error(f"Failed to import from src.app: {e}")
    try:
        # Try direct import
        os.chdir('src')
        from app import main as app_main
        logger.info("Successfully imported app module directly")
    except ImportError as e2:
        logger.error(f"All import attempts failed. Last error: {e2}")
        sys.exit(1)

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
