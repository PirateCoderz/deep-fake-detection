"""
Configuration management for the Fake Product Detection System.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    database_url: str = "postgresql://postgres:123123@localhost:5432/fakedetect"
    database_pool_size: int = 10
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # Model Configuration
    model_path: str = "./models/fake_detector_final.keras"
    model_version: str = "1.0.0"
    target_image_size: int = 224
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Rate Limiting
    rate_limit_per_hour: int = 100
    
    # File Upload
    max_file_size_mb: int = 10
    allowed_formats: List[str] = ["jpeg", "jpg", "png", "heic"]
    temp_storage_path: str = "./temp_uploads"
    image_cleanup_hours: int = 24
    
    # Security
    secret_key: str = "your-secret-key-here"
    https_only: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Model Training
    training_batch_size: int = 32
    validation_split: float = 0.2
    min_model_accuracy: float = 0.85
    
    # Explainability
    confidence_threshold: int = 60
    min_explanation_reasons: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
