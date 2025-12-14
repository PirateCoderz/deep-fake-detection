@echo off
echo ========================================
echo Organizing Project Structure
echo ========================================
echo.

REM Create directory structure
mkdir guides\setup 2>nul
mkdir guides\training 2>nul
mkdir guides\testing 2>nul
mkdir guides\troubleshooting 2>nul
mkdir guides\progress 2>nul
mkdir scripts\startup 2>nul
mkdir scripts\utilities 2>nul

echo Moving setup guides...
move /Y "DATABASE_SETUP_GUIDE.md" "guides\setup\" 2>nul
move /Y "PGADMIN_VISUAL_GUIDE.md" "guides\setup\" 2>nul
move /Y "FRONTEND_SETUP_GUIDE.md" "guides\setup\" 2>nul
move /Y "START_HERE.md" "guides\setup\" 2>nul
move /Y "QUICK_START.md" "guides\setup\" 2>nul
move /Y "1_SETUP_COMPLETE.md" "guides\progress\" 2>nul

echo Moving training guides...
move /Y "HOW_TO_TRAIN_MODEL.md" "guides\training\" 2>nul
move /Y "HOW_TO_ADD_REAL_IMAGES.md" "guides\training\" 2>nul
move /Y "IMPROVING_MODEL_ACCURACY.md" "guides\training\" 2>nul

echo Moving testing guides...
move /Y "TESTING_COMPLETE_GUIDE.md" "guides\testing\" 2>nul
move /Y "TESTING_GUIDE.md" "guides\testing\" 2>nul
move /Y "HOW_TO_TEST.md" "guides\testing\" 2>nul

echo Moving troubleshooting guides...
move /Y "FIX_BACKEND_IMPORT_ERROR.md" "guides\troubleshooting\" 2>nul
move /Y "FIX_SWC_ERROR.md" "guides\troubleshooting\" 2>nul
move /Y "FINAL_FIX_GUIDE.md" "guides\troubleshooting\" 2>nul
move /Y "SOLUTION_SWC_BINARY.md" "guides\troubleshooting\" 2>nul
move /Y "BACKEND_FIXED.md" "guides\troubleshooting\" 2>nul
move /Y "DO_THIS_NOW.md" "guides\troubleshooting\" 2>nul

echo Moving progress/status guides...
move /Y "2_data_models_and_database_complete.md" "guides\progress\" 2>nul
move /Y "2_3_classification_logging_test_complete.md" "guides\progress\" 2>nul
move /Y "3_build_image_preprocessing_complete.md" "guides\progress\" 2>nul
move /Y "3_image_preprocessing_pipeline_complete.md" "guides\progress\" 2>nul
move /Y "5_training_dataset_pipeline_complete.md" "guides\progress\" 2>nul
move /Y "6_cnn_model_training_progress.md" "guides\progress\" 2>nul
move /Y "8_explainability_module_complete.md" "guides\progress\" 2>nul
move /Y "9_fastapi_backend_complete.md" "guides\progress\" 2>nul
move /Y "10_logging_metrics_services_complete.md" "guides\progress\" 2>nul
move /Y "11_CHECKPOINT_SUMMARY.md" "guides\progress\" 2>nul
move /Y "12_FRONTEND_COMPLETE.md" "guides\progress\" 2>nul
move /Y "TASK_6_COMPLETE.md" "guides\progress\" 2>nul
move /Y "TASK_10_README.md" "guides\progress\" 2>nul
move /Y "FINAL_BACKEND_STATUS.md" "guides\progress\" 2>nul
move /Y "FINAL_PROJECT_SUMMARY.md" "guides\progress\" 2>nul
move /Y "PROJECT_PROGRESS_SUMMARY.md" "guides\progress\" 2>nul
move /Y "SESSION_SUMMARY.md" "guides\progress\" 2>nul

echo Moving reference guides...
move /Y "ALL_FIXED_NOW.md" "guides\" 2>nul
move /Y "START_SYSTEM_NOW.md" "guides\" 2>nul
move /Y "RUN_NOW.md" "guides\" 2>nul
move /Y "RUN_SYSTEM.md" "guides\" 2>nul
move /Y "SYSTEM_READY.md" "guides\" 2>nul
move /Y "WHAT_TO_DO_NOW.md" "guides\" 2>nul
move /Y "README_NEXT_STEPS.md" "guides\" 2>nul
move /Y "READY_TO_RUN.txt" "guides\" 2>nul
move /Y "DOCUMENTATION_INDEX.md" "guides\" 2>nul

echo Moving startup scripts...
move /Y "start-backend.bat" "scripts\startup\" 2>nul
move /Y "start-backend.ps1" "scripts\startup\" 2>nul
move /Y "start-frontend-new-terminal.bat" "scripts\startup\" 2>nul
move /Y "start-frontend-new-terminal.ps1" "scripts\startup\" 2>nul

echo Moving utility scripts...
move /Y "run_backend.py" "scripts\utilities\" 2>nul
move /Y "augment_dataset.py" "scripts\utilities\" 2>nul
move /Y "create_sample_dataset.py" "scripts\utilities\" 2>nul
move /Y "download_sample_images.py" "scripts\utilities\" 2>nul
move /Y "demo_system.py" "scripts\utilities\" 2>nul
move /Y "quick_demo.py" "scripts\utilities\" 2>nul
move /Y "test_db_connection.py" "scripts\utilities\" 2>nul
move /Y "test_system.py" "scripts\utilities\" 2>nul
move /Y "test_trained_model.py" "scripts\utilities\" 2>nul
move /Y "run_all_tests.py" "scripts\utilities\" 2>nul
move /Y "verify_setup.py" "scripts\utilities\" 2>nul

echo.
echo ========================================
echo Organization Complete!
echo ========================================
echo.
echo Project structure:
echo.
echo Root:
echo   - README.md (main documentation)
echo   - SYSTEM_WORKING_NOW.md (quick start)
echo   - start-both.bat (main startup script)
echo   - start-both.ps1 (PowerShell version)
echo   - train.py (model training)
echo.
echo guides/
echo   - setup/ (installation guides)
echo   - training/ (model training guides)
echo   - testing/ (testing guides)
echo   - troubleshooting/ (fix guides)
echo   - progress/ (task completion docs)
echo.
echo scripts/
echo   - startup/ (startup scripts)
echo   - utilities/ (utility scripts)
echo.
pause
