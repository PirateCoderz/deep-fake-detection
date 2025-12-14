# 🚀 RUN THE SYSTEM RIGHT NOW

## The Easiest Way (1 Click)

**Just double-click this file:**
```
start-both.bat
```

This will automatically:
1. Open Terminal 1 with backend (with venv)
2. Open Terminal 2 with frontend (without venv)
3. Start both services

**Wait 10-15 seconds**, then open: **http://localhost:3000**

---

## Manual Way (2 Terminals)

### Terminal 1: Backend

```bash
# Navigate to project directory
cd G:\Github\Pirate-Coderz\deep-fake-detection

# Activate venv
.venv\Scripts\activate

# Start backend
python run_backend.py
```

**✅ Success**: You'll see `Uvicorn running on http://0.0.0.0:8000`

---

### Terminal 2: Frontend

**Open a NEW terminal (no venv!)**

```bash
# Navigate to frontend
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend

# Fix SWC binary (if needed)
fix-swc-binary.bat

# Start frontend
npm run dev
```

**✅ Success**: You'll see `✓ Ready in 2.5s`

---

## Common Errors & Quick Fixes

### Error 1: "No module named 'src'"

**Problem**: You're in the backend/ directory
**Fix**: Go back to project root
```bash
cd ..
python backend/src/main.py
```
**Guide**: `FIX_BACKEND_IMPORT_ERROR.md`

---

### Error 2: "Failed to load SWC binary"

**Problem**: SWC binary is corrupted
**Fix**: Run the fix script
```bash
cd frontend
fix-swc-binary.bat
npm run dev
```
**Guide**: `FINAL_FIX_GUIDE.md`

---

### Error 3: "No module named 'fastapi'"

**Problem**: Dependencies not installed
**Fix**: Install dependencies
```bash
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

---

### Error 4: "Database connection error"

**Problem**: PostgreSQL not running or database not created
**Fix**: Start PostgreSQL and create database
```bash
# In pgAdmin: Create database 'fakedetect'
python test_db_connection.py
```
**Guide**: `DATABASE_SETUP_GUIDE.md`

---

## ✅ Success Indicators

### Backend Success:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup...
INFO:     Application startup complete.
```

### Frontend Success:
```
▲ Next.js 14.0.4
- Local:        http://localhost:3000

✓ Starting...
✓ Ready in 2.5s
```

---

## 🎯 What to Do After Starting

1. **Open browser**: http://localhost:3000
2. **Upload image**: Drag & drop or click to browse
3. **View results**: See classification, confidence, explanations
4. **Submit feedback**: Click correct/incorrect
5. **Check API docs**: http://localhost:8000/docs

---

## 🛑 How to Stop

### Stop Backend (Terminal 1):
Press `Ctrl + C`

### Stop Frontend (Terminal 2):
Press `Ctrl + C`

### Or:
Just close both terminal windows

---

## 📚 Need More Help?

- **Backend import error**: `FIX_BACKEND_IMPORT_ERROR.md`
- **Frontend SWC error**: `FINAL_FIX_GUIDE.md`
- **Complete guide**: `RUN_SYSTEM.md`
- **Quick start**: `QUICK_START.md`

---

## 🎉 Summary

**Easiest**: Double-click `start-both.bat`
**Manual**: 2 terminals, run from correct directories
**Time**: 10-15 seconds to start

**Then open**: http://localhost:3000

---

**Let's run it!** 🚀
