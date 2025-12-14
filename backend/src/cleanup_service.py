"""
Service for automatic cleanup of temporary files and old data.
"""
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List


class CleanupService:
    """Service for cleaning up temporary files and old data."""
    
    def __init__(self, temp_dir: str = "temp_uploads"):
        """
        Initialize cleanup service.
        
        Args:
            temp_dir: Directory containing temporary files
        """
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def cleanup_old_images(self, max_age_hours: int = 24) -> int:
        """
        Delete images older than specified hours.
        
        Args:
            max_age_hours: Maximum age in hours before deletion
            
        Returns:
            Number of files deleted
        """
        if not self.temp_dir.exists():
            return 0
        
        cutoff_time = time.time() - (max_age_hours * 3600)
        deleted_count = 0
        
        for file_path in self.temp_dir.glob("*"):
            if file_path.is_file():
                try:
                    # Check file modification time
                    if file_path.stat().st_mtime < cutoff_time:
                        file_path.unlink()
                        deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        
        return deleted_count
    
    def cleanup_all_temp_files(self) -> int:
        """
        Delete all temporary files regardless of age.
        
        Returns:
            Number of files deleted
        """
        if not self.temp_dir.exists():
            return 0
        
        deleted_count = 0
        
        for file_path in self.temp_dir.glob("*"):
            if file_path.is_file():
                try:
                    file_path.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        
        return deleted_count
    
    def get_temp_file_count(self) -> int:
        """
        Get count of temporary files.
        
        Returns:
            Number of files in temp directory
        """
        if not self.temp_dir.exists():
            return 0
        
        return sum(1 for f in self.temp_dir.glob("*") if f.is_file())
    
    def get_temp_dir_size(self) -> int:
        """
        Get total size of temporary directory in bytes.
        
        Returns:
            Total size in bytes
        """
        if not self.temp_dir.exists():
            return 0
        
        total_size = 0
        for file_path in self.temp_dir.glob("*"):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except Exception:
                    pass
        
        return total_size
