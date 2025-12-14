# This script opens a NEW PowerShell window for the frontend
# This ensures Python venv is NOT active

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Opening NEW PowerShell for frontend..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will open a new PowerShell window" -ForegroundColor Yellow
Write-Host "WITHOUT Python virtual environment." -ForegroundColor Yellow
Write-Host ""
Write-Host "The new window will:" -ForegroundColor Green
Write-Host "1. Navigate to frontend directory" -ForegroundColor Green
Write-Host "2. Start npm run dev" -ForegroundColor Green
Write-Host ""
Write-Host "Keep both windows open." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$frontendDir = Join-Path $scriptDir "frontend"

# Open new PowerShell window and run frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendDir'; Write-Host 'Starting Next.js frontend...' -ForegroundColor Green; Write-Host ''; npm run dev"

Write-Host ""
Write-Host "✅ New PowerShell window opened!" -ForegroundColor Green
Write-Host ""
Write-Host "You should see a new PowerShell window." -ForegroundColor Cyan
Write-Host "The frontend will start in that window." -ForegroundColor Cyan
Write-Host ""
Write-Host "If you don't see it, check your taskbar." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to close this window"
