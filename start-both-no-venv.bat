@echo off
echo ========================================
echo Fake Product Detection System
echo Starting WITHOUT Virtual Environment
echo ========================================
echo.

REM Start Backend
echo [1/2] Starting Backend Server...
start "Backend Server" cmd /k "cd /d %~dp0 && python scripts\utilities\run_backend.py"

REM Wait for backend to initialize
echo Waiting for backend to start...
timeout /t 10 /nobreak > nul

REM Start Frontend
echo [2/2] Starting Frontend Server...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ========================================
echo System is starting...
echo ========================================
echo.
echo Backend API:  http://localhost:8000
echo API Docs:     http://localhost:8000/docs
echo Frontend:     http://localhost:3000
echo.
echo Wait 10-15 seconds for both servers to be ready
echo Then open: http://localhost:3000
echo.
echo Press any key to close this window
echo (Backend and Frontend will keep running)
pause > nul
