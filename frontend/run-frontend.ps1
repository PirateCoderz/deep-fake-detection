# PowerShell script to run Next.js frontend
# Run this OUTSIDE Python venv to avoid SWC binary errors

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting Next.js Frontend" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in a venv
if ($env:VIRTUAL_ENV) {
    Write-Host "WARNING: Python virtual environment detected!" -ForegroundColor Yellow
    Write-Host "Please run this script from a NEW terminal window" -ForegroundColor Yellow
    Write-Host "WITHOUT activating the venv." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Steps:" -ForegroundColor Yellow
    Write-Host "1. Open a NEW PowerShell window" -ForegroundColor Yellow
    Write-Host "2. Navigate to: $PSScriptRoot" -ForegroundColor Yellow
    Write-Host "3. Run: .\run-frontend.ps1" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Navigate to frontend directory
Set-Location $PSScriptRoot

# Check if node_modules exists
if (-not (Test-Path "node_modules")) {
    Write-Host "node_modules not found. Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "ERROR: npm install failed!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host ""
}

# Check if .env.local exists
if (-not (Test-Path ".env.local")) {
    Write-Host "Creating .env.local from example..." -ForegroundColor Yellow
    Copy-Item ".env.local.example" ".env.local"
    Write-Host ""
}

Write-Host "Starting development server..." -ForegroundColor Green
Write-Host ""
Write-Host "Frontend will be available at: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend API should be running at: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the dev server
npm run dev

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to start development server!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Troubleshooting:" -ForegroundColor Yellow
    Write-Host "1. Make sure you're NOT in Python venv" -ForegroundColor Yellow
    Write-Host "2. Try: npm install" -ForegroundColor Yellow
    Write-Host "3. Try: npm cache clean --force" -ForegroundColor Yellow
    Write-Host "4. Delete node_modules and .next, then npm install" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
