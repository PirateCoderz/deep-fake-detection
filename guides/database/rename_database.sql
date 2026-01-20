-- Rename database from 'fakedetect' to 'fakedetect'
-- Run this in pgAdmin or psql

-- Step 1: Disconnect all users from the database
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = 'fakedetect'
  AND pid <> pg_backend_pid();

-- Step 2: Rename the database
ALTER DATABASE fakedetect RENAME TO fakedetect;

-- Done! The database is now named 'fakedetect'
