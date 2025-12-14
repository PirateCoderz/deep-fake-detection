# 🚀 START HERE - Fake Product Detection System

## Quick Start (2 Terminals)

### Terminal 1: Backend (WITH Python venv)

```bash
# Activate virtual environment
.venv\Scripts\activate

# Start FastAPI backend
python run_backend.py
```

**Note**: The `run_backend.py` wrapper handles Python paths automatically

✅ Backend running at: **http://localhost:8000**

---

### Terminal 2: Frontend (WITHOUT Python venv)

**Option A: Using Batch Script (Recommended)**
```bash
frontend\run-frontend.bat
```

**Option B: Using PowerShell Script**
```powershell
cd frontend
.\run-frontend.ps1
```

**Option C: Manual**
```bash
cd frontend
npm run dev
```

✅ Frontend running at: **http://localhost:3000**

---

## ⚠️ IMPORTANT: SWC Binary Issue

The frontend **MUST** run in a terminal **WITHOUT** Python venv activated.

**Why?** The Next.js SWC binary conflicts with Python's virtual environment on Windows.

**Solution:**
1. Keep backend running in Terminal 1 (with venv)
2. Open a **NEW** terminal for frontend (without venv)
3. Run `frontend\run-frontend.bat`

---

## 🧪 Test the System

1. Open http://localhost:3000
2. Upload a product image
3. View classification results
4. Check confidence score and explanations
5. Submit feedback

---

## 📋 Prerequisites Checklist

- [x] Python 3.8+ installed
- [x] Node.js 18+ installed
- [x] PostgreSQL running
- [x] Database `fakedetect` created
- [x] Backend dependencies installed: `pip install -r backend/requirements.txt`
- [x] Frontend dependencies installed: `npm install` (in frontend/)
- [x] Trained model exists: `models/fake_product_classifier.keras`

---

## 🔧 First Time Setup

### 1. Database Setup
```bash
# Test database connection
python test_db_connection.py
```

See: `DATABASE_SETUP_GUIDE.md` for detailed instructions

### 2. Backend Setup
```bash
# Activate venv
.venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Test backend
python backend/src/main.py
```

### 3. Frontend Setup
```bash
# Navigate to frontend (WITHOUT venv)
cd frontend

# Install dependencies
npm install

# Create environment file
copy .env.local.example .env.local

# Start frontend
npm run dev
```

---

## 📊 System Architecture

```
┌─────────────────┐
│   Browser       │
│  (Port 3000)    │
└────────┬────────┘
         │
         │ HTTP Requests
         ▼
┌─────────────────┐
│  Next.js        │
│  Frontend       │
└────────┬────────┘
         │
         │ API Calls
         ▼
┌─────────────────┐      ┌──────────────┐
│  FastAPI        │─────▶│  PostgreSQL  │
│  Backend        │      │  Database    │
│  (Port 8000)    │      └──────────────┘
└────────┬────────┘
         │
         │ Model Inference
         ▼
┌─────────────────┐
│  ResNet50 CNN   │
│  Classifier     │
└─────────────────┘
```

---

## 🎯 Current Status

### ✅ Completed
- Backend API (Tasks 9-11)
- Frontend UI (Task 12)
- Database integration
- Classification pipeline
- Explainability module
- Logging & metrics services

### ⚠️ Needs Improvement
- Model accuracy (only 20 training images)
- Add 100-500+ images per class
- Retrain model: `python train.py`

### 📝 Optional
- Frontend tests (Tasks 12.3, 12.6, 12.8, 12.10)
- Security measures (Task 13)
- Docker deployment (Task 14)
- API documentation (Task 16)

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| `QUICK_START.md` | Quick start guide with troubleshooting |
| `DATABASE_SETUP_GUIDE.md` | PostgreSQL setup instructions |
| `FRONTEND_SETUP_GUIDE.md` | Frontend installation guide |
| `HOW_TO_TRAIN_MODEL.md` | Model training instructions |
| `HOW_TO_ADD_REAL_IMAGES.md` | Adding training data |
| `TESTING_COMPLETE_GUIDE.md` | Testing guide |
| `FINAL_BACKEND_STATUS.md` | Backend implementation status |
| `12_FRONTEND_COMPLETE.md` | Frontend implementation status |

---

## 🆘 Troubleshooting

### Backend Won't Start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Install missing dependencies
pip install -r backend/requirements.txt

# Check database connection
python test_db_connection.py
```

### Frontend SWC Error
```bash
# Make sure you're NOT in venv
# Open NEW terminal and run:
frontend\run-frontend.bat
```

### Database Connection Error
```bash
# Start PostgreSQL service
# Create database in pgAdmin
# Update .env file with correct credentials
```

### Model Not Found
```bash
# Train a new model
python train.py

# Or use demo mode (mock predictions)
# Edit backend/src/main.py to use mock classifier
```

---

## 🎉 You're Ready!

1. Start backend in Terminal 1 (with venv)
2. Start frontend in Terminal 2 (without venv)
3. Open http://localhost:3000
4. Upload an image
5. Get instant results!

---

**Need help?** Check `QUICK_START.md` for detailed troubleshooting.
