@echo off
echo ========================================
echo Database Password Configuration Helper
echo ========================================
echo.
echo This script will help you fix the database password issue.
echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
    echo.
)

REM Run the password fix script
python scripts\utilities\fix_database_password.py

echo.
pause
