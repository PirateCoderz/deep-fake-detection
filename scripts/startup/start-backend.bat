@echo off
echo ========================================
echo Starting FastAPI Backend
echo ========================================
echo.

REM Check if venv is activated
if not defined VIRTUAL_ENV (
    echo ERROR: Python virtual environment is NOT activated!
    echo.
    echo Please activate venv first:
    echo   .venv\Scripts\activate
    echo.
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo ✓ Virtual environment is active
echo.

REM Navigate to project root
cd /d "%~dp0"

echo Starting FastAPI backend...
echo.
echo Backend will be available at: http://localhost:8000
echo API docs will be available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the backend using wrapper script
python run_backend.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start backend!
    echo.
    echo Troubleshooting:
    echo 1. Make sure venv is activated: .venv\Scripts\activate
    echo 2. Install dependencies: pip install -r backend/requirements.txt
    echo 3. Check database connection: python test_db_connection.py
    echo.
    pause
    exit /b 1
)

pause
