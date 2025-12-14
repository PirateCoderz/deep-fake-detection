@echo off
echo ========================================
echo Starting Fake Product Detection System
echo ========================================
echo.
echo This will start BOTH backend and frontend
echo in separate terminal windows.
echo.
pause

REM Check if venv exists
if not exist ".venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first.
    pause
    exit /b 1
)

echo.
echo Step 1: Starting Backend (with venv)...
start "Backend - Fake Product Detection" cmd /k ".venv\Scripts\activate.bat && python scripts\utilities\run_backend.py"

echo ✓ Backend terminal opened
echo.

timeout /t 3 /nobreak >nul

echo Step 2: Starting Frontend (without venv)...
start "Frontend - Fake Product Detection" cmd /k "cd frontend && npm run dev"

echo ✓ Frontend terminal opened
echo.
echo.
echo ========================================
echo System Starting!
echo ========================================
echo.
echo Two new terminal windows have been opened:
echo.
echo 1. Backend Terminal (with venv)
echo    - Starting FastAPI backend...
echo    - Will be available at: http://localhost:8000
echo.
echo 2. Frontend Terminal (without venv)
echo    - Starting Next.js frontend...
echo    - Will be available at: http://localhost:3000
echo.
echo Wait 10-15 seconds for both to start, then:
echo.
echo Open your browser to: http://localhost:3000
echo.
echo To stop the system:
echo - Close both terminal windows
echo - Or press Ctrl+C in each window
echo.
pause
