import os
import json
import logging
import platform
import socket
import sys
from datetime import datetime
import traceback
from typing import Dict, Any, List, Optional

# In-memory log buffer
MAX_LOG_ENTRIES = 100
log_buffer = []

class MemoryLogHandler(logging.Handler):
    """Custom log handler that stores logs in memory for diagnostic retrieval"""
    def __init__(self):
        super().__init__()
        self.setLevel(logging.INFO)
        self.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    
    def emit(self, record):
        log_entry = self.format(record)
        # Add to buffer with timestamp
        log_buffer.append({
            'timestamp': datetime.now().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name
        })
        # Keep buffer size limited
        if len(log_buffer) > MAX_LOG_ENTRIES:
            log_buffer.pop(0)

# Set up memory logging
memory_handler = MemoryLogHandler()
root_logger = logging.getLogger()
root_logger.addHandler(memory_handler)

# Status tracking
connection_stats = {
    'total_connections': 0,
    'active_connections': 0,
    'failed_connections': 0,
    'messages_received': 0,
    'messages_sent': 0,
    'last_error': None,
    'last_connection_time': None,
    'service_start_time': datetime.now().isoformat()
}

def update_stats(action: str, **kwargs):
    """Update connection statistics"""
    if action == 'connection_open':
        connection_stats['total_connections'] += 1
        connection_stats['active_connections'] += 1
        connection_stats['last_connection_time'] = datetime.now().isoformat()
    elif action == 'connection_close':
        connection_stats['active_connections'] = max(0, connection_stats['active_connections'] - 1)
    elif action == 'connection_fail':
        connection_stats['failed_connections'] += 1
        if 'error' in kwargs:
            connection_stats['last_error'] = str(kwargs['error'])
    elif action == 'message_received':
        connection_stats['messages_received'] += 1
    elif action == 'message_sent':
        connection_stats['messages_sent'] += 1

async def handle_diagnostics_request(path: str) -> tuple:
    """Handle diagnostic HTTP requests"""
    if path == '/diagnostics':
        return create_diagnostic_response()
    elif path == '/diagnostics/logs':
        return create_logs_response()
    elif path == '/diagnostics/status':
        return create_status_response()
    elif path == '/diagnostics/environment':
        return create_environment_response()
    elif path == '/diagnostics/network':
        return create_network_response()
    
    return None  # Not a diagnostic path

def create_diagnostic_response() -> tuple:
    """Generate full diagnostic information"""
    try:
        diagnostic_data = {
            'status': connection_stats,
            'environment': get_environment_info(),
            'network': get_network_info(),
            'system': get_system_info(),
            'recent_logs': log_buffer[-10:] if log_buffer else []
        }
        
        return 200, {'Content-Type': 'application/json'}, json.dumps(diagnostic_data).encode('utf-8')
    except Exception as e:
        error_data = {
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return 500, {'Content-Type': 'application/json'}, json.dumps(error_data).encode('utf-8')

def create_logs_response() -> tuple:
    """Return recent logs"""
    return 200, {'Content-Type': 'application/json'}, json.dumps({
        'logs': log_buffer
    }).encode('utf-8')

def create_status_response() -> tuple:
    """Return current connection status"""
    return 200, {'Content-Type': 'application/json'}, json.dumps({
        'status': connection_stats
    }).encode('utf-8')

def create_environment_response() -> tuple:
    """Return environment information"""
    return 200, {'Content-Type': 'application/json'}, json.dumps({
        'environment': get_environment_info()
    }).encode('utf-8')

def create_network_response() -> tuple:
    """Return network diagnostics"""
    network_info = get_network_info()
    
    # Attempt simple connectivity tests
    kong_url = os.environ.get('KONG_GATEWAY_URL')
    if kong_url:
        if kong_url.startswith('http'):
            kong_host = kong_url.split('://')[1].split('/')[0]
        else:
            kong_host = kong_url.split('/')[0]
            
        try:
            socket.gethostbyname(kong_host)
            network_info['kong_dns_resolution'] = 'success'
        except Exception as e:
            network_info['kong_dns_resolution'] = f'failed: {str(e)}'
    
    return 200, {'Content-Type': 'application/json'}, json.dumps({
        'network': network_info
    }).encode('utf-8')

def get_environment_info() -> Dict[str, Any]:
    """Get environment information"""
    safe_env = {}
    sensitive_keys = ['PASSWORD', 'SECRET', 'KEY', 'TOKEN', 'CREDENTIAL']
    
    for key, value in os.environ.items():
        # Filter sensitive information
        if any(sensitive in key.upper() for sensitive in sensitive_keys):
            safe_env[key] = '******'
        else:
            safe_env[key] = value
    
    return {
        'variables': safe_env,
        'python_version': sys.version,
        'python_path': sys.executable,
    }

def get_network_info() -> Dict[str, Any]:
    """Get network information"""
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except:
        local_ip = "Unable to determine"
    
    kong_url = os.environ.get('KONG_GATEWAY_URL', 'Not configured')
    
    return {
        'hostname': hostname,
        'local_ip': local_ip,
        'kong_gateway_url': kong_url,
    }

def get_system_info() -> Dict[str, Any]:
    """Get system information"""
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'python_impl': platform.python_implementation(),
        'python_version': platform.python_version(),
    }
