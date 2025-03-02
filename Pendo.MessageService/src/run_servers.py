import asyncio
import logging
import sys
import signal
from src import app

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Handle graceful shutdown
async def shutdown(signal, loop):
    """Gracefully shutdown the servers"""
    logger.info(f"Received exit signal {signal.name}...")
    logger.info("Shutting down servers...")
    
    # Cancel all running tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    
    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()

def register_signals(loop):
    """Register signal handlers for graceful shutdown"""
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(
            sig, lambda s=sig: asyncio.create_task(shutdown(s, loop))
        )

async def main():
    """Main entry point with proper signal handling"""
    loop = asyncio.get_event_loop()
    register_signals(loop)
    logger.info("Starting servers with signal handling...")
    
    try:
        await app.main()
    except asyncio.CancelledError:
        logger.info("Main task was cancelled")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    try:
        asyncio.run(main())
        logger.info("Servers stopped cleanly")
    except KeyboardInterrupt:
        logger.info("Servers stopped by user")
