# Fix Database Password Authentication Error

## Problem
```
psycopg2.OperationalError: password authentication failed for user "postgres"
```

Your PostgreSQL database password doesn't match the one in the configuration.

---

## Solution: Choose ONE of these methods

### Method 1: Update Configuration File (Recommended)

**Step 1:** Find your actual PostgreSQL password
- Check what password you set during PostgreSQL installation
- Or reset it using Method 3 below

**Step 2:** Update `backend/src/config.py`

Open the file and change this line:
```python
database_url: str = "postgresql://postgres:123123@localhost:5432/fakedetect"
```

To (replace `YOUR_ACTUAL_PASSWORD` with your real password):
```python
database_url: str = "postgresql://postgres:YOUR_ACTUAL_PASSWORD@localhost:5432/fakedetect"
```

**Example:** If your password is `admin`, change to:
```python
database_url: str = "postgresql://postgres:admin@localhost:5432/fakedetect"
```

---

### Method 2: Use Environment Variable (No Code Changes)

**Step 1:** Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:YOUR_ACTUAL_PASSWORD@localhost:5432/fakedetect
```

**Step 2:** The config will automatically load this

---

### Method 3: Reset PostgreSQL Password

If you forgot your password, reset it:

**Step 1:** Open Command Prompt as Administrator

**Step 2:** Connect to PostgreSQL:
```cmd
psql -U postgres
```

If it asks for password and you don't know it, you need to edit `pg_hba.conf`:

**Step 3:** Find `pg_hba.conf` file:
```cmd
# Usually located at:
C:\Program Files\PostgreSQL\14\data\pg_hba.conf
# Or
C:\Program Files\PostgreSQL\15\data\pg_hba.conf
```

**Step 4:** Edit `pg_hba.conf` (as Administrator):

Find this line:
```
host    all             all             127.0.0.1/32            scram-sha-256
```

Change to:
```
host    all             all             127.0.0.1/32            trust
```

**Step 5:** Restart PostgreSQL:
```cmd
net stop postgresql-x64-14
net start postgresql-x64-14
```

**Step 6:** Now connect without password:
```cmd
psql -U postgres
```

**Step 7:** Set new password:
```sql
ALTER USER postgres WITH PASSWORD '123123';
```

**Step 8:** Change `pg_hba.conf` back to `scram-sha-256`

**Step 9:** Restart PostgreSQL again

---

### Method 4: Quick Test - Find Current Password

Try common default passwords:

```cmd
# Test with empty password
psql -U postgres -d fakedetect

# Test with 'postgres'
psql -U postgres -d fakedetect
# When prompted, enter: postgres

# Test with 'admin'
psql -U postgres -d fakedetect
# When prompted, enter: admin
```

If one works, update your config with that password.

---

## Quick Fix Script

I'll create a script to help you update the password easily.

**Step 1:** Run this command to test different passwords:
```cmd
python scripts\utilities\test_db_connection.py
```

**Step 2:** If it fails, tell me your PostgreSQL password and I'll update the config for you.

---

## After Fixing

Once you've updated the password, test the connection:

```cmd
# Test database connection
python scripts\utilities\test_db_connection.py

# If successful, start backend
python scripts\utilities\run_backend.py
```

---

## Common PostgreSQL Default Passwords

Try these common defaults:
- `postgres`
- `admin`
- `password`
- `123456`
- Empty (no password)
- `root`

---

## Need Help?

Tell me:
1. What password did you set during PostgreSQL installation?
2. Or do you want to reset it to `123123`?

I'll update the configuration for you!
