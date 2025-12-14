# Database Setup Guide - PostgreSQL with pgAdmin

This guide will help you set up the PostgreSQL database for the Fake Product Detection system using pgAdmin.

## Prerequisites

- PostgreSQL installed (download from https://www.postgresql.org/download/)
- pgAdmin 4 installed (comes with PostgreSQL installer)
- PostgreSQL service running

## Step 1: Open pgAdmin

1. Launch **pgAdmin 4** from your Start menu
2. Enter your master password if prompted
3. In the left sidebar, expand **Servers**
4. Click on **PostgreSQL** (you may need to enter your PostgreSQL password)

## Step 2: Create Database

### Option A: Using pgAdmin GUI

1. Right-click on **Databases** in the left sidebar
2. Select **Create** → **Database...**
3. In the dialog:
   - **Database name**: `fakedetect`
   - **Owner**: `postgres` (or your username)
   - **Encoding**: `UTF8`
4. Click **Save**

### Option B: Using SQL Query

1. Right-click on **PostgreSQL** server
2. Select **Query Tool**
3. Run this SQL:

```sql
CREATE DATABASE fakedetect
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;
```

4. Click the **Execute** button (▶️) or press F5

## Step 3: Verify Database Creation

1. In the left sidebar, expand **Databases**
2. You should see **fakedetect** in the list
3. Click on **fakedetect** to select it

## Step 4: Create Tables

The application will automatically create tables when it starts, but you can also create them manually:

### Method 1: Automatic (Recommended)

The tables will be created automatically when you run the FastAPI application:

```bash
cd backend
python src/main.py
```

The code `Base.metadata.create_all(bind=engine)` in `main.py` handles this.

### Method 2: Manual Creation Using pgAdmin

1. Right-click on **fakedetect** database
2. Select **Query Tool**
3. Copy and paste the SQL below:

```sql
-- Create classifications table
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

-- Create feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    classification_id INTEGER NOT NULL,
    is_correct BOOLEAN NOT NULL,
    user_label VARCHAR(50),
    comments TEXT,
    flagged_for_review BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (classification_id) REFERENCES classifications(id) ON DELETE CASCADE
);

-- Create daily_metrics table
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

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_classifications_created_at ON classifications(created_at);
CREATE INDEX IF NOT EXISTS idx_classifications_request_id ON classifications(request_id);
CREATE INDEX IF NOT EXISTS idx_feedback_classification_id ON feedback(classification_id);
CREATE INDEX IF NOT EXISTS idx_feedback_flagged ON feedback(flagged_for_review);
CREATE INDEX IF NOT EXISTS idx_daily_metrics_date ON daily_metrics(date);
```

4. Click **Execute** (▶️) or press F5
5. You should see "Query returned successfully" message

## Step 5: Verify Tables

1. In the left sidebar under **fakedetect**, expand:
   - **Schemas** → **public** → **Tables**
2. You should see three tables:
   - `classifications`
   - `feedback`
   - `daily_metrics`

3. To view table structure:
   - Right-click on a table (e.g., `classifications`)
   - Select **Properties**
   - Click on **Columns** tab to see all fields

## Step 6: Configure Connection String

Update your `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/fakedetect
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

## Step 7: Test Database Connection

Run this Python script to test the connection:

```bash
python -c "from backend.src.database import engine; print('Database connection successful!' if engine else 'Failed')"
```

Or use this test script:

```python
# test_db_connection.py
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/fakedetect"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        print("✅ Database connection successful!")
        print(f"PostgreSQL version: {result.fetchone()[0]}")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

## Common Issues and Solutions

### Issue 1: "password authentication failed"
**Solution**: 
- Verify your PostgreSQL password
- Update the password in `.env` file
- Check if PostgreSQL service is running

### Issue 2: "database does not exist"
**Solution**:
- Make sure you created the `fakedetect` database
- Check the database name spelling in connection string

### Issue 3: "could not connect to server"
**Solution**:
- Start PostgreSQL service:
  - Windows: Services → PostgreSQL → Start
  - Or use pgAdmin: Right-click server → Connect Server
- Check if port 5432 is not blocked by firewall

### Issue 4: Tables not created
**Solution**:
- Run the SQL script manually in pgAdmin Query Tool
- Or run the FastAPI app which auto-creates tables
- Check for error messages in the output

## Viewing Data in pgAdmin

### View all classifications:
1. Right-click on `classifications` table
2. Select **View/Edit Data** → **All Rows**

### Run custom queries:
1. Right-click on **fakedetect** database
2. Select **Query Tool**
3. Example queries:

```sql
-- View all classifications
SELECT * FROM classifications ORDER BY created_at DESC LIMIT 10;

-- View classifications with feedback
SELECT c.request_id, c.predicted_label, c.confidence, f.is_correct, f.comments
FROM classifications c
LEFT JOIN feedback f ON c.id = f.classification_id
ORDER BY c.created_at DESC;

-- View statistics
SELECT 
    COUNT(*) as total_classifications,
    AVG(confidence) as avg_confidence,
    SUM(CASE WHEN predicted_label = 'Original' THEN 1 ELSE 0 END) as original_count,
    SUM(CASE WHEN predicted_label = 'Fake' THEN 1 ELSE 0 END) as fake_count
FROM classifications;

-- View flagged items for review
SELECT c.request_id, c.predicted_label, c.confidence, f.user_label, f.comments
FROM classifications c
JOIN feedback f ON c.id = f.classification_id
WHERE f.flagged_for_review = TRUE
ORDER BY f.created_at DESC;
```

## Database Backup (Optional)

To backup your database:

1. Right-click on **fakedetect** database
2. Select **Backup...**
3. Choose filename and location
4. Click **Backup**

To restore:
1. Right-click on **Databases**
2. Select **Restore...**
3. Choose your backup file
4. Click **Restore**

## Next Steps

After database setup:

1. ✅ Database created: `fakedetect`
2. ✅ Tables created: `classifications`, `feedback`, `daily_metrics`
3. ✅ Connection string configured in `.env`
4. ✅ Connection tested

You can now:
- Start the FastAPI backend: `python backend/src/main.py`
- Run tests: `pytest tests/`
- Use the API endpoints to classify images

## Quick Reference

**Default Connection Details:**
- Host: `localhost`
- Port: `5432`
- Database: `fakedetect`
- Username: `postgres`
- Password: (your PostgreSQL password)

**Connection String Format:**
```
postgresql://username:password@host:port/database
```

**Example:**
```
postgresql://postgres:123123@localhost:5432/fakedetect
```
