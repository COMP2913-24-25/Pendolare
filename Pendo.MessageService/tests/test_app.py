import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
import websockets

from src import app


@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint returns correct response"""
    mock_request = MagicMock()
    
    response = await app.health_check(mock_request)
    
    assert response.status == 200
    
    # Extract response data by checking if response has text attribute
    # and using it if it's callable, otherwise decode the body
    if hasattr(response, 'text'):
        if callable(response.text):
            data = json.loads(await response.text())
        else:
            data = json.loads(response.text)
    else:
        # Mock response in test
        data = json.loads(response.body.decode('utf-8'))
    
    assert data["status"] == "healthy" 
    assert "timestamp" in data
    assert data["service"] == "message-service"


@pytest.mark.asyncio
async def test_root_handler():
    """Test the root handler returns service information"""
    mock_request = MagicMock()
    mock_request.headers = {"Host": "localhost:9999"}
    mock_request.url.scheme = "http"
    
    response = await app.root_handler(mock_request)
    
    assert response.status == 200
    
    # Handle response data extraction as in test_health_check
    if hasattr(response, 'text'):
        if callable(response.text):
            data = json.loads(await response.text())
        else:
            data = json.loads(response.text)
    else:
        data = json.loads(response.body.decode('utf-8'))
    
    # Check service info
    assert data["service"] == "Pendo Message Service"
    assert "version" in data
    assert "endpoints" in data
    assert "health" in data["endpoints"]
    assert "websocket" in data["endpoints"]
    assert data["endpoints"]["websocket"].startswith("ws://")


@pytest.mark.asyncio
async def test_websocket_handler_welcome_message(mock_websocket):
    """Test websocket handler sends welcome message"""
        
    # Mock recv to raise ConnectionClosed after first message simulating disconnect
    async def mock_recv():
        raise websockets.exceptions.ConnectionClosed(1000, "Test disconnect")
    
    mock_websocket.recv = mock_recv
    
    await app.websocket_handler(mock_websocket)
    
    # Check welcome message was sent
    assert len(mock_websocket.sent_messages) >= 1
    welcome_msg = json.loads(mock_websocket.sent_messages[0])
    assert welcome_msg["type"] == "welcome"
    assert "Connected to Pendo Message Service" in welcome_msg["message"]


@pytest.mark.asyncio
async def test_setup_http_server():
    """Test HTTP server setup"""

    # Derived from: https://stackoverflow.com/questions/57699218/how-can-i-mock-out-responses-made-by-aiohttp-clientsession
    with patch('aiohttp.web.AppRunner') as mock_runner_class:
        # Create a mock runner instance with async methods
        mock_runner_instance = AsyncMock()
        mock_runner_class.return_value = mock_runner_instance
        
        # 
        with patch('aiohttp.web.TCPSite') as mock_site_class:
            # Create a mock site instance with async methods
            mock_site_instance = AsyncMock()
            mock_site_class.return_value = mock_site_instance
            
            result = await app.setup_http_server()
            
            mock_site_class.assert_called_once()
            mock_site_instance.start.assert_awaited_once()
            assert result == mock_runner_instance


@pytest.mark.asyncio
async def test_setup_ws_server():
    """Test WebSocket server setup"""

    # Derived from: https://github.com/python-websockets/websockets/issues/282
    with patch('websockets.serve') as mock_serve:
       
        # Create a dummy server
        async def mock_server(*args, **kwargs):
            return "mock_server"
        
        mock_serve.side_effect = mock_server
        
        result = await app.setup_ws_server()
        
        mock_serve.assert_called_once()
        assert result == "mock_server"
