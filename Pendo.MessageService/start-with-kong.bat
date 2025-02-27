@echo off

echo ==============================================
echo Starting Kong Gateway + Message Service
echo ==============================================

REM Clean up existing containers
echo Stopping any existing containers...
docker-compose -f docker-compose.message-kong.yml down
timeout /t 2 /nobreak > nul

REM Build and start services
echo Building and starting services...
docker-compose -f docker-compose.message-kong.yml up --build -d
timeout /t 5 /nobreak > nul

REM Check if services are running
echo Checking if services are running:
docker ps --format "table {{.Names}}\t{{.Status}}"

REM Display available endpoints
echo.
echo ==============================================
echo Available endpoints:
echo ==============================================
echo Kong Gateway API:      http://localhost:8000
echo Kong Admin API:        http://localhost:8001
echo WebSocket (direct):    ws://localhost:5006/ws
echo WebSocket (via Kong):  ws://localhost:8000/message/ws
echo Test Client:           http://localhost:5059/test-client
echo ==============================================
echo.

REM Open the test client
echo Opening test client in browser...
start "" http://localhost:5059/test-client

REM Show logs
echo Showing logs (press Ctrl+C to stop)...
docker-compose -f docker-compose.message-kong.yml logs -f
