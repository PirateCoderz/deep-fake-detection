# Complete Installation Guide
## Fake Product Detection System - Setup Without Environment Files

This guide will walk you through installing the frontend, backend, and database from scratch without using `.env` files.

---

## 📋 Prerequisites

Before starting, ensure you have:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **PostgreSQL 14+** - [Download](https://www.postgresql.org/download/)
- **Git** (optional) - [Download](https://git-scm.com/)

---

## 🗄️ Part 1: Database Setup

### Step 1: Install PostgreSQL

1. Download and install PostgreSQL from the official website
2. During installation, remember your **postgres user password**
3. Default port is **5432** (keep this unless you have conflicts)

### Step 2: Start PostgreSQL Service

**Windows:**
```cmd
# Check if PostgreSQL is running
sc query postgresql-x64-14

# Start if not running
net start postgresql-x64-14
```

**Alternative:** Use pgAdmin or Services app to start PostgreSQL

### Step 3: Create Database

**Option A: Using psql command line**
```cmd
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE fakedetect;

# Verify
\l

# Exit
\q
```

**Option B: Using pgAdmin**
1. Open pgAdmin
2. Right-click "Databases" → "Create" → "Database"
3. Name: `fakedetect`
4. Click "Save"

### Step 4: Test Database Connection

```cmd
# Test connection (replace password if different)
psql -U postgres -d fakedetect -c "SELECT version();"
```

**Database Configuration:**
- Host: `localhost`
- Port: `5432`
- Database: `fakedetect`
- Username: `postgres`
- Password: `123123` (or your chosen password)

---

## 🐍 Part 2: Backend Setup

### Choose Your Setup Method

**Option A: With Virtual Environment (Recommended)**
- Isolated dependencies
- No conflicts with other Python projects
- Easy to clean up

**Option B: Without Virtual Environment (Global Installation)**
- Simpler setup
- Dependencies installed system-wide
- May conflict with other projects

---

### Option A: Backend Setup WITH Virtual Environment

#### Step 1: Navigate to Project Directory

```cmd
cd path\to\fake-product-detection
```

#### Step 2: Create Python Virtual Environment

```cmd
# Create virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Verify activation (should show .venv path)
where python
```

#### Step 3: Install Backend Dependencies

```cmd
# Install all required packages
pip install -r backend\requirements.txt

# Verify installation
pip list
```

**Key packages installed:**
- FastAPI (web framework)
- TensorFlow (machine learning)
- SQLAlchemy (database ORM)
- OpenCV (image processing)
- Redis (caching)
- Pytest (testing)

#### Step 4: Configure Database Connection

Edit `backend/src/config.py` and update the database URL:

```python
# Find this line and update with your database credentials
DATABASE_URL = "postgresql://postgres:123123@localhost:5432/fakedetect"
```

**Format:** `postgresql://username:password@host:port/database`

#### Step 5: Initialize Database Schema

```cmd
# Still in activated venv
cd backend

# Run Alembic migrations
alembic upgrade head

# Go back to root
cd ..
```

#### Step 6: Test Backend Connection

```cmd
# Test database connection
python scripts\utilities\test_db_connection.py

# Should output: "✅ Database connection successful!"
```

#### Step 7: Start Backend Server

**Option A: Using startup script**
```cmd
python scripts\utilities\run_backend.py
```

**Option B: Direct uvicorn**
```cmd
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify Backend:**
- Open browser: http://localhost:8000/docs
- You should see the FastAPI Swagger documentation
- Try the `/api/v1/health` endpoint

---

### Option B: Backend Setup WITHOUT Virtual Environment

#### Step 1: Navigate to Project Directory

```cmd
cd path\to\fake-product-detection
```

#### Step 2: Install Backend Dependencies Globally

```cmd
# Install all required packages to your system Python
pip install -r backend\requirements.txt

# Verify installation
pip list | findstr fastapi
pip list | findstr tensorflow
```

**⚠️ Warning:** This installs packages globally and may:
- Conflict with other Python projects
- Require administrator privileges
- Be harder to uninstall cleanly

**Key packages installed:**
- FastAPI (web framework)
- TensorFlow (machine learning)
- SQLAlchemy (database ORM)
- OpenCV (image processing)
- Redis (caching)
- Pytest (testing)

#### Step 3: Configure Database Connection

Edit `backend/src/config.py` and update the database URL:

```python
# Find this line and update with your database credentials
DATABASE_URL = "postgresql://postgres:123123@localhost:5432/fakedetect"
```

**Format:** `postgresql://username:password@host:port/database`

#### Step 4: Initialize Database Schema

```cmd
cd backend

# Run Alembic migrations
alembic upgrade head

# Go back to root
cd ..
```

#### Step 5: Test Backend Connection

```cmd
# Test database connection (no venv activation needed)
python scripts\utilities\test_db_connection.py

# Should output: "✅ Database connection successful!"
```

#### Step 6: Start Backend Server

**Option A: Using startup script**
```cmd
python scripts\utilities\run_backend.py
```

**Option B: Direct uvicorn**
```cmd
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Option C: Using Python directly**
```cmd
python -m uvicorn backend.src.main:app --reload --host 0.0.0.0 --port 8000
```

**Verify Backend:**
- Open browser: http://localhost:8000/docs
- You should see the FastAPI Swagger documentation
- Try the `/api/v1/health` endpoint

---

### Comparison: With vs Without Virtual Environment

| Feature | With venv | Without venv |
|---------|-----------|--------------|
| Setup complexity | Medium | Simple |
| Isolation | ✅ Isolated | ❌ Global |
| Conflicts | ✅ No conflicts | ⚠️ May conflict |
| Cleanup | ✅ Easy (delete folder) | ❌ Hard (manual uninstall) |
| Best for | Development, multiple projects | Single project, testing |
| Recommended | ✅ Yes | ⚠️ Only if needed |

---

## ⚛️ Part 3: Frontend Setup

### Step 1: Open NEW Terminal (Important!)

**DO NOT use the terminal with Python venv activated**

Open a fresh Command Prompt or PowerShell window.

### Step 2: Navigate to Frontend Directory

```cmd
cd path\to\fake-product-detection\frontend
```

### Step 3: Install Node Dependencies

```cmd
# Install all packages
npm install

# This will take 2-5 minutes
```

**Key packages installed:**
- Next.js 14 (React framework)
- Material-UI (UI components)
- Axios (HTTP client)
- React Dropzone (file upload)
- TypeScript (type safety)

### Step 4: Fix SWC Binary (Windows Only)

```cmd
# Run the fix script
fix-swc-binary.bat

# Or manually:
npm install @next/swc-win32-x64-msvc@14.0.4
```

### Step 5: Configure API URL

Edit `frontend/src/services/api.ts`:

```typescript
// Find this line and update if needed
const API_BASE_URL = 'http://localhost:8000';
```

### Step 6: Start Frontend Development Server

```cmd
npm run dev
```

**Verify Frontend:**
- Open browser: http://localhost:3000
- You should see the Fake Product Detection homepage
- Try uploading an image

---

## 🚀 Part 4: Running the Complete System

### Method 1: Manual Start - WITH Virtual Environment

**Terminal 1 - Backend:**
```cmd
cd path\to\fake-product-detection
.venv\Scripts\activate
python scripts\utilities\run_backend.py
```

**Terminal 2 - Frontend:**
```cmd
cd path\to\fake-product-detection\frontend
npm run dev
```

### Method 2: Manual Start - WITHOUT Virtual Environment

**Terminal 1 - Backend:**
```cmd
cd path\to\fake-product-detection
python scripts\utilities\run_backend.py
```

**Terminal 2 - Frontend:**
```cmd
cd path\to\fake-product-detection\frontend
npm run dev
```

### Method 3: One-Click Start (Automated)

**If using virtual environment:**
```cmd
# From project root
start-both.bat
```

**If NOT using virtual environment:**

You'll need to modify `start-both.bat` to skip venv activation. Create a new file `start-both-no-venv.bat`:

```batch
@echo off
echo Starting Fake Product Detection System (No Virtual Environment)...
echo.

REM Start Backend
echo Starting Backend...
start "Backend Server" cmd /k "cd /d %~dp0 && python scripts\utilities\run_backend.py"

REM Wait for backend to start
timeout /t 10 /nobreak

REM Start Frontend
echo Starting Frontend...
start "Frontend Server" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo System is starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window (servers will keep running)
pause
```

Then run:
```cmd
start-both-no-venv.bat
```

---

## 🧪 Part 5: Verify Installation

### Test 1: Health Check

```cmd
# In browser or curl
curl http://localhost:8000/api/v1/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "model": "loaded"
}
```

### Test 2: Upload Test Image

1. Go to http://localhost:3000
2. Drag and drop an image from `data/test/original/` or `data/test/fake/`
3. Click "Analyze Image"
4. Should see classification result with confidence score

### Test 3: Run Test Suite

**With virtual environment:**
```cmd
# Activate venv
.venv\Scripts\activate

# Run all tests
python scripts\utilities\run_all_tests.py
```

**Without virtual environment:**
```cmd
# Run all tests directly
python scripts\utilities\run_all_tests.py
```

---

## 📊 Configuration Reference

### Backend Configuration (backend/src/config.py)

```python
# Database
DATABASE_URL = "postgresql://postgres:123123@localhost:5432/fakedetect"

# Redis (optional)
REDIS_URL = "redis://localhost:6379/0"

# Model
MODEL_PATH = "models/fake_detector_final.keras"
CONFIDENCE_THRESHOLD = 70

# API
CORS_ORIGINS = ["http://localhost:3000", "http://127.0.0.1:3000"]
RATE_LIMIT_PER_HOUR = 100

# Server
HOST = "0.0.0.0"
PORT = 8000
```

### Frontend Configuration (frontend/src/services/api.ts)

```typescript
const API_BASE_URL = 'http://localhost:8000';
const API_VERSION = 'v1';
const TIMEOUT = 30000; // 30 seconds
```

---

## 🔧 Troubleshooting

### Backend Issues

**Problem: "ModuleNotFoundError"**

**With venv:**
```cmd
# Solution: Reinstall dependencies
.venv\Scripts\activate
pip install -r backend\requirements.txt
```

**Without venv:**
```cmd
# Solution: Reinstall dependencies globally
pip install -r backend\requirements.txt
```

**Problem: "Database connection failed"**
```cmd
# Solution: Check PostgreSQL is running
sc query postgresql-x64-14
net start postgresql-x64-14

# Test connection
python scripts\utilities\test_db_connection.py
```

**Problem: "Model file not found"**
```cmd
# Solution: Train the model first
.venv\Scripts\activate
python train.py
```

### Frontend Issues

**Problem: "SWC binary not found"**
```cmd
# Solution: Fix SWC binary
cd frontend
fix-swc-binary.bat
```

**Problem: "Port 3000 already in use"**
```cmd
# Solution: Kill process or use different port
npx kill-port 3000
# Or
set PORT=3001 && npm run dev
```

**Problem: "Cannot connect to backend"**
- Verify backend is running on port 8000
- Check `frontend/src/services/api.ts` has correct URL
- Check CORS settings in `backend/src/main.py`

### Database Issues

**Problem: "Database does not exist"**
```cmd
# Solution: Create database
psql -U postgres -c "CREATE DATABASE fakedetect;"
```

**Problem: "Password authentication failed"**
- Update password in `backend/src/config.py`
- Format: `postgresql://postgres:YOUR_PASSWORD@localhost:5432/fakedetect`

---

## 📦 Optional: Redis Setup

Redis is optional but recommended for rate limiting and caching.

### Install Redis (Windows)

1. Download Redis from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`
3. Default port: 6379

### Configure Redis

In `backend/src/config.py`:
```python
REDIS_URL = "redis://localhost:6379/0"
```

---

## 🎓 Next Steps

### 1. Train the Model

**With venv:**
```cmd
.venv\Scripts\activate
python train.py
```

**Without venv:**
```cmd
python train.py
```

See: `guides/training/HOW_TO_TRAIN_MODEL.md`

### 2. Add More Training Data

- Add images to `data/train/original/` and `data/train/fake/`
- Minimum: 100 images per class
- Recommended: 500+ images per class

See: `guides/training/HOW_TO_ADD_REAL_IMAGES.md`

### 3. Run Tests

**With venv:**
```cmd
.venv\Scripts\activate
python scripts\utilities\run_all_tests.py
```

**Without venv:**
```cmd
python scripts\utilities\run_all_tests.py
```

See: `guides/testing/TESTING_COMPLETE_GUIDE.md`

---

## 📝 Quick Reference

### Start System

**With virtual environment:**
```cmd
# One command
start-both.bat

# Or manually
# Terminal 1: .venv\Scripts\activate && python scripts\utilities\run_backend.py
# Terminal 2: cd frontend && npm run dev
```

**Without virtual environment:**
```cmd
# One command
start-both-no-venv.bat

# Or manually
# Terminal 1: python scripts\utilities\run_backend.py
# Terminal 2: cd frontend && npm run dev
```

### Stop System
```cmd
# Press Ctrl+C in both terminals
```

### Access Points
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

### Key Files
- Backend config: `backend/src/config.py`
- Frontend API: `frontend/src/services/api.ts`
- Database schema: `backend/alembic/versions/001_initial_schema.py`

---

## ✅ Installation Complete!

Your system is now ready to use.

**With virtual environment:**
```cmd
start-both.bat
```

**Without virtual environment:**
```cmd
start-both-no-venv.bat
```

Then open: **http://localhost:3000**

For more help, see:
- `README.md` - Project overview
- `SYSTEM_WORKING_NOW.md` - Quick start guide
- `guides/DOCUMENTATION_INDEX.md` - All documentation

---

**Last Updated:** January 20, 2026
**Version:** 1.0.0
