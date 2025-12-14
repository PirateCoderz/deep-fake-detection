"""
Wrapper script to run the backend with correct Python path.
This adds the backend directory to sys.path so imports work correctly.
"""
import sys
import os
from pathlib import Path

# Add backend directory to Python path
# This script is in scripts/utilities/, so go up 2 levels to project root
project_root = Path(__file__).parent.parent.parent
backend_dir = project_root / "backend"
sys.path.insert(0, str(backend_dir))

# Now import and run the main application
if __name__ == "__main__":
    from src.main import app
    import uvicorn
    
    print("=" * 60)
    print("Starting Fake Product Detection Backend")
    print("=" * 60)
    print()
    print("Backend API: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/api/v1/health")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
