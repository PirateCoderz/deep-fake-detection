# 🚀 How to Run the System

## Visual Step-by-Step Guide

### 📋 Prerequisites Check

Before starting, make sure you have:
- ✅ PostgreSQL running
- ✅ Database `fakedetect` created
- ✅ Python venv created (`.venv/`)
- ✅ Backend dependencies installed
- ✅ Frontend dependencies installed (`frontend/node_modules/`)

---

## 🎬 Running the System

### Terminal 1: Backend Server

```
┌─────────────────────────────────────────────────────────┐
│ Terminal 1 - Backend (WITH Python venv)                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  G:\Github\Pirate-Coderz\deep-fake-detection>         │
│  .venv\Scripts\activate                                │
│                                                         │
│  (.venv) G:\...\deep-fake-detection>                   │
│  python backend/src/main.py                            │
│                                                         │
│  INFO:     Started server process [12345]              │
│  INFO:     Waiting for application startup...          │
│  INFO:     Application startup complete.               │
│  INFO:     Uvicorn running on http://0.0.0.0:8000     │
│                                                         │
│  ✅ Backend is running!                                │
│  📡 API: http://localhost:8000                         │
│  📚 Docs: http://localhost:8000/docs                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Commands:**
```bash
# Navigate to project directory
cd G:\Github\Pirate-Coderz\deep-fake-detection

# Activate venv
.venv\Scripts\activate

# Start backend
python run_backend.py
```

---

### Terminal 2: Frontend Server

```
┌─────────────────────────────────────────────────────────┐
│ Terminal 2 - Frontend (WITHOUT Python venv)            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  G:\Github\Pirate-Coderz\deep-fake-detection>         │
│  frontend\run-frontend.bat                             │
│                                                         │
│  ========================================               │
│  Starting Next.js Frontend                             │
│  ========================================               │
│                                                         │
│  Starting development server...                        │
│                                                         │
│  ▲ Next.js 14.2.35                                     │
│  - Local:        http://localhost:3000                 │
│  - Environments: .env.local                            │
│                                                         │
│  ✓ Starting...                                         │
│  ✓ Ready in 2.5s                                       │
│                                                         │
│  ✅ Frontend is running!                               │
│  🌐 App: http://localhost:3000                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**Commands:**
```bash
# Open NEW terminal (DO NOT activate venv!)
cd G:\Github\Pirate-Coderz\deep-fake-detection

# Run frontend script
frontend\run-frontend.bat
```

---

### Browser: Access Application

```
┌─────────────────────────────────────────────────────────┐
│ Browser - Chrome/Firefox/Edge                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🌐 http://localhost:3000                              │
│                                                         │
│  ┌───────────────────────────────────────────────┐    │
│  │  Fake Product Detection                       │    │
│  │                                                │    │
│  │  ┌─────────────────────────────────────────┐ │    │
│  │  │                                          │ │    │
│  │  │   📁 Drag & drop image here             │ │    │
│  │  │      or click to browse                  │ │    │
│  │  │                                          │ │    │
│  │  └─────────────────────────────────────────┘ │    │
│  │                                                │    │
│  │  Supported: JPEG, PNG, HEIC (max 10MB)       │    │
│  │                                                │    │
│  └───────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

**URL:** http://localhost:3000

---

## 🧪 Testing the System

### 1. Upload Image

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Upload Product Image                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  1. Drag image file to upload area                     │
│     OR                                                  │
│  2. Click upload area to browse files                  │
│                                                         │
│  ✅ Accepted: .jpg, .jpeg, .png, .heic                 │
│  ✅ Max size: 10 MB                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 2. View Results

```
┌─────────────────────────────────────────────────────────┐
│ Step 2: Classification Results                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Classification: 🟢 ORIGINAL  or  🔴 FAKE              │
│                                                         │
│  Confidence: ████████░░ 85%                            │
│                                                         │
│  Explanations:                                         │
│  • Logo clarity is high                                │
│  • Text alignment is consistent                        │
│  • Color distribution matches authentic products       │
│                                                         │
│  [Heatmap showing focus areas]                         │
│                                                         │
│  Was this classification correct?                      │
│  [✓ Correct]  [✗ Incorrect]                           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 3. Submit Feedback

```
┌─────────────────────────────────────────────────────────┐
│ Step 3: User Feedback (Optional)                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Click "Correct" or "Incorrect" button                 │
│                                                         │
│  Optional: Add comments                                │
│  ┌─────────────────────────────────────────────────┐  │
│  │ The logo looks slightly different...            │  │
│  └─────────────────────────────────────────────────┘  │
│                                                         │
│  [Submit Feedback]                                     │
│                                                         │
│  ✅ Feedback helps improve the model!                  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 Monitoring

### Backend Logs (Terminal 1)

```
INFO:     127.0.0.1:52341 - "POST /api/v1/classify HTTP/1.1" 200 OK
INFO:     Request ID: abc123 | Duration: 1.23s
INFO:     Classification: ORIGINAL | Confidence: 85.3%
```

### Frontend Logs (Terminal 2)

```
✓ Compiled /api/classify in 234ms
✓ Compiled /results/[id] in 156ms
```

### Database (pgAdmin)

```sql
-- Check recent classifications
SELECT * FROM classifications 
ORDER BY created_at DESC 
LIMIT 10;

-- Check feedback
SELECT * FROM feedback 
WHERE is_correct = false;

-- Check daily metrics
SELECT * FROM daily_metrics 
ORDER BY date DESC;
```

---

## 🛑 Stopping the System

### Stop Frontend (Terminal 2)
```
Press: Ctrl + C

Stopping development server...
✓ Stopped
```

### Stop Backend (Terminal 1)
```
Press: Ctrl + C

INFO:     Shutting down
INFO:     Finished server process
```

---

## ⚠️ Common Issues

### Issue 1: Frontend SWC Error

```
❌ Failed to load SWC binary for win32/x64
```

**Solution:**
```
✅ Make sure Terminal 2 does NOT have Python venv active
✅ Close terminal and open NEW one
✅ Run: frontend\run-frontend.bat
```

---

### Issue 2: Backend Module Not Found

**Error A: No module named 'fastapi'**
```
❌ ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```
✅ Activate venv: .venv\Scripts\activate
✅ Install: pip install -r backend/requirements.txt
```

**Error B: No module named 'src'**
```
❌ ModuleNotFoundError: No module named 'src'
```

**Solution:**
```
✅ You're in the wrong directory!
✅ Go to project root: cd ..
✅ Run from root: python backend/src/main.py
✅ See: FIX_BACKEND_IMPORT_ERROR.md
```

---

### Issue 3: Database Connection Error

```
❌ could not connect to server
```

**Solution:**
```
✅ Start PostgreSQL service
✅ Create database in pgAdmin: fakedetect
✅ Test: python test_db_connection.py
```

---

### Issue 4: Port Already in Use

```
❌ Error: listen EADDRINUSE: address already in use :::3000
```

**Solution:**
```
# Find process using port
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F

# Or use different port
set PORT=3001
npm run dev
```

---

## 📊 System Health Check

### Quick Health Check

```bash
# Backend health
curl http://localhost:8000/api/v1/health

# Expected response:
{
  "status": "healthy",
  "model_loaded": true,
  "database_connected": true
}
```

### Full System Test

```bash
# Activate venv
.venv\Scripts\activate

# Run all tests
python run_all_tests.py

# Test specific component
python test_trained_model.py
python test_db_connection.py
```

---

## 🎯 Quick Reference

| Component | URL | Status Check |
|-----------|-----|--------------|
| Frontend | http://localhost:3000 | Open in browser |
| Backend API | http://localhost:8000 | http://localhost:8000/api/v1/health |
| API Docs | http://localhost:8000/docs | Open in browser |
| Database | localhost:5432 | `python test_db_connection.py` |

---

## 📚 More Help

- **Quick Start**: `START_HERE.md`
- **Troubleshooting**: `QUICK_START.md`
- **System Status**: `SYSTEM_READY.md`
- **Training**: `HOW_TO_TRAIN_MODEL.md`
- **Testing**: `TESTING_COMPLETE_GUIDE.md`

---

**Ready to go!** 🚀

1. Start backend (Terminal 1 with venv)
2. Start frontend (Terminal 2 without venv)
3. Open http://localhost:3000
4. Upload image
5. Get results!
