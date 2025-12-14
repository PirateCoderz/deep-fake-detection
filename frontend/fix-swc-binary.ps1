# Fix SWC Binary Issue on Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fixing SWC Binary Issue" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will:" -ForegroundColor Yellow
Write-Host "1. Delete corrupted SWC binary" -ForegroundColor Yellow
Write-Host "2. Clear npm cache" -ForegroundColor Yellow
Write-Host "3. Reinstall dependencies" -ForegroundColor Yellow
Write-Host ""
Write-Host "This may take 2-3 minutes..." -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to continue"

Set-Location $PSScriptRoot

Write-Host ""
Write-Host "Step 1: Deleting corrupted SWC binary..." -ForegroundColor Cyan
if (Test-Path "node_modules\@next\swc-win32-x64-msvc") {
    Remove-Item -Recurse -Force "node_modules\@next\swc-win32-x64-msvc"
    Write-Host "✓ Deleted SWC binary" -ForegroundColor Green
} else {
    Write-Host "! SWC binary folder not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Clearing npm cache..." -ForegroundColor Cyan
npm cache clean --force
Write-Host "✓ Cache cleared" -ForegroundColor Green

Write-Host ""
Write-Host "Step 3: Reinstalling SWC binary..." -ForegroundColor Cyan
npm install @next/swc-win32-x64-msvc@14.0.4 --force
Write-Host "✓ SWC binary reinstalled" -ForegroundColor Green

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fix Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Now try running: npm run dev" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
