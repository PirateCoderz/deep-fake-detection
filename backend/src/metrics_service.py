"""
Daily metrics calculation service.

This module handles aggregation of classification data into daily metrics
for performance tracking and reporting.
"""
from datetime import datetime, date, timedelta
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func

try:
    from src.db_models import Classification, Feedback, DailyMetric
except ImportError:
    from backend.src.db_models import Classification, Feedback, DailyMetric


class MetricsService:
    """Service for calculating and storing daily metrics."""
    
    @staticmethod
    def calculate_daily_metrics(
        db: Session,
        target_date: Optional[date] = None
    ) -> DailyMetric:
        """
        Calculate metrics for a specific date.
        
        Args:
            db: Database session
            target_date: Date to calculate metrics for (default: today)
            
        Returns:
            DailyMetric record with calculated values
        """
        if target_date is None:
            target_date = datetime.utcnow().date()
        
        # Define date range for the target date
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        
        # Get all classifications for the date
        classifications = db.query(Classification).filter(
            Classification.created_at >= start_datetime,
            Classification.created_at <= end_datetime
        ).all()
        
        total_classifications = len(classifications)
        
        if total_classifications == 0:
            # No data for this date
            return DailyMetric(
                date=target_date,
                total_classifications=0,
                accuracy=None,
                avg_confidence=0.0,
                original_count=0,
                fake_count=0
            )
        
        # Calculate accuracy from feedback
        accuracy = MetricsService._calculate_accuracy(db, classifications)
        
        # Calculate average confidence
        avg_confidence = sum(c.confidence for c in classifications) / total_classifications
        
        # Count by category
        original_count = sum(1 for c in classifications if c.predicted_label == "Original")
        fake_count = sum(1 for c in classifications if c.predicted_label == "Fake")
        
        # Create or update daily metric
        existing_metric = db.query(DailyMetric).filter(
            DailyMetric.date == target_date
        ).first()
        
        if existing_metric:
            # Update existing
            existing_metric.total_classifications = total_classifications
            existing_metric.accuracy = accuracy
            existing_metric.avg_confidence = avg_confidence
            existing_metric.original_count = original_count
            existing_metric.fake_count = fake_count
            metric = existing_metric
        else:
            # Create new
            metric = DailyMetric(
                date=target_date,
                total_classifications=total_classifications,
                accuracy=accuracy,
                avg_confidence=avg_confidence,
                original_count=original_count,
                fake_count=fake_count
            )
            db.add(metric)
        
        try:
            db.commit()
            db.refresh(metric)
            return metric
        except Exception as e:
            db.rollback()
            raise Exception(f"Failed to save daily metrics: {str(e)}")
    
    @staticmethod
    def _calculate_accuracy(
        db: Session,
        classifications: list
    ) -> Optional[float]:
        """
        Calculate accuracy from feedback for given classifications.
        
        Args:
            db: Database session
            classifications: List of Classification records
            
        Returns:
            Accuracy as float between 0 and 1, or None if no feedback
        """
        if not classifications:
            return None
        
        classification_ids = [c.id for c in classifications]
        
        # Get feedback for these classifications
        feedbacks = db.query(Feedback).filter(
            Feedback.classification_id.in_(classification_ids)
        ).all()
        
        if not feedbacks:
            return None
        
        # Calculate accuracy
        correct_count = sum(1 for f in feedbacks if f.is_correct)
        total_with_feedback = len(feedbacks)
        
        return correct_count / total_with_feedback if total_with_feedback > 0 else None
    
    @staticmethod
    def calculate_metrics_for_date_range(
        db: Session,
        start_date: date,
        end_date: date
    ) -> list:
        """
        Calculate metrics for a range of dates.
        
        Args:
            db: Database session
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of DailyMetric records
        """
        metrics = []
        current_date = start_date
        
        while current_date <= end_date:
            metric = MetricsService.calculate_daily_metrics(db, current_date)
            metrics.append(metric)
            current_date += timedelta(days=1)
        
        return metrics
    
    @staticmethod
    def get_daily_metric(
        db: Session,
        target_date: date
    ) -> Optional[DailyMetric]:
        """
        Get daily metric for a specific date.
        
        Args:
            db: Database session
            target_date: Date to retrieve
            
        Returns:
            DailyMetric record or None if not found
        """
        return db.query(DailyMetric).filter(
            DailyMetric.date == target_date
        ).first()
    
    @staticmethod
    def get_metrics_summary(
        db: Session,
        days: int = 7
    ) -> Dict[str, Any]:
        """
        Get summary of metrics for the last N days.
        
        Args:
            db: Database session
            days: Number of days to include (default: 7)
            
        Returns:
            Dictionary with summary statistics
        """
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days - 1)
        
        metrics = db.query(DailyMetric).filter(
            DailyMetric.date >= start_date,
            DailyMetric.date <= end_date
        ).order_by(DailyMetric.date).all()
        
        if not metrics:
            return {
                "period": f"Last {days} days",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "total_classifications": 0,
                "average_accuracy": None,
                "average_confidence": 0.0,
                "total_original": 0,
                "total_fake": 0,
                "daily_metrics": []
            }
        
        # Calculate aggregates
        total_classifications = sum(m.total_classifications for m in metrics)
        
        # Average accuracy (only from days with accuracy data)
        accuracies = [m.accuracy for m in metrics if m.accuracy is not None]
        avg_accuracy = sum(accuracies) / len(accuracies) if accuracies else None
        
        # Average confidence
        total_conf = sum(m.avg_confidence * m.total_classifications for m in metrics)
        avg_confidence = total_conf / total_classifications if total_classifications > 0 else 0.0
        
        # Category totals
        total_original = sum(m.original_count for m in metrics)
        total_fake = sum(m.fake_count for m in metrics)
        
        return {
            "period": f"Last {days} days",
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_classifications": total_classifications,
            "average_accuracy": avg_accuracy,
            "average_confidence": avg_confidence,
            "total_original": total_original,
            "total_fake": total_fake,
            "daily_metrics": [
                {
                    "date": m.date.isoformat(),
                    "classifications": m.total_classifications,
                    "accuracy": m.accuracy,
                    "confidence": m.avg_confidence,
                    "original": m.original_count,
                    "fake": m.fake_count
                }
                for m in metrics
            ]
        }
    
    @staticmethod
    def get_overall_statistics(db: Session) -> Dict[str, Any]:
        """
        Get overall system statistics.
        
        Args:
            db: Database session
            
        Returns:
            Dictionary with overall statistics
        """
        # Total classifications
        total_classifications = db.query(func.count(Classification.id)).scalar()
        
        # Get all classifications with feedback
        classifications_with_feedback = db.query(Classification).join(
            Feedback, Classification.id == Feedback.classification_id
        ).all()
        
        # Calculate overall accuracy
        if classifications_with_feedback:
            correct_count = sum(
                1 for c in classifications_with_feedback
                if db.query(Feedback).filter(
                    Feedback.classification_id == c.id,
                    Feedback.is_correct == True
                ).first()
            )
            overall_accuracy = correct_count / len(classifications_with_feedback)
        else:
            overall_accuracy = None
        
        # Average confidence
        all_classifications = db.query(Classification).all()
        if all_classifications:
            avg_confidence = sum(c.confidence for c in all_classifications) / len(all_classifications)
        else:
            avg_confidence = 0.0
        
        # Category distribution
        original_count = db.query(Classification).filter(
            Classification.predicted_label == "Original"
        ).count()
        fake_count = db.query(Classification).filter(
            Classification.predicted_label == "Fake"
        ).count()
        
        # Feedback count
        feedback_count = db.query(func.count(Feedback.id)).scalar()
        
        # Flagged for review count
        flagged_count = db.query(Feedback).filter(
            Feedback.flagged_for_review == True
        ).count()
        
        return {
            "total_classifications": total_classifications,
            "overall_accuracy": overall_accuracy,
            "average_confidence": avg_confidence,
            "category_distribution": {
                "original": original_count,
                "fake": fake_count
            },
            "feedback_count": feedback_count,
            "flagged_for_review": flagged_count
        }
