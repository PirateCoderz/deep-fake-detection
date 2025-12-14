# 🔧 Fix Backend Import Error

## The Error

```
ModuleNotFoundError: No module named 'src'
```

## The Problem

The backend imports need the correct Python path to find the `src` module.

## ✅ The Fix (EASY)

Use the wrapper script that handles paths automatically:

```bash
# Navigate to project directory
cd G:\Github\Pirate-Coderz\deep-fake-detection

# Activate venv
.venv\Scripts\activate

# Run backend using wrapper
python run_backend.py
```

The `run_backend.py` script automatically adds the backend directory to Python's path, so imports work correctly.

---

## Alternative: Use start-backend.bat

Even easier:

```bash
.venv\Scripts\activate
start-backend.bat
```

---

## 🚀 Even Easier: Use the Script

From project root:

```bash
.venv\Scripts\activate
start-backend.bat
```

This script:
- Checks if venv is active
- Ensures you're in the right directory
- Starts the backend correctly

---

## 🎯 Why This Happens

The backend code uses imports like:
```python
from src.config import settings
from src.database import get_db
```

These imports expect to be run from the **project root**, where Python can find the `src/` module inside the `backend/` directory.

When you run from `backend/`, Python looks for `backend/src/src/` which doesn't exist!

---

## ✅ Correct Workflow

### Terminal 1: Backend

```bash
# Navigate to project root
cd G:\Github\Pirate-Coderz\deep-fake-detection

# Activate venv
.venv\Scripts\activate

# Start backend
python backend/src/main.py
```

### Terminal 2: Frontend

```bash
# Open NEW terminal (no venv)
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend

# Start frontend
npm run dev
```

---

## 📝 Quick Reference

| Command | Directory | Result |
|---------|-----------|--------|
| `python backend/src/main.py` | Project root | ✅ Works |
| `python ./src/main.py` | backend/ | ❌ Error |
| `python src/main.py` | backend/ | ❌ Error |
| `start-backend.bat` | Project root | ✅ Works |

---

## 🎉 Summary

**Problem**: Running backend from wrong directory
**Solution**: Run from project root: `python backend/src/main.py`
**Easy way**: Use `start-backend.bat` script

---

**Now try again from the project root!** 🚀
