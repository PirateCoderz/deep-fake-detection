-- Update classifications table to add new columns
-- Run this in pgAdmin or psql

-- Add new columns if they don't exist
ALTER TABLE classifications 
ADD COLUMN IF NOT EXISTS image_filename VARCHAR(255),
ADD COLUMN IF NOT EXISTS predicted_label VARCHAR(50),
ADD COLUMN IF NOT EXISTS confidence FLOAT,
ADD COLUMN IF NOT EXISTS probabilities JSONB,
ADD COLUMN IF NOT EXISTS image_metadata JSONB,
ADD COLUMN IF NOT EXISTS explanations JSONB,
ADD COLUMN IF NOT EXISTS processing_time_ms FLOAT,
ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Create indexes for new columns
CREATE INDEX IF NOT EXISTS idx_classifications_image_filename ON classifications(image_filename);
CREATE INDEX IF NOT EXISTS idx_classifications_predicted_label ON classifications(predicted_label);
CREATE INDEX IF NOT EXISTS idx_classifications_created_at_new ON classifications(created_at);

-- Display success message
SELECT 'Database schema updated successfully!' AS status;
