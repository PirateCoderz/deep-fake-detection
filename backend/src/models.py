"""
Data models for the Fake Product Detection System.

This module defines dataclasses for representing images, classification results,
explanations, and user feedback throughout the system.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Optional, Any
from uuid import UUID, uuid4
import numpy as np


@dataclass
class ImageMetadata:
    """
    Metadata about an uploaded product image.
    
    Attributes:
        original_width: Width of the original image in pixels
        original_height: Height of the original image in pixels
        file_format: Image format (JPEG, PNG, HEIC)
        file_size_bytes: Size of the image file in bytes
        quality_score: Quality assessment score (0-1) based on blur/resolution
        has_glare: Whether glare was detected in the image
        preprocessing_applied: List of preprocessing operations applied
    """
    original_width: int
    original_height: int
    file_format: str
    file_size_bytes: int
    quality_score: float
    has_glare: bool
    preprocessing_applied: List[str] = field(default_factory=list)
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate the image metadata.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.original_width <= 0 or self.original_height <= 0:
            return False, "Image dimensions must be positive"
        
        if self.file_format.upper() not in ["JPEG", "JPG", "PNG", "HEIC"]:
            return False, f"Unsupported file format: {self.file_format}"
        
        if self.file_size_bytes <= 0:
            return False, "File size must be positive"
        
        if self.file_size_bytes > 10 * 1024 * 1024:  # 10MB
            return False, "File size exceeds 10MB limit"
        
        if not 0 <= self.quality_score <= 1:
            return False, "Quality score must be between 0 and 1"
        
        return True, ""


@dataclass
class ClassificationResult:
    """
    Result of a product authenticity classification.
    
    Attributes:
        request_id: Unique identifier for this classification request
        timestamp: When the classification was performed
        classification: Classification label ("Original" or "Fake")
        confidence_score: Confidence percentage (0-100)
        processing_time_ms: Time taken to process in milliseconds
        model_version: Version of the model used
        image_metadata: Metadata about the classified image
    """
    request_id: UUID
    timestamp: datetime
    classification: str
    confidence_score: float
    processing_time_ms: int
    model_version: str
    image_metadata: ImageMetadata
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate the classification result.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.classification not in ["Original", "Fake"]:
            return False, f"Invalid classification: {self.classification}"
        
        if not 0 <= self.confidence_score <= 100:
            return False, "Confidence score must be between 0 and 100"
        
        if self.processing_time_ms < 0:
            return False, "Processing time cannot be negative"
        
        # Validate image metadata
        metadata_valid, metadata_error = self.image_metadata.validate()
        if not metadata_valid:
            return False, f"Invalid image metadata: {metadata_error}"
        
        return True, ""
    
    def has_low_confidence(self) -> bool:
        """Check if confidence score is below threshold (60%)."""
        return self.confidence_score < 60


@dataclass
class ExplanationData:
    """
    Explanation data for a classification decision.
    
    Attributes:
        heatmap_image: Grad-CAM heatmap overlay as numpy array
        textual_reasons: List of textual explanations (3-5 reasons)
        feature_scores: Dictionary of individual feature analysis scores
        reference_comparison: Optional feature comparison with reference images
    """
    heatmap_image: np.ndarray
    textual_reasons: List[str]
    feature_scores: Dict[str, float]
    reference_comparison: Optional[Dict[str, float]] = None
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate the explanation data.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.heatmap_image is None or self.heatmap_image.size == 0:
            return False, "Heatmap image cannot be empty"
        
        if len(self.textual_reasons) < 3:
            return False, "Must provide at least 3 textual reasons"
        
        if not self.feature_scores:
            return False, "Feature scores cannot be empty"
        
        # Validate feature scores are in valid range
        for feature, score in self.feature_scores.items():
            if not isinstance(score, (int, float)):
                return False, f"Feature score for {feature} must be numeric"
            if not 0 <= score <= 1:
                return False, f"Feature score for {feature} must be between 0 and 1"
        
        return True, ""


@dataclass
class UserFeedback:
    """
    User feedback on a classification result.
    
    Attributes:
        request_id: Reference to the classification request
        feedback_type: Type of feedback ("correct" or "incorrect")
        user_comments: Optional user comments
        timestamp: When the feedback was submitted
        flagged_for_review: Whether this feedback flags the classification for review
    """
    request_id: UUID
    feedback_type: str
    user_comments: Optional[str]
    timestamp: datetime
    flagged_for_review: bool = False
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate the user feedback.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if self.feedback_type not in ["correct", "incorrect"]:
            return False, f"Invalid feedback type: {self.feedback_type}"
        
        if not self.request_id:
            return False, "Request ID cannot be empty"
        
        # Flag for review if feedback indicates incorrect classification
        if self.feedback_type == "incorrect":
            self.flagged_for_review = True
        
        return True, ""


@dataclass
class TrainingSample:
    """
    Training sample for model training.
    
    Attributes:
        image_path: Path to the image file
        label: Classification label (0 = Original, 1 = Fake)
        product_category: Category of the product
        brand: Optional brand name
        source: Source of the image
        verified: Whether the label has been manually verified
        metadata: Additional metadata
    """
    image_path: str
    label: int
    product_category: str
    brand: Optional[str] = None
    source: str = "unknown"
    verified: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> tuple[bool, str]:
        """
        Validate the training sample.
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.image_path:
            return False, "Image path cannot be empty"
        
        if self.label not in [0, 1]:
            return False, "Label must be 0 (Original) or 1 (Fake)"
        
        if not self.product_category:
            return False, "Product category cannot be empty"
        
        return True, ""
