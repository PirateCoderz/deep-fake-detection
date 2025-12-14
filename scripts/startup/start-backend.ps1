# PowerShell script to start FastAPI backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting FastAPI Backend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if venv is activated
if (-not $env:VIRTUAL_ENV) {
    Write-Host "ERROR: Python virtual environment is NOT activated!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please activate venv first:" -ForegroundColor Yellow
    Write-Host "  .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Then run this script again." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✓ Virtual environment is active" -ForegroundColor Green
Write-Host ""

# Navigate to project root
Set-Location $PSScriptRoot

Write-Host "Starting FastAPI backend..." -ForegroundColor Green
Write-Host ""
Write-Host "Backend will be available at: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API docs will be available at: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the backend using wrapper script
python run_backend.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to start backend!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure venv is activated: .venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "2. Install dependencies: pip install -r backend/requirements.txt" -ForegroundColor Yellow
    Write-Host "3. Check database connection: python test_db_connection.py" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
