# 🚀 START THE SYSTEM NOW - Complete Guide

## ✅ All Issues Fixed!

Both backend and frontend issues have been resolved:
- ✅ Backend import error → Fixed with `run_backend.py` wrapper
- ✅ Frontend SWC error → Fixed with `fix-swc-binary.bat`

---

## 🎯 THE EASIEST WAY (1 Click)

**Just double-click this file:**
```
start-both.bat
```

This will:
1. Open Terminal 1 with backend (with venv) ✅
2. Open Terminal 2 with frontend (without venv) ✅
3. Start both services automatically ✅

**Wait 10-15 seconds**, then open: **http://localhost:3000**

---

## 📋 Manual Way (If You Prefer)

### Terminal 1: Backend

```bash
# Navigate to project
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

# Fix SWC binary (run once)
fix-swc-binary.bat

# Start frontend
npm run dev
```

**✅ Success**: You'll see `✓ Ready in 2.5s`

---

## 🎉 What to Do After Starting

1. **Open browser**: http://localhost:3000
2. **Upload image**: Drag & drop a product image
3. **View results**: See classification (Original/Fake)
4. **Check confidence**: View confidence score
5. **Read explanations**: See why it was classified that way
6. **Submit feedback**: Click correct/incorrect

---

## 🔍 Verify Everything is Working

### Check Backend:
- Open: http://localhost:8000/api/v1/health
- Should see: `{"status":"healthy"}`

### Check API Docs:
- Open: http://localhost:8000/docs
- Should see: Interactive API documentation

### Check Frontend:
- Open: http://localhost:3000
- Should see: Upload page with drag & drop area

---

## ⚠️ If You Still Have Issues

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'src'`
**Fix**: Use `python run_backend.py` instead of `python backend/src/main.py`
**Guide**: `BACKEND_FIXED.md`

---

### Frontend Won't Start

**Error**: `Failed to load SWC binary`
**Fix**: Run `cd frontend && fix-swc-binary.bat`
**Guide**: `FINAL_FIX_GUIDE.md`

---

### Database Connection Error

**Error**: `could not connect to server`
**Fix**: 
1. Start PostgreSQL service
2. Create database in pgAdmin: `fakedetect`
3. Test: `python test_db_connection.py`
**Guide**: `DATABASE_SETUP_GUIDE.md`

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Browser                            │
│                 http://localhost:3000                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP Requests
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Next.js Frontend                       │
│                  (Terminal 2 - no venv)                 │
│                  Port 3000                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ API Calls
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                        │
│                  (Terminal 1 - with venv)               │
│                  Port 8000                              │
└────────┬───────────┴────────────┬───────────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌─────────────────┐
│   PostgreSQL    │      │  ResNet50 CNN   │
│   Database      │      │  Classifier     │
└─────────────────┘      └─────────────────┘
```

---

## 🎯 Quick Command Reference

| Task | Command |
|------|---------|
| Start both | `start-both.bat` |
| Start backend only | `python run_backend.py` |
| Start frontend only | `cd frontend && npm run dev` |
| Fix SWC binary | `cd frontend && fix-swc-binary.bat` |
| Test database | `python test_db_connection.py` |
| Run tests | `python run_all_tests.py` |
| Train model | `python train.py` |

---

## 📚 Documentation Index

| Guide | Purpose |
|-------|---------|
| `START_SYSTEM_NOW.md` | This file - complete startup guide |
| `RUN_NOW.md` | Quick reference |
| `BACKEND_FIXED.md` | Backend import fix details |
| `FINAL_FIX_GUIDE.md` | Frontend SWC fix details |
| `QUICK_START.md` | Detailed quick start |
| `RUN_SYSTEM.md` | Visual step-by-step guide |

---

## ✅ Pre-Flight Checklist

Before starting, make sure:
- [ ] PostgreSQL is running
- [ ] Database `fakedetect` exists
- [ ] Python venv is created (`.venv/`)
- [ ] Backend dependencies installed (`pip install -r backend/requirements.txt`)
- [ ] Frontend dependencies installed (`npm install` in frontend/)
- [ ] You're in the project root directory

---

## 🎉 You're Ready!

Everything is fixed and ready to go. Just run:

```bash
start-both.bat
```

Or manually start backend and frontend in separate terminals.

**Then open**: http://localhost:3000

---

## 🆘 Need Help?

- **Backend issues**: `BACKEND_FIXED.md`
- **Frontend issues**: `FINAL_FIX_GUIDE.md`
- **Database issues**: `DATABASE_SETUP_GUIDE.md`
- **General help**: `QUICK_START.md`
- **Complete docs**: `DOCUMENTATION_INDEX.md`

---

**Let's run it!** 🚀

**Time to start**: 10-15 seconds
**Time to first result**: 30 seconds after upload

**Your fake product detection system is ready!**
