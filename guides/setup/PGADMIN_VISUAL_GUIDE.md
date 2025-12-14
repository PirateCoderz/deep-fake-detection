# pgAdmin Visual Step-by-Step Guide

This is a detailed visual guide for setting up the database using pgAdmin 4.

## 📋 Prerequisites Checklist

- [ ] PostgreSQL installed
- [ ] pgAdmin 4 installed (comes with PostgreSQL)
- [ ] PostgreSQL service is running
- [ ] You know your PostgreSQL password (set during installation)

---

## Part 1: Opening pgAdmin and Connecting

### Step 1: Launch pgAdmin 4

1. **Open pgAdmin 4** from Windows Start Menu
   - Search for "pgAdmin 4"
   - Click to launch

2. **Enter Master Password** (if prompted)
   - This is the password you set when first opening pgAdmin
   - Check "Save Password" for convenience

### Step 2: Connect to PostgreSQL Server

1. In the **left sidebar (Browser panel)**, you'll see:
   ```
   Servers
   └── PostgreSQL 15 (or your version)
   ```

2. **Click on "PostgreSQL 15"** to expand it
   - You may be prompted for a password
   - Enter your PostgreSQL password (set during installation)
   - Check "Save Password" box
   - Click "OK"

3. **Verify Connection**
   - If connected, you'll see a green icon next to PostgreSQL
   - The tree will expand showing: Databases, Login/Group Roles, Tablespaces

---

## Part 2: Creating the Database

### Method A: Using Right-Click Menu (Easiest)

1. **Locate "Databases"** in the left sidebar:
   ```
   Servers
   └── PostgreSQL 15
       └── Databases (X)  ← Right-click here
   ```

2. **Right-click on "Databases"**
   - Select **"Create"** → **"Database..."**

3. **Fill in the Create Database Dialog**:
   
   **General Tab:**
   - **Database**: `fakedetect`
   - **Owner**: `postgres` (default)
   - **Comment**: `Fake Product Detection System Database` (optional)
   
   **Definition Tab** (optional, defaults are fine):
   - **Encoding**: `UTF8`
   - **Template**: `template0`
   - **Collation**: `Default`
   - **Character type**: `Default`
   
   **Security Tab**: (leave as default)
   
   **Parameters Tab**: (leave as default)

4. **Click "Save"** button at bottom right

5. **Verify Creation**:
   - Expand "Databases" in left sidebar
   - You should see "fakedetect" in the list
   - It will show: `fakedetect (postgres)`

### Method B: Using SQL Query

1. **Open Query Tool**:
   - Right-click on **"PostgreSQL 15"** server
   - Select **"Query Tool"**
   - A new tab opens with SQL editor

2. **Type or paste this SQL**:
   ```sql
   CREATE DATABASE fakedetect
       WITH 
       OWNER = postgres
       ENCODING = 'UTF8'
       CONNECTION LIMIT = -1;
   ```

3. **Execute the Query**:
   - Click the **▶️ Execute/Refresh** button (or press F5)
   - Look at bottom panel for "CREATE DATABASE" message

4. **Refresh Database List**:
   - Right-click on "Databases"
   - Select "Refresh"
   - You should now see "fakedetect"

---

## Part 3: Creating Tables

### Step 1: Open Query Tool for fakedetect Database

1. **Click on "fakedetect"** database in left sidebar to select it

2. **Open Query Tool**:
   - Right-click on **"fakedetect"**
   - Select **"Query Tool"**
   - A new tab opens

3. **Verify you're connected to correct database**:
   - Look at the tab title, it should say "Query Tool - fakedetect"

### Step 2: Run Table Creation SQL

1. **Copy the SQL below** and paste into the Query Tool:

```sql
-- ============================================
-- FAKE PRODUCT DETECTION - TABLE CREATION
-- ============================================

-- Table 1: Classifications
-- Stores all image classification results
CREATE TABLE IF NOT EXISTS classifications (
    id SERIAL PRIMARY KEY,
    request_id VARCHAR(255) UNIQUE NOT NULL,
    image_filename VARCHAR(255) NOT NULL,
    predicted_label VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    probabilities JSONB,
    metadata JSONB,
    explanations JSONB,
    processing_time_ms FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Feedback
-- Stores user feedback on classifications
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    classification_id INTEGER NOT NULL,
    is_correct BOOLEAN NOT NULL,
    user_label VARCHAR(50),
    comments TEXT,
    flagged_for_review BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_classification
        FOREIGN KEY (classification_id) 
        REFERENCES classifications(id) 
        ON DELETE CASCADE
);

-- Table 3: Daily Metrics
-- Stores aggregated daily statistics
CREATE TABLE IF NOT EXISTS daily_metrics (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    total_classifications INTEGER NOT NULL,
    accuracy FLOAT,
    avg_confidence FLOAT,
    original_count INTEGER,
    fake_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Indexes for Performance
CREATE INDEX IF NOT EXISTS idx_classifications_created_at 
    ON classifications(created_at);

CREATE INDEX IF NOT EXISTS idx_classifications_request_id 
    ON classifications(request_id);

CREATE INDEX IF NOT EXISTS idx_feedback_classification_id 
    ON feedback(classification_id);

CREATE INDEX IF NOT EXISTS idx_feedback_flagged 
    ON feedback(flagged_for_review);

CREATE INDEX IF NOT EXISTS idx_daily_metrics_date 
    ON daily_metrics(date);

-- Display success message
SELECT 'Tables created successfully!' AS status;
```

2. **Execute the SQL**:
   - Click **▶️ Execute/Refresh** button (or press F5)
   - Watch the **Messages** panel at bottom

3. **Check for Success**:
   - You should see messages like:
     ```
     CREATE TABLE
     CREATE TABLE
     CREATE TABLE
     CREATE INDEX
     CREATE INDEX
     ...
     Query returned successfully
     ```

### Step 3: Verify Tables Were Created

1. **Refresh the Database Tree**:
   - In left sidebar, expand: `fakedetect` → `Schemas` → `public`
   - Right-click on **"Tables"**
   - Select **"Refresh"**

2. **View Tables**:
   - Expand **"Tables"**
   - You should see:
     ```
     Tables
     ├── classifications
     ├── daily_metrics
     └── feedback
     ```

3. **Inspect Table Structure**:
   - Right-click on **"classifications"**
   - Select **"Properties"**
   - Click **"Columns"** tab to see all fields:
     - id (integer)
     - request_id (character varying)
     - image_filename (character varying)
     - predicted_label (character varying)
     - confidence (double precision)
     - probabilities (jsonb)
     - metadata (jsonb)
     - explanations (jsonb)
     - processing_time_ms (double precision)
     - created_at (timestamp)

---

## Part 4: Testing the Database

### Test 1: View Empty Tables

1. **Right-click on "classifications" table**
2. Select **"View/Edit Data"** → **"All Rows"**
3. You should see column headers but no data (empty table)
4. This confirms the table structure is correct

### Test 2: Insert Test Data

1. **Open Query Tool** (right-click fakedetect → Query Tool)

2. **Run this test query**:
```sql
-- Insert a test classification
INSERT INTO classifications (
    request_id, 
    image_filename, 
    predicted_label, 
    confidence,
    probabilities
) VALUES (
    'test-123',
    'test_image.jpg',
    'Original',
    0.95,
    '{"Original": 0.95, "Fake": 0.05}'::jsonb
);

-- View the inserted data
SELECT * FROM classifications;e
```

3. **Check Results**:
   - Bottom panel shows "INSERT 0 1" (1 row inserted)
   - Second query shows your test data

4. **Clean up test data** (optional):
```sql
DELETE FROM classifications WHERE request_id = 'test-123';
```

### Test 3: Test Foreign Key Relationship

```sql
-- This should work (references existing classification)
INSERT INTO feedback (classification_id, is_correct, comments)
SELECT id, true, 'Test feedback'
FROM classifications
LIMIT 1;

-- View feedback
SELECT * FROM feedback;
```

---

## Part 5: Configure Application Connection

### Step 1: Find Your Connection Details

Your connection details are:
- **Host**: `localhost`
- **Port**: `5432` (default)
- **Database**: `fakedetect`
- **Username**: `postgres`
- **Password**: (your PostgreSQL password)

### Step 2: Update .env File

1. **Open or create `.env` file** in project root

2. **Add this line** (replace YOUR_PASSWORD):
```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/fakedetect
```

Example:
```env
DATABASE_URL=postgresql://postgres:123123@localhost:5432/fakedetect
```

### Step 3: Test Connection from Python

Run the test script:
```bash
python test_db_connection.py
```

You should see:
```
✅ PostgreSQL server is running
✅ Database 'fakedetect' exists
✅ Connected to database: fakedetect
✅ Tables created/verified
```

---

## Part 6: Useful pgAdmin Features

### View Data in Tables

1. Right-click table → **"View/Edit Data"** → **"All Rows"**
2. Or use **"First 100 Rows"** for large tables

### Run Custom Queries

**Example: View recent classifications**
```sql
SELECT 
    request_id,
    image_filename,
    predicted_label,
    confidence,
    created_at
FROM classifications
ORDER BY created_at DESC
LIMIT 10;
```

**Example: View classifications with feedback**
```sql
SELECT 
    c.request_id,
    c.predicted_label,
    c.confidence,
    f.is_correct,
    f.comments
FROM classifications c
LEFT JOIN feedback f ON c.id = f.classification_id
ORDER BY c.created_at DESC;
```

**Example: Get statistics**
```sql
SELECT 
    COUNT(*) as total_classifications,
    AVG(confidence) as avg_confidence,
    SUM(CASE WHEN predicted_label = 'Original' THEN 1 ELSE 0 END) as original_count,
    SUM(CASE WHEN predicted_label = 'Fake' THEN 1 ELSE 0 END) as fake_count
FROM classifications;
```

### Export Data

1. Right-click table → **"Import/Export Data..."**
2. Choose format (CSV, JSON, etc.)
3. Select file location
4. Click "OK"

### Backup Database

1. Right-click **"fakedetect"** database
2. Select **"Backup..."**
3. Choose:
   - **Filename**: `fakedetect_backup_2024-12-13.backup`
   - **Format**: Custom
4. Click **"Backup"**

### Restore Database

1. Right-click **"Databases"**
2. Select **"Restore..."**
3. Choose your backup file
4. Click **"Restore"**

---

## 🔧 Troubleshooting

### Problem: "password authentication failed for user postgres"

**Solution:**
1. You entered wrong password
2. Reset password:
   - Open Command Prompt as Administrator
   - Run: `psql -U postgres`
   - Enter: `ALTER USER postgres PASSWORD 'newpassword';`

### Problem: "database fakedetect does not exist"

**Solution:**
1. Go back to Part 2 and create the database
2. Make sure you're connected to PostgreSQL server first

### Problem: "relation classifications does not exist"

**Solution:**
1. Tables weren't created
2. Go back to Part 3 and run the table creation SQL
3. Make sure you're running SQL in "fakedetect" database, not "postgres"

### Problem: Can't see tables in left sidebar

**Solution:**
1. Right-click "Tables" → "Refresh"
2. Make sure you're looking under: fakedetect → Schemas → public → Tables
3. Not under: postgres → Schemas → public → Tables

### Problem: pgAdmin won't connect to server

**Solution:**
1. Check if PostgreSQL service is running:
   - Windows: Services → PostgreSQL → Start
2. Check if port 5432 is in use:
   - Run: `netstat -an | findstr 5432`

---

## ✅ Verification Checklist

After completing this guide, verify:

- [ ] pgAdmin opens and connects to PostgreSQL
- [ ] Database "fakedetect" exists
- [ ] Three tables exist: classifications, feedback, daily_metrics
- [ ] Can view table structure in pgAdmin
- [ ] Can run SELECT queries successfully
- [ ] .env file has correct DATABASE_URL
- [ ] test_db_connection.py runs successfully

---

## 🎯 Next Steps

Now that your database is set up:

1. **Start Redis** (for rate limiting):
   ```bash
   # If using Docker:
   docker run -d -p 6379:6379 redis
   
   # Or install Redis for Windows
   ```

2. **Start the FastAPI backend**:
   ```bash
   cd backend
   python src/main.py
   ```

3. **Access API documentation**:
   - Open browser: http://localhost:8000/docs
   - Try the `/api/v1/health` endpoint

4. **Test classification**:
   - Use the `/api/v1/classify` endpoint in Swagger UI
   - Upload a test image
   - Check pgAdmin to see data in classifications table

---

## 📚 Additional Resources

- **pgAdmin Documentation**: https://www.pgadmin.org/docs/
- **PostgreSQL Tutorial**: https://www.postgresql.org/docs/current/tutorial.html
- **SQL Cheat Sheet**: https://www.postgresqltutorial.com/postgresql-cheat-sheet/

---

**Need Help?** Check the troubleshooting section or refer to DATABASE_SETUP_GUIDE.md for more details.
