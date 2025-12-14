# 📁 Project Structure

## Overview

The project is now organized into a clean, logical structure with all documentation and scripts properly categorized.

---

## Root Directory

```
deep-fake-detection/
├── README.md                    # Main documentation
├── SYSTEM_WORKING_NOW.md       # Quick start guide
├── start-both.bat              # Main startup script ⭐
├── start-both.ps1              # PowerShell version
├── train.py                    # Model training
├── setup.bat                   # Initial setup
├── docker-compose.yml          # Docker configuration
├── .env.example                # Environment variables template
└── update_database_schema.sql  # Database schema updates
```

---

## Guides Directory

### guides/
```
guides/
├── DOCUMENTATION_INDEX.md      # Complete documentation index
├── ALL_FIXED_NOW.md           # All fixes summary
├── START_SYSTEM_NOW.md        # Complete startup guide
├── RUN_NOW.md                 # Quick reference
├── RUN_SYSTEM.md              # Visual step-by-step
├── SYSTEM_READY.md            # System overview
├── WHAT_TO_DO_NOW.md          # What to do next
├── README_NEXT_STEPS.md       # Next steps guide
└── READY_TO_RUN.txt           # ASCII art summary
```

### guides/setup/
```
guides/setup/
├── START_HERE.md              # Getting started
├── QUICK_START.md             # Quick setup guide
├── DATABASE_SETUP_GUIDE.md    # Database setup
├── PGADMIN_VISUAL_GUIDE.md    # Visual database guide
└── FRONTEND_SETUP_GUIDE.md    # Frontend setup
```

### guides/training/
```
guides/training/
├── HOW_TO_TRAIN_MODEL.md      # Model training guide
├── HOW_TO_ADD_REAL_IMAGES.md  # Adding training data
└── IMPROVING_MODEL_ACCURACY.md # Accuracy improvement tips
```

### guides/testing/
```
guides/testing/
├── TESTING_COMPLETE_GUIDE.md  # Complete testing guide
├── TESTING_GUIDE.md           # Testing overview
└── HOW_TO_TEST.md             # Quick testing reference
```

### guides/troubleshooting/
```
guides/troubleshooting/
├── FIX_BACKEND_IMPORT_ERROR.md # Backend import fixes
├── FIX_SWC_ERROR.md           # Frontend SWC fixes
├── FINAL_FIX_GUIDE.md         # Complete fix guide
├── SOLUTION_SWC_BINARY.md     # SWC solutions
├── BACKEND_FIXED.md           # Backend fix details
└── DO_THIS_NOW.md             # Immediate fixes
```

### guides/progress/
```
guides/progress/
├── 1_SETUP_COMPLETE.md
├── 2_data_models_and_database_complete.md
├── 3_image_preprocessing_pipeline_complete.md
├── 5_training_dataset_pipeline_complete.md
├── 6_cnn_model_training_progress.md
├── 8_explainability_module_complete.md
├── 9_fastapi_backend_complete.md
├── 10_logging_metrics_services_complete.md
├── 11_CHECKPOINT_SUMMARY.md
├── 12_FRONTEND_COMPLETE.md
├── TASK_6_COMPLETE.md
├── TASK_10_README.md
├── FINAL_BACKEND_STATUS.md
├── FINAL_PROJECT_SUMMARY.md
├── PROJECT_PROGRESS_SUMMARY.md
└── SESSION_SUMMARY.md
```

---

## Scripts Directory

### scripts/startup/
```
scripts/startup/
├── start-backend.bat          # Start backend only
├── start-backend.ps1          # PowerShell version
├── start-frontend-new-terminal.bat # Start frontend in new window
└── start-frontend-new-terminal.ps1 # PowerShell version
```

### scripts/utilities/
```
scripts/utilities/
├── run_backend.py             # Backend wrapper script
├── augment_dataset.py         # Data augmentation
├── create_sample_dataset.py   # Create sample data
├── download_sample_images.py  # Download images
├── demo_system.py             # System demo
├── quick_demo.py              # Quick demo
├── test_db_connection.py      # Test database
├── test_system.py             # Test system
├── test_trained_model.py      # Test model
├── run_all_tests.py           # Run all tests
└── verify_setup.py            # Verify setup
```

---

## Backend Directory

```
backend/
├── src/
│   ├── main.py                # FastAPI application
│   ├── config.py              # Configuration
│   ├── models.py              # Data models
│   ├── database.py            # Database connection
│   ├── db_models.py           # SQLAlchemy models
│   ├── preprocessor.py        # Image preprocessing
│   ├── classifier.py          # CNN classifier
│   ├── explainability.py      # Grad-CAM & explanations
│   ├── logging_service.py     # Classification logging
│   ├── metrics_service.py     # Metrics calculation
│   ├── train_model.py         # Model training
│   └── data_collection.py     # Data collection
└── requirements.txt           # Python dependencies
```

---

## Frontend Directory

```
frontend/
├── src/
│   ├── app/                   # Next.js pages (server components)
│   │   ├── layout.tsx         # Root layout
│   │   ├── page.tsx           # Home page
│   │   ├── globals.css        # Global styles
│   │   └── results/[id]/page.tsx # Results page
│   ├── components/            # React components (client components)
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   └── ResultsPage.tsx
│   │   ├── upload/
│   │   │   ├── ImageUploader.tsx
│   │   │   └── ImagePreview.tsx
│   │   ├── results/
│   │   │   ├── ClassificationBadge.tsx
│   │   │   ├── ConfidenceScore.tsx
│   │   │   ├── ExplanationsList.tsx
│   │   │   └── FeedbackForm.tsx
│   │   └── providers/
│   │       └── ThemeProvider.tsx
│   ├── hooks/                 # Custom React hooks
│   │   ├── useClassification.ts
│   │   └── useFeedback.ts
│   ├── services/              # API services
│   │   └── api.ts
│   ├── types/                 # TypeScript types
│   │   └── index.ts
│   ├── utils/                 # Utility functions
│   │   └── validation.ts
│   └── data/                  # Mock data
│       └── mockData.ts
├── public/                    # Static files
├── package.json               # Node dependencies
├── next.config.js             # Next.js configuration
├── tsconfig.json              # TypeScript configuration
├── tailwind.config.ts         # Tailwind configuration
├── fix-swc-binary.bat         # Fix SWC binary
├── fix-swc-binary.ps1         # PowerShell version
└── switch-to-babel.bat        # Switch to Babel compiler
```

---

## Other Directories

```
models/                        # Trained model weights
├── fake_product_classifier.keras

data/                          # Training and test datasets
├── train/
│   ├── original/
│   └── fake/
└── test/
    ├── original/
    └── fake/

tests/                         # Property-based tests
├── test_property_*.py         # 17+ test files

logs/                          # Application logs
temp_uploads/                  # Temporary file uploads
```

---

## Quick Reference

| Need | Location |
|------|----------|
| Start system | `start-both.bat` (root) |
| Quick start guide | `SYSTEM_WORKING_NOW.md` (root) |
| Setup help | `guides/setup/QUICK_START.md` |
| Training guide | `guides/training/HOW_TO_TRAIN_MODEL.md` |
| Fix backend | `guides/troubleshooting/FIX_BACKEND_IMPORT_ERROR.md` |
| Fix frontend | `guides/troubleshooting/FINAL_FIX_GUIDE.md` |
| All docs | `guides/DOCUMENTATION_INDEX.md` |
| Test database | `scripts/utilities/test_db_connection.py` |
| Train model | `train.py` (root) |

---

## Benefits of This Structure

✅ **Clean Root**: Only essential files in root directory  
✅ **Organized Docs**: All guides categorized by purpose  
✅ **Easy Navigation**: Clear folder structure  
✅ **Quick Access**: Main startup script in root  
✅ **Logical Grouping**: Related files together  
✅ **Scalable**: Easy to add new docs/scripts  

---

**Everything is organized and ready to use!** 🎉
