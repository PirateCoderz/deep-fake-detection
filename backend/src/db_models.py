"""
SQLAlchemy ORM models for database tables.

This module defines the database schema for storing classifications,
user feedback, and daily metrics.
"""
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, 
    Date, Text, ForeignKey, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

try:
    from database import Base
except ImportError:
    try:
        from src.database import Base
    except ImportError:
        from backend.src.database import Base


class Classification(Base):
    """
    ORM model for the classifications table.
    
    Stores all classification requests and results for logging and analysis.
    """
    __tablename__ = "classifications"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String(255), unique=True, nullable=False, index=True)
    image_filename = Column(String(255), nullable=False)  # Hashed filename for privacy
    predicted_label = Column(String(50), nullable=False)  # "Original" or "Fake"
    confidence = Column(Float, nullable=False)
    probabilities = Column(JSON)  # Class probabilities
    image_metadata = Column(JSON)  # Image metadata (renamed from metadata to avoid SQLAlchemy conflict)
    explanations = Column(JSON)  # Textual explanations
    processing_time_ms = Column(Float)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Legacy fields (kept for compatibility)
    timestamp = Column(DateTime, nullable=True, default=datetime.utcnow, index=True)
    classification = Column(String(10), nullable=True)  # "Original" or "Fake"
    confidence_score = Column(Float, nullable=True)
    model_version = Column(String(50))
    
    # Image metadata (legacy)
    image_quality_score = Column(Float)
    image_width = Column(Integer)
    image_height = Column(Integer)
    image_format = Column(String(10))
    image_size_bytes = Column(Integer)
    has_glare = Column(Boolean, default=False)
    preprocessing_applied = Column(JSON)  # List of preprocessing operations
    
    # Product information
    product_category = Column(String(100))
    
    # Explanation data
    feature_scores = Column(JSON)  # Dictionary of feature scores
    textual_reasons = Column(JSON)  # List of explanation reasons
    
    # Relationship to feedback
    feedback = relationship("Feedback", back_populates="classification", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Classification(id={self.id}, request_id={self.request_id}, classification={self.classification})>"


class Feedback(Base):
    """
    ORM model for the feedback table.
    
    Stores user feedback on classification results for model improvement.
    """
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(UUID(as_uuid=True), ForeignKey("classifications.request_id"), nullable=False, index=True)
    feedback_type = Column(String(20), nullable=False)  # "correct" or "incorrect"
    user_comments = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    flagged_for_review = Column(Boolean, default=False, index=True)
    
    # Relationship to classification
    classification = relationship("Classification", back_populates="feedback")
    
    def __repr__(self):
        return f"<Feedback(id={self.id}, request_id={self.request_id}, feedback_type={self.feedback_type})>"


class DailyMetrics(Base):
    """
    ORM model for the daily_metrics table.
    
    Stores aggregated daily performance metrics for monitoring and analysis.
    """
    __tablename__ = "daily_metrics"
    
    date = Column(Date, primary_key=True, index=True)
    total_classifications = Column(Integer, nullable=False, default=0)
    avg_confidence = Column(Float)
    correct_feedback_count = Column(Integer, default=0)
    incorrect_feedback_count = Column(Integer, default=0)
    avg_processing_time_ms = Column(Float)
    
    # Category-wise breakdown
    category_distribution = Column(JSON)  # Dict of category: count
    classification_distribution = Column(JSON)  # Dict of Original/Fake counts
    
    # Confidence score distribution
    low_confidence_count = Column(Integer, default=0)  # confidence < 60%
    medium_confidence_count = Column(Integer, default=0)  # 60% <= confidence < 80%
    high_confidence_count = Column(Integer, default=0)  # confidence >= 80%
    
    def __repr__(self):
        return f"<DailyMetrics(date={self.date}, total_classifications={self.total_classifications})>"
    
    @property
    def accuracy_estimate(self) -> float:
        """
        Calculate accuracy estimate from user feedback.
        
        Returns:
            Accuracy as a float between 0 and 1, or None if no feedback
        """
        total_feedback = self.correct_feedback_count + self.incorrect_feedback_count
        if total_feedback == 0:
            return None
        return self.correct_feedback_count / total_feedback
