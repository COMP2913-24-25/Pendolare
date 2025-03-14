@echo off
REM Set Python path to include the current directory
SET PYTHONPATH=%CD%

REM Set environment variables for testing
SET ENV=Testing
SET USE_DATABASE=false
SET LOG_LEVEL=DEBUG

REM Run tests with coverage reporting
pytest -xvs tests/ --cov=src --cov-report=term-missing

REM Pause to see the results
pause
