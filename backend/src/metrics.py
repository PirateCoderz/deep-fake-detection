"""
Performance metrics tracking and monitoring.
"""
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import defaultdict, deque
from threading import Lock


class MetricsCollector:
    """Collect and track application metrics."""
    
    def __init__(self, window_size: int = 1000):
        """
        Initialize metrics collector.
        
        Args:
            window_size: Number of recent metrics to keep in memory
        """
        self.window_size = window_size
        self.lock = Lock()
        
        # Request metrics
        self.request_count = 0
        self.request_times = deque(maxlen=window_size)
        self.request_timestamps = deque(maxlen=window_size)
        
        # Classification metrics
        self.classification_count = 0
        self.classification_times = deque(maxlen=window_size)
        self.classification_labels = deque(maxlen=window_size)
        self.confidence_scores = deque(maxlen=window_size)
        
        # Model inference metrics
        self.inference_times = deque(maxlen=window_size)
        
        # Error metrics
        self.error_count = 0
        self.error_types = defaultdict(int)
        
        # Rate limiting metrics
        self.rate_limit_hits = 0
    
    def record_request(self, duration_ms: float, endpoint: str, status_code: int):
        """
        Record API request metrics.
        
        Args:
            duration_ms: Request duration in milliseconds
            endpoint: API endpoint path
            status_code: HTTP status code
        """
        with self.lock:
            self.request_count += 1
            self.request_times.append(duration_ms)
            self.request_timestamps.append(time.time())
            
            if status_code >= 400:
                self.error_count += 1
                self.error_types[status_code] += 1
            
            if status_code == 429:
                self.rate_limit_hits += 1
    
    def record_classification(
        self,
        label: str,
        confidence: float,
        processing_time_ms: float,
        inference_time_ms: Optional[float] = None
    ):
        """
        Record classification metrics.
        
        Args:
            label: Classification label (Original/Fake)
            confidence: Confidence score (0-1)
            processing_time_ms: Total processing time
            inference_time_ms: Model inference time only
        """
        with self.lock:
            self.classification_count += 1
            self.classification_times.append(processing_time_ms)
            self.classification_labels.append(label)
            self.confidence_scores.append(confidence)
            
            if inference_time_ms is not None:
                self.inference_times.append(inference_time_ms)
    
    def get_request_metrics(self) -> Dict:
        """
        Get request metrics summary.
        
        Returns:
            Dictionary of request metrics
        """
        with self.lock:
            if not self.request_times:
                return {
                    "total_requests": self.request_count,
                    "avg_response_time_ms": 0,
                    "min_response_time_ms": 0,
                    "max_response_time_ms": 0,
                    "requests_per_minute": 0,
                    "error_count": self.error_count,
                    "error_rate": 0
                }
            
            # Calculate requests per minute
            now = time.time()
            recent_requests = sum(1 for ts in self.request_timestamps if now - ts < 60)
            
            return {
                "total_requests": self.request_count,
                "avg_response_time_ms": sum(self.request_times) / len(self.request_times),
                "min_response_time_ms": min(self.request_times),
                "max_response_time_ms": max(self.request_times),
                "requests_per_minute": recent_requests,
                "error_count": self.error_count,
                "error_rate": self.error_count / self.request_count if self.request_count > 0 else 0,
                "rate_limit_hits": self.rate_limit_hits
            }
    
    def get_classification_metrics(self) -> Dict:
        """
        Get classification metrics summary.
        
        Returns:
            Dictionary of classification metrics
        """
        with self.lock:
            if not self.classification_labels:
                return {
                    "total_classifications": self.classification_count,
                    "avg_processing_time_ms": 0,
                    "avg_confidence": 0,
                    "label_distribution": {},
                    "confidence_distribution": {}
                }
            
            # Label distribution
            label_counts = defaultdict(int)
            for label in self.classification_labels:
                label_counts[label] += 1
            
            # Confidence distribution (buckets)
            confidence_buckets = {
                "0.0-0.5": 0,
                "0.5-0.7": 0,
                "0.7-0.85": 0,
                "0.85-1.0": 0
            }
            for conf in self.confidence_scores:
                if conf < 0.5:
                    confidence_buckets["0.0-0.5"] += 1
                elif conf < 0.7:
                    confidence_buckets["0.5-0.7"] += 1
                elif conf < 0.85:
                    confidence_buckets["0.7-0.85"] += 1
                else:
                    confidence_buckets["0.85-1.0"] += 1
            
            return {
                "total_classifications": self.classification_count,
                "avg_processing_time_ms": sum(self.classification_times) / len(self.classification_times),
                "min_processing_time_ms": min(self.classification_times),
                "max_processing_time_ms": max(self.classification_times),
                "avg_confidence": sum(self.confidence_scores) / len(self.confidence_scores),
                "min_confidence": min(self.confidence_scores),
                "max_confidence": max(self.confidence_scores),
                "label_distribution": dict(label_counts),
                "confidence_distribution": confidence_buckets
            }
    
    def get_inference_metrics(self) -> Dict:
        """
        Get model inference metrics.
        
        Returns:
            Dictionary of inference metrics
        """
        with self.lock:
            if not self.inference_times:
                return {
                    "avg_inference_time_ms": 0,
                    "min_inference_time_ms": 0,
                    "max_inference_time_ms": 0
                }
            
            return {
                "avg_inference_time_ms": sum(self.inference_times) / len(self.inference_times),
                "min_inference_time_ms": min(self.inference_times),
                "max_inference_time_ms": max(self.inference_times)
            }
    
    def get_all_metrics(self) -> Dict:
        """
        Get all metrics combined.
        
        Returns:
            Dictionary of all metrics
        """
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "requests": self.get_request_metrics(),
            "classifications": self.get_classification_metrics(),
            "inference": self.get_inference_metrics(),
            "errors": dict(self.error_types)
        }
    
    def reset(self):
        """Reset all metrics."""
        with self.lock:
            self.request_count = 0
            self.request_times.clear()
            self.request_timestamps.clear()
            self.classification_count = 0
            self.classification_times.clear()
            self.classification_labels.clear()
            self.confidence_scores.clear()
            self.inference_times.clear()
            self.error_count = 0
            self.error_types.clear()
            self.rate_limit_hits = 0


# Global metrics collector instance
metrics_collector = MetricsCollector()
