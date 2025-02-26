"""
> HTTP Server for Static Test Interface derived from Generative AI
"""

import http.server
import socketserver
import pathlib
import threading
import logging

logger = logging.getLogger(__name__)

class TestClientHTTPHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logger.info(f"HTTP Request: {self.path}")
        if self.path in ["/", "/test-client", "/test-client.html"]:
            self.serve_test_client()
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            content = b"OK"
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_error(404, "Not Found")
    
    def serve_test_client(self):
        try:
            # Look for test-client.html in one of the expected locations
            file_paths = [
                pathlib.Path(__file__).parent / "test-client.html",
                pathlib.Path("/app/src/test-client.html")
            ]
            html_content = None
            for path in file_paths:
                logger.info(f"Looking for test client at: {path}")
                if path.exists():
                    with open(path, "rb") as f:
                        html_content = f.read()
                    break
            if html_content:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.send_header("Content-Length", str(len(html_content)))
                self.end_headers()
                self.wfile.write(html_content)
            else:
                self.send_error(404, "Test client HTML file not found")
        except Exception as e:
            logger.error(f"Error serving test client: {e}")
            self.send_error(500, str(e))

class ReuseAddressServer(socketserver.TCPServer):
    allow_reuse_address = True  # Allows quick restart

def start_http_server(port=8080):
    try:
        httpd = ReuseAddressServer(("", port), TestClientHTTPHandler)
        logger.info(f"HTTP server successfully started on port {port}")
        httpd.serve_forever()
    except Exception as e:
        logger.error(f"Failed to start HTTP server on port {port}: {e}")

def run_server_in_thread(port=8080):
    try:
        httpd = ReuseAddressServer(("", port), TestClientHTTPHandler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()
        logger.info(f"HTTP server running on port {port} in background thread")
        return httpd, thread
    except Exception as e:
        logger.error(f"Failed to run HTTP server in thread on port {port}: {e}")
        return None, None
