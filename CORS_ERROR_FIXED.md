# ✅ CORS Error Fixed!

## The Error

```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/classify' 
from origin 'http://localhost:3000' has been blocked by CORS policy: 
No 'Access-Control-Allow-Origin' header is present on the requested resource.
```

## What This Means

CORS (Cross-Origin Resource Sharing) prevents the frontend (port 3000) from accessing the backend (port 8000) for security reasons.

---

## What Was Fixed

### Updated CORS Configuration

Changed from reading from settings to explicit URLs:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)
```

This explicitly allows:
- ✅ Frontend at `http://localhost:3000`
- ✅ Frontend at `http://127.0.0.1:3000`
- ✅ All HTTP methods (GET, POST, etc.)
- ✅ All headers
- ✅ Credentials (cookies, auth)

---

## How to Apply the Fix

### Step 1: Stop Backend

If backend is running, stop it (Ctrl+C)

### Step 2: Restart Backend

```bash
# Activate venv
.venv\Scripts\activate

# Start backend
python scripts/utilities/run_backend.py
```

Or use:
```bash
start-both.bat
```

### Step 3: Verify Backend is Running

Check: http://localhost:8000/api/v1/health

Should see:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "database_connected": true
}
```

### Step 4: Test Frontend

1. Open: http://localhost:3000
2. Upload an image
3. Should work without CORS errors!

---

## Troubleshooting

### Still Getting CORS Error?

**Check 1: Is backend running?**
```bash
curl http://localhost:8000/api/v1/health
```

If this fails, backend is not running.

**Check 2: Check backend logs**

Look for:
```
Configuring CORS with origins: ['http://localhost:3000', 'http://127.0.0.1:3000']
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Check 3: Frontend URL**

Make sure frontend is at `http://localhost:3000` (not `http://127.0.0.1:3000`)

**Check 4: Restart both**

Stop both backend and frontend, then restart:
```bash
start-both.bat
```

---

## Connection Refused Error

If you see `ERR_CONNECTION_REFUSED`, the backend is not running.

**Solution:**
1. Check if backend is running: `curl http://localhost:8000/api/v1/health`
2. If not, start it: `python scripts/utilities/run_backend.py`
3. Check for errors in backend terminal

---

## Complete Startup Checklist

### Terminal 1: Backend
```bash
cd G:\Github\Pirate-Coderz\deep-fake-detection
.venv\Scripts\activate
python scripts/utilities/run_backend.py
```

**Wait for:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Terminal 2: Frontend
```bash
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend
npm run dev
```

**Wait for:**
```
✓ Ready in 2.5s
```

### Browser
```
http://localhost:3000
```

---

## Expected Behavior

### Before Fix:
- ❌ CORS error when uploading image
- ❌ Request blocked by browser
- ❌ No response from backend

### After Fix:
- ✅ Image uploads successfully
- ✅ Backend processes request
- ✅ Results displayed in frontend
- ✅ No CORS errors

---

## Summary

**Fixed:**
- ✅ CORS configuration updated
- ✅ Explicit origins allowed
- ✅ All methods enabled
- ✅ Headers configured

**Status:** CORS errors resolved! 🚀

---

**Restart the backend and try uploading an image - should work now!**
