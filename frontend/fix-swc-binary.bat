@echo off
echo ========================================
echo Fixing SWC Binary Issue
echo ========================================
echo.
echo This will:
echo 1. Delete corrupted SWC binary
echo 2. Clear npm cache
echo 3. Reinstall dependencies
echo.
echo This may take 2-3 minutes...
echo.
pause

cd /d "%~dp0"

echo.
echo Step 1: Deleting corrupted SWC binary...
if exist "node_modules\@next\swc-win32-x64-msvc" (
    rmdir /s /q "node_modules\@next\swc-win32-x64-msvc"
    echo ✓ Deleted SWC binary
) else (
    echo ! SWC binary folder not found
)

echo.
echo Step 2: Clearing npm cache...
call npm cache clean --force
echo ✓ Cache cleared

echo.
echo Step 3: Reinstalling SWC binary...
call npm install @next/swc-win32-x64-msvc@14.0.4 --force
echo ✓ SWC binary reinstalled

echo.
echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo Now try running: npm run dev
echo.
pause
