# 🔧 Fix SWC Binary Error - Visual Guide

## The Error You're Seeing

```
⚠ Attempted to load @next/swc-win32-x64-msvc, but an error occurred
⨯ Failed to load SWC binary for win32/x64
```

---

## 🎯 The Problem

You're trying to run the frontend while Python's virtual environment is still active. This causes conflicts with Node.js native modules.

---

## ✅ Solution: 3 Easy Methods

### Method 1: Auto-Launcher (EASIEST) ⭐

Just double-click this file or run from terminal:

```bash
start-frontend-new-terminal.bat
```

This will:
1. Open a NEW terminal window
2. Navigate to frontend directory
3. Start `npm run dev` automatically
4. WITHOUT Python venv!

**That's it!** The new window will have the frontend running.

---

### Method 2: Manual - New Terminal

#### Step 1: Close Current Terminal
- Click the X button on your current terminal
- Or type `exit` and press Enter

#### Step 2: Open NEW Terminal
- Press `Win + R`
- Type `powershell` (or `cmd`)
- Press Enter

#### Step 3: Navigate to Frontend
```bash
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend
```

#### Step 4: Verify NO venv
Your prompt should look like:
```
✅ GOOD:  PS G:\Github\Pirate-Coderz\deep-fake-detection\frontend>
```

NOT like:
```
❌ BAD:   (.venv) PS G:\Github\Pirate-Coderz\deep-fake-detection\frontend>
```

#### Step 5: Start Frontend
```bash
npm run dev
```

---

### Method 3: Deactivate venv

If you want to use the same terminal:

```bash
# Deactivate Python venv
deactivate

# Navigate to frontend
cd frontend

# Start frontend
npm run dev
```

**Note:** Sometimes `deactivate` doesn't fully clean the environment. If you still get the error, use Method 1 or 2.

---

## 🎬 Visual Walkthrough

### Current Situation (ERROR):
```
┌─────────────────────────────────────────────────────────┐
│ Terminal 1 - Backend (WITH venv) ✅                     │
├─────────────────────────────────────────────────────────┤
│ (.venv) PS G:\...\deep-fake-detection>                 │
│ python backend/src/main.py                             │
│                                                         │
│ ✅ Backend running on http://localhost:8000            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Same Terminal - Trying Frontend (STILL HAS venv) ❌     │
├─────────────────────────────────────────────────────────┤
│ (.venv) PS G:\...\deep-fake-detection\frontend>       │
│ npm run dev                                            │
│                                                         │
│ ❌ Failed to load SWC binary for win32/x64            │
└─────────────────────────────────────────────────────────┘
```

### Correct Setup (WORKS):
```
┌─────────────────────────────────────────────────────────┐
│ Terminal 1 - Backend (WITH venv) ✅                     │
├─────────────────────────────────────────────────────────┤
│ (.venv) PS G:\...\deep-fake-detection>                 │
│ python backend/src/main.py                             │
│                                                         │
│ ✅ Backend running on http://localhost:8000            │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│ Terminal 2 - Frontend (NO venv) ✅                      │
├─────────────────────────────────────────────────────────┤
│ PS G:\...\deep-fake-detection\frontend>               │
│ npm run dev                                            │
│                                                         │
│ ✅ Frontend running on http://localhost:3000          │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Fix Right Now

### Option A: Use Auto-Launcher
1. Keep your current terminal open (backend is running)
2. Double-click: `start-frontend-new-terminal.bat`
3. Wait for new window to open
4. Frontend will start automatically

### Option B: Manual New Terminal
1. Keep your current terminal open (backend is running)
2. Press `Win + R`, type `powershell`, press Enter
3. Type: `cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend`
4. Type: `npm run dev`

---

## ✅ Success Indicators

When it works, you'll see:

```
▲ Next.js 14.2.35
- Local:        http://localhost:3000
- Environments: .env.local

✓ Starting...
✓ Ready in 2.5s
```

**No warnings about SWC!**

Then open: http://localhost:3000

---

## 🎯 The Correct Workflow

### Every Time You Start the System:

**Terminal 1 (Backend):**
```bash
cd G:\Github\Pirate-Coderz\deep-fake-detection
.venv\Scripts\activate
python backend/src/main.py
```
✅ Keep this open with venv

**Terminal 2 (Frontend) - NEW TERMINAL:**
```bash
# Open NEW terminal (Win + R → powershell)
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend
npm run dev
```
✅ This should NOT have venv

**Or use the auto-launcher:**
```bash
# From project root
start-frontend-new-terminal.bat
```

---

## 🔍 Troubleshooting

### Still Getting Error After New Terminal?

1. **Check if venv is really deactivated:**
   ```powershell
   echo $env:VIRTUAL_ENV
   # Should output nothing
   ```

2. **Try clearing npm cache:**
   ```bash
   npm cache clean --force
   npm install
   npm run dev
   ```

3. **Try deleting node_modules:**
   ```bash
   cd frontend
   rmdir /s /q node_modules
   npm install
   npm run dev
   ```

4. **See detailed troubleshooting:**
   - Read: `frontend/TROUBLESHOOTING_SWC.md`

---

## 📞 Need More Help?

- **Detailed SWC troubleshooting**: `frontend/TROUBLESHOOTING_SWC.md`
- **General troubleshooting**: `QUICK_START.md`
- **Visual guide**: `RUN_SYSTEM.md`

---

## 💡 Why This Happens

Python's virtual environment modifies system paths and environment variables. When Node.js tries to load native modules (like the SWC binary), these modifications can cause conflicts on Windows.

**The solution is simple**: Run Node.js in a clean environment without Python venv.

---

## 🎉 Summary

**Problem**: SWC binary error when running frontend
**Cause**: Python venv is still active
**Solution**: Run frontend in NEW terminal without venv

**Easiest fix**: Run `start-frontend-new-terminal.bat`

---

**You got this!** 🚀
