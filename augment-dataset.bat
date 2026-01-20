@echo off
echo ========================================
echo Dataset Augmentation Tool
echo ========================================
echo.

REM Check if argument provided
if "%1"=="" (
    set NUM_AUG=10
    echo Using default: 10 augmentations per image
) else (
    set NUM_AUG=%1
    echo Creating %1 augmentations per image
)

echo.

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
    echo.
)

REM Run simple augmentation script (no complex imports)
python scripts\utilities\augment_dataset_simple.py %NUM_AUG%

echo.
echo ========================================
echo Done!
echo ========================================
echo.
echo Next steps:
echo 1. Check augmented images in data/train_augmented/
echo 2. Update train.py to use augmented data
echo 3. Run: python train.py
echo.
pause
