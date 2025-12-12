#!/bin/bash
# Setup script for macOS/Linux

set -e

echo "Setting up Fake Product Detection System..."
echo ""

# Create Python virtual environment
echo "Creating Python virtual environment..."
cd backend
python3 -m venv venv

# Activate virtual environment and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

cd ..

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and configure your settings"
echo "2. Start Docker services: docker-compose up -d"
echo "3. Run database migrations: cd backend && source venv/bin/activate && alembic upgrade head"
echo "4. Start the backend: cd backend && source venv/bin/activate && python src/main.py"
echo ""
