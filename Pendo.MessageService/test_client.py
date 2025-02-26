"""
WebSocket test client for Message Service
Run this locally to test connections to your deployed service
"""
import asyncio
import json
import websockets
import logging
import argparse
from datetime import datetime
import sys
import ssl

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ws-client")

class WebSocketClient:
    def __init__(self, uri, user_id=None, verify_ssl=True):
        self.uri = uri
        self.user_id = user_id or f"test-client-{datetime.now().timestamp()}"
        self.verify_ssl = verify_ssl
        self.connected = False
    
    async def connect(self):
        """Connect to the WebSocket server"""
        logger.info(f"Connecting to {self.uri} as {self.user_id}")
        
        # SSL context
        ssl_context = None
        if not self.verify_ssl and self.uri.startswith('wss://'):
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            logger.warning("SSL verification disabled!")
        
        try:
            # Connect to the WebSocket server
            async with websockets.connect(
                self.uri, 
                ssl=ssl_context
            ) as self.websocket:
                self.connected = True
                logger.info("Connected successfully!")
                
                # Register with the server
                register_msg = {
                    "register": True,
                    "user_id": self.user_id
                }
                await self.websocket.send(json.dumps(register_msg))
                logger.info(f"Sent registration message: {register_msg}")
                
                # Wait for welcome message
                response = await asyncio.wait_for(self.websocket.recv(), timeout=5)
                logger.info(f"Received: {response}")
                
                # Start the message loop
                await self.message_loop()
                
        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f"Connection closed: {e.code} {e.reason}")
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
        finally:
            self.connected = False
    
    async def message_loop(self):
        """Send test messages and receive responses"""
        count = 1
        try:
            while True:
                # Send a test message
                message = {
                    "type": "test_message",
                    "content": f"Test message {count}",
                    "timestamp": datetime.now().isoformat()
                }
                await self.websocket.send(json.dumps(message))
                logger.info(f"Sent: {message}")
                count += 1
                
                # Wait for response
                response = await asyncio.wait_for(self.websocket.recv(), timeout=5)
                logger.info(f"Received: {response}")
                
                # Wait 5 seconds before sending next message
                await asyncio.sleep(5)
        except asyncio.TimeoutError:
            logger.error("Timed out waiting for response")
        except KeyboardInterrupt:
            logger.info("User interrupted. Closing connection.")
        except Exception as e:
            logger.error(f"Error in message loop: {str(e)}")

async def check_http_endpoint(url):
    """Check if the HTTP diagnostics endpoint is accessible"""
    import aiohttp
    
    try:
        logger.info(f"Testing HTTP endpoint: {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                logger.info(f"HTTP Status: {response.status}")
                if response.status == 200:
                    data = await response.text()
                    logger.info(f"Response: {data[:100]}...")  # First 100 chars
                return response.status == 200
    except Exception as e:
        logger.error(f"HTTP request failed: {str(e)}")
        return False

async def main():
    parser = argparse.ArgumentParser(description='WebSocket Client for Message Service')
    parser.add_argument('--host', type=str, help='WebSocket server host (without protocol)')
    parser.add_argument('--path', type=str, default='/ws', help='WebSocket endpoint path')
    parser.add_argument('--ssl', action='store_true', help='Use SSL (wss://)')
    parser.add_argument('--no-verify', action='store_true', help='Disable SSL verification')
    parser.add_argument('--user-id', type=str, help='User ID for registration')
    parser.add_argument('--http-check', action='store_true', help='Check HTTP diagnostics first')
    
    args = parser.parse_args()
    
    # Get host from arguments or prompt
    host = args.host
    if not host:
        host = input("Enter WebSocket server host (without protocol): ")
    
    # Construct URI
    protocol = "wss://" if args.ssl else "ws://"
    uri = f"{protocol}{host}{args.path}"
    
    # Check HTTP endpoint first if requested
    if args.http_check:
        http_protocol = "https" if args.ssl else "http"
        health_url = f"{http_protocol}://{host}/health"
        diag_url = f"{http_protocol}://{host}/diagnostics"
        
        health_ok = await check_http_endpoint(health_url)
        diag_ok = await check_http_endpoint(diag_url)
        
        if not health_ok and not diag_ok:
            logger.error("Server is not responding to HTTP requests")
            if input("Continue anyway? (y/n): ").lower() != 'y':
                return
    
    # Create and start client
    client = WebSocketClient(uri, args.user_id, not args.no_verify)
    await client.connect()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Program terminated by user")
        sys.exit(0)
