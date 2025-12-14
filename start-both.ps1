# PowerShell script to start both backend and frontend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Fake Product Detection System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will start BOTH backend and frontend" -ForegroundColor Yellow
Write-Host "in separate terminal windows." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"

# Check if venv exists
if (-not (Test-Path ".venv\Scripts\Activate.ps1")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first." -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 1: Starting Backend (with venv)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; .venv\Scripts\Activate.ps1; Write-Host 'Starting Backend...' -ForegroundColor Green; python scripts\utilities\run_backend.py"

Write-Host "✓ Backend terminal opened" -ForegroundColor Green
Write-Host ""

Start-Sleep -Seconds 3

Write-Host "Step 2: Starting Frontend (without venv)..." -ForegroundColor Cyan
$frontendPath = Join-Path $PWD "frontend"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; Write-Host 'Starting Frontend...' -ForegroundColor Green; npm run dev"

Write-Host "✓ Frontend terminal opened" -ForegroundColor Green
Write-Host ""
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "System Starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Two new terminal windows have been opened:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Backend Terminal (with venv)" -ForegroundColor Cyan
Write-Host "   - Starting FastAPI backend..." -ForegroundColor White
Write-Host "   - Will be available at: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "2. Frontend Terminal (without venv)" -ForegroundColor Cyan
Write-Host "   - Starting Next.js frontend..." -ForegroundColor White
Write-Host "   - Will be available at: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Wait 10-15 seconds for both to start, then:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Open your browser to: http://localhost:3000" -ForegroundColor Green
Write-Host ""
Write-Host "To stop the system:" -ForegroundColor Yellow
Write-Host "- Close both terminal windows" -ForegroundColor White
Write-Host "- Or press Ctrl+C in each window" -ForegroundColor White
Write-Host ""
Read-Host "Press Enter to close this window"
