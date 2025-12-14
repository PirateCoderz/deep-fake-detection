# Troubleshooting SWC Binary Error

## The Problem

```
⚠ Attempted to load @next/swc-win32-x64-msvc, but an error occurred
⨯ Failed to load SWC binary for win32/x64
```

This error occurs when Next.js tries to load the SWC binary while Python's virtual environment is active on Windows.

---

## Solution 1: Close Terminal and Open New One (RECOMMENDED)

### Step-by-Step:

1. **Close the current terminal completely** (X button or `exit`)

2. **Open a NEW PowerShell or Command Prompt**
   - Press `Win + R`
   - Type `powershell` or `cmd`
   - Press Enter

3. **Navigate to frontend directory**
   ```bash
   cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend
   ```

4. **Verify you're NOT in venv**
   - Your prompt should NOT show `(.venv)` at the start
   - Should look like: `PS G:\Github\...\frontend>`
   - NOT like: `(.venv) PS G:\Github\...\frontend>`

5. **Run the frontend**
   ```bash
   npm run dev
   ```

---

## Solution 2: Deactivate venv in Current Terminal

If you want to use the same terminal:

### For PowerShell:
```powershell
# Deactivate venv
deactivate

# Navigate to frontend
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend

# Run frontend
npm run dev
```

### For Command Prompt:
```cmd
# Deactivate venv
deactivate

# Navigate to frontend
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend

# Run frontend
npm run dev
```

---

## Solution 3: Use the Batch Script

The batch script will warn you if venv is active:

```bash
cd G:\Github\Pirate-Coderz\deep-fake-detection
frontend\run-frontend.bat
```

If you see a warning about venv, follow the instructions to open a new terminal.

---

## Solution 4: Delete and Reinstall SWC Binary

If the above doesn't work, the binary might be corrupted:

```bash
# Navigate to frontend
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend

# Delete node_modules and lock file
rmdir /s /q node_modules
del package-lock.json

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
npm install

# Try running again
npm run dev
```

---

## Solution 5: Use Alternative Compiler

If SWC continues to fail, you can disable it and use Babel instead:

1. Create `frontend/.babelrc`:
```json
{
  "presets": ["next/babel"]
}
```

2. Update `frontend/next.config.js`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: false,  // Disable SWC minification
}

module.exports = nextConfig
```

3. Run again:
```bash
npm run dev
```

---

## How to Verify You're NOT in venv

### Check 1: Look at your prompt
```
✅ GOOD:  PS G:\Github\Pirate-Coderz\deep-fake-detection\frontend>
❌ BAD:   (.venv) PS G:\Github\Pirate-Coderz\deep-fake-detection\frontend>
```

### Check 2: Check environment variable
```powershell
# PowerShell
echo $env:VIRTUAL_ENV

# Should output nothing or empty
# If it shows a path, you're in venv
```

```cmd
# Command Prompt
echo %VIRTUAL_ENV%

# Should output %VIRTUAL_ENV% (literally)
# If it shows a path, you're in venv
```

---

## Why This Happens

The SWC binary is a native Node.js addon compiled for Windows. When Python's virtual environment is active, it modifies system paths and environment variables that can interfere with how Node.js loads native modules.

**The fix**: Run Node.js/npm in a clean environment without Python venv.

---

## Quick Reference

| Symptom | Solution |
|---------|----------|
| Prompt shows `(.venv)` | Close terminal, open new one |
| `$env:VIRTUAL_ENV` has value | Run `deactivate` |
| Still failing after deactivate | Close terminal, open new one |
| Binary corrupted | Delete node_modules, reinstall |
| Nothing works | Use Babel instead (Solution 5) |

---

## The Correct Workflow

### Terminal 1: Backend (WITH venv)
```bash
cd G:\Github\Pirate-Coderz\deep-fake-detection
.venv\Scripts\activate
python backend/src/main.py
```
✅ Keep this terminal open with venv active

### Terminal 2: Frontend (WITHOUT venv)
```bash
# Open NEW terminal (no venv!)
cd G:\Github\Pirate-Coderz\deep-fake-detection\frontend
npm run dev
```
✅ This terminal should NOT have venv

---

## Still Having Issues?

1. **Check Node.js version**
   ```bash
   node --version
   # Should be 18.x or higher
   ```

2. **Check npm version**
   ```bash
   npm --version
   # Should be 9.x or higher
   ```

3. **Try running as administrator**
   - Right-click PowerShell/CMD
   - Select "Run as administrator"
   - Navigate to frontend directory
   - Run `npm run dev`

4. **Check antivirus**
   - Some antivirus software blocks native modules
   - Try temporarily disabling antivirus
   - Or add exception for node_modules folder

---

## Success Indicators

When it works, you should see:

```
▲ Next.js 14.2.35
- Local:        http://localhost:3000
- Environments: .env.local

✓ Starting...
✓ Ready in 2.5s
```

No warnings about SWC binary!

---

**Bottom line**: Open a NEW terminal without Python venv, then run `npm run dev`.
