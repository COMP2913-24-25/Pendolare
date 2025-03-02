@echo off
echo ======================================
echo Message Service - Local Rebuild Script
echo ======================================
echo.

REM Kill any running instances
echo Stopping any running containers...
docker-compose down

REM Build the Docker image
echo Building Docker image...
docker-compose build

REM Check if Kong network exists, create if it doesn't
echo Checking if Kong network exists...
docker network inspect kong-net >nul 2>&1
if %errorlevel% neq 0 (
    echo Creating Kong network...
    docker network create kong-net
)

REM Start the service
echo Starting service...
docker-compose up -d