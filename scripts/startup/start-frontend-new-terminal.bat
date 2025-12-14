@echo off
REM This script opens a NEW terminal window for the frontend
REM This ensures Python venv is NOT active

echo ========================================
echo Opening NEW terminal for frontend...
echo ========================================
echo.
echo This will open a new Command Prompt window
echo WITHOUT Python virtual environment.
echo.
echo The new window will:
echo 1. Navigate to frontend directory
echo 2. Start npm run dev
echo.
echo Keep this window and the new window open.
echo.
pause

REM Open new Command Prompt window and run frontend
start cmd /k "cd /d %~dp0frontend && echo Starting Next.js frontend... && echo. && npm run dev"

echo.
echo ✅ New terminal window opened!
echo.
echo You should see a new Command Prompt window.
echo The frontend will start in that window.
echo.
echo If you don't see it, check your taskbar.
echo.
pause
