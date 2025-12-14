@echo off
echo ========================================
echo Starting Next.js Frontend
echo ========================================
echo.
echo IMPORTANT: This script must run OUTSIDE Python venv
echo to avoid SWC binary loading errors.
echo.

REM Check if we're in a venv and warn user
if defined VIRTUAL_ENV (
    echo WARNING: Python virtual environment detected!
    echo Please run this script from a NEW terminal window
    echo WITHOUT activating the venv.
    echo.
    echo Steps:
    echo 1. Open a NEW Command Prompt or PowerShell
    echo 2. Navigate to: %~dp0
    echo 3. Run: run-frontend.bat
    echo.
    pause
    exit /b 1
)

REM Navigate to frontend directory
cd /d "%~dp0"

REM Check if node_modules exists
if not exist "node_modules" (
    echo node_modules not found. Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo.
        echo ERROR: npm install failed!
        pause
        exit /b 1
    )
    echo.
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo Creating .env.local from example...
    copy .env.local.example .env.local
    echo.
)

echo Starting development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo Backend API should be running at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the dev server
call npm run dev

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start development server!
    echo.
    echo Troubleshooting:
    echo 1. Make sure you're NOT in Python venv
    echo 2. Try: npm install
    echo 3. Try: npm cache clean --force
    echo 4. Delete node_modules and .next, then npm install
    echo.
    pause
    exit /b 1
)

pause
