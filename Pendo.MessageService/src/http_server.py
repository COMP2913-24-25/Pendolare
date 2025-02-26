"""
Dedicated HTTP server for health checks and diagnostics
"""
import asyncio
import logging
import json
import os
from aiohttp import web
from datetime import datetime

logger = logging.getLogger(__name__)

# Simple in-memory status tracking
service_status = {
    'startup_time': datetime.now().isoformat(),
    'websocket_connections': 0,
    'health_checks': 0,
    'errors': 0,
    'last_error': None
}

async def health_handler(request):
    """Simple health check endpoint"""
    service_status['health_checks'] += 1
    return web.Response(text="OK", content_type="text/plain")

async def diagnostics_handler(request):
    """Return diagnostic information"""
    try:
        diagnostic_data = {
            'status': service_status,
            'environment': {
                'KONG_GATEWAY_URL': os.environ.get('KONG_GATEWAY_URL'),
                'SERVICE_NAME': os.environ.get('SERVICE_NAME'),
                'CONTAINER_APP_ENV': os.environ.get('CONTAINER_APP_ENV'),
                'PYTHON_VERSION': os.environ.get('PYTHON_VERSION'),
            },
            'request': {
                'headers': dict(request.headers),
                'path': request.path,
                'method': request.method
            }
        }
        
        return web.json_response(diagnostic_data)
    except Exception as e:
        service_status['errors'] += 1
        service_status['last_error'] = str(e)
        return web.json_response({
            'error': str(e),
            'status': 'ERROR'
        }, status=500)

async def logs_handler(request):
    """Return log information"""
    # In a real implementation, we would fetch logs from somewhere,
    # but for now we'll just return a placeholder
    return web.json_response({
        'logs': [
            {'timestamp': datetime.now().isoformat(), 'level': 'INFO', 'message': 'Log endpoint accessed'}
        ]
    })

def create_http_app():
    """Create and configure the HTTP app"""
    app = web.Application()
    app.router.add_get('/health', health_handler)
    app.router.add_get('/diagnostics', diagnostics_handler)
    app.router.add_get('/diagnostics/status', diagnostics_handler)
    app.router.add_get('/diagnostics/logs', logs_handler)
    
    # Add CORS middleware if needed
    return app

def update_status(key, value):
    """Update the service status"""
    service_status[key] = value
    
    # Keep track of connection count
    if key == 'connection_opened':
        service_status['websocket_connections'] += 1
    elif key == 'connection_closed':
        service_status['websocket_connections'] = max(0, service_status['websocket_connections'] - 1)
    elif key == 'error':
        service_status['errors'] += 1
        service_status['last_error'] = value

async def start_http_server(host='0.0.0.0', port=5007):
    """Start the HTTP server"""
    app = create_http_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    logger.info(f"HTTP server started on {host}:{port}")
    return runner
