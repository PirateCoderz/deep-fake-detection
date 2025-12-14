"""
Classification logging service with PII anonymization.

This module handles logging of classification events to the database
with proper anonymization of personally identifiable information.
"""
import re
import hashlib
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

try:
    from src.db_models import Classification
    from src.models import ClassificationResult, ImageMetadata
except ImportError:
    from backend.src.db_models import Classification
    from backend.src.models import ClassificationResult, ImageMetadata


class LoggingService:
    """Service for logging classification events with PII anonymization."""
    
    # PII patterns to detect and anonymize
    # Email: must have @ and domain with at least 2 chars
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9][A-Za-z0-9._%+-]*@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    # Phone: matches 555-1234, 555-123-4567, 5551234567 (7-10 digits with optional separators)
    PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    # IP: must be 4 octets with dots, not matching phone numbers
    IP_PATTERN = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')
    
    @staticmethod
    def anonymize_text(text: str) -> str:
        """
        Anonymize PII in text.
        
        Args:
            text: Text that may contain PII
            
        Returns:
            Anonymized text with PII replaced
        """
        if not text:
            return text
        
        # Replace emails
        text = LoggingService.EMAIL_PATTERN.sub('[EMAIL]', text)
        
        # Replace phone numbers
        text = LoggingService.PHONE_PATTERN.sub('[PHONE]', text)
        
        # Replace IP addresses
        text = LoggingService.IP_PATTERN.sub('[IP]', text)
        
        return text
    
    @staticmethod
    def anonymize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively anonymize PII in dictionary.
        
        Args:
            data: Dictionary that may contain PII
            
        Returns:
            Dictionary with PII anonymized
        """
        if not isinstance(data, dict):
            return data
        
        anonymized = {}
        for key, value in data.items():
            if isinstance(value, str):
                anonymized[key] = LoggingService.anonymize_text(value)
            elif isinstance(value, dict):
                anonymized[key] = LoggingService.anonymize_dict(value)
            elif isinstance(value, list):
                anonymized[key] = [
                    LoggingService.anonymize_dict(item) if isinstance(item, dict)
                    else LoggingService.anonymize_text(item) if isinstance(item, str)
                    else item
                    for item in value
                ]
            else:
                anonymized[key] = value
        
        return anonymized
    
    @staticmethod
    def hash_filename(filename: str) -> str:
        """
        Hash filename to protect privacy while maintaining uniqueness.
        
        Args:
            filename: Original filename
            
        Returns:
            Hashed filename with original extension
        """
        if not filename:
            return "unknown"
        
        # Split filename and extension
        parts = filename.rsplit('.', 1)
        name = parts[0]
        ext = parts[1] if len(parts) > 1 else ""
        
        # Hash the name part
        hashed = hashlib.sha256(name.encode()).hexdigest()[:16]
        
        # Return hashed name with original extension
        return f"{hashed}.{ext}" if ext else hashed
    
    @staticmethod
    def log_classification(
        db: Session,
        request_id: str,
        image_filename: str,
        result: ClassificationResult,
        metadata: Optional[ImageMetadata] = None,
        explanations: Optional[list] = None,
        processing_time_ms: float = 0.0,
        anonymize: bool = True
    ) -> Classification:
        """
        Log a classification event to the database.
        
        Args:
            db: Database session
            request_id: Unique request identifier
            image_filename: Original image filename
            result: Classification result
            metadata: Image metadata
            explanations: List of explanation strings
            processing_time_ms: Processing time in milliseconds
            anonymize: Whether to anonymize PII (default: True)
            
        Returns:
            Created Classification record
            
        Raises:
            Exception: If logging fails
        """
        # Anonymize filename if requested
        if anonymize:
            safe_filename = LoggingService.hash_filename(image_filename)
        else:
            safe_filename = image_filename
        
        # Prepare metadata
        metadata_dict = {}
        if metadata:
            metadata_dict = metadata.__dict__ if hasattr(metadata, '__dict__') else dict(metadata)
            if anonymize:
                metadata_dict = LoggingService.anonymize_dict(metadata_dict)
        
        # Anonymize explanations
        safe_explanations = explanations or []
        if anonymize and safe_explanations:
            safe_explanations = [
                LoggingService.anonymize_text(exp) if isinstance(exp, str) else exp
                for exp in safe_explanations
            ]
        
        # Create classification record
        classification = Classification(
            request_id=request_id,
            image_filename=safe_filename,
            predicted_label=result.label,
            confidence=result.confidence,
            probabilities=result.probabilities,
            image_metadata=metadata_dict,  # Renamed from metadata
            explanations=safe_explanations,
            processing_time_ms=processing_time_ms,
            created_at=datetime.utcnow()
        )
        
        try:
            db.add(classification)
            db.commit()
            db.refresh(classification)
            return classification
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to log classification: {str(e)}")
    
    @staticmethod
    def get_classification_by_request_id(
        db: Session,
        request_id: str
    ) -> Optional[Classification]:
        """
        Retrieve a classification by request ID.
        
        Args:
            db: Database session
            request_id: Request identifier
            
        Returns:
            Classification record or None if not found
        """
        return db.query(Classification).filter(
            Classification.request_id == request_id
        ).first()
    
    @staticmethod
    def get_recent_classifications(
        db: Session,
        limit: int = 100
    ) -> list:
        """
        Get recent classifications.
        
        Args:
            db: Database session
            limit: Maximum number of records to return
            
        Returns:
            List of Classification records
        """
        return db.query(Classification).order_by(
            Classification.created_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_classifications_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime
    ) -> list:
        """
        Get classifications within a date range.
        
        Args:
            db: Database session
            start_date: Start of date range
            end_date: End of date range
            
        Returns:
            List of Classification records
        """
        return db.query(Classification).filter(
            Classification.created_at >= start_date,
            Classification.created_at <= end_date
        ).all()
