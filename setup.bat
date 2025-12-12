@echo off
REM Setup script for Windows

echo Setting up Fake Product Detection System...
echo.

REM Create Python virtual environment
echo Creating Python virtual environment...
cd backend
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    exit /b 1
)

REM Activate virtual environment and install dependencies
echo Installing Python dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    exit /b 1
)

cd ..

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Copy .env.example to .env and configure your settings
echo 2. Start Docker services: docker-compose up -d
echo 3. Run database migrations: cd backend ^&^& alembic upgrade head
echo 4. Start the backend: cd backend ^&^& venv\Scripts\activate ^&^& python src\main.py
echo.
