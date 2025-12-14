"""
Model Evaluation Module for Fake Product Detection System.

This module provides functions for calculating evaluation metrics,
generating confusion matrices, and analyzing model performance.
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

# Optional sklearn import
try:
    from sklearn.metrics import (
        precision_score, recall_score, f1_score,
        confusion_matrix, classification_report,
        roc_auc_score, roc_curve
    )
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


@dataclass
class ClassificationMetrics:
    """Container for classification metrics."""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    confusion_matrix: np.ndarray
    per_class_metrics: Dict[str, Dict[str, float]]
    
    def to_dict(self) -> Dict:
        """Convert metrics to dictionary."""
        return {
            'accuracy': float(self.accuracy),
            'precision': float(self.precision),
            'recall': float(self.recall),
            'f1_score': float(self.f1_score),
            'confusion_matrix': self.confusion_matrix.tolist(),
            'per_class_metrics': self.per_class_metrics
        }


class ModelEvaluator:
    """
    Evaluates model performance with comprehensive metrics.
    """
    
    def __init__(self, class_names: List[str] = None):
        """
        Initialize the evaluator.
        
        Args:
            class_names: List of class names (e.g., ["Original", "Fake"])
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError(
                "scikit-learn is required for evaluation. "
                "Install with: pip install scikit-learn"
            )
        
        self.class_names = class_names or ["Original", "Fake"]
    
    def calculate_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: Optional[np.ndarray] = None
    ) -> ClassificationMetrics:
        """
        Calculate comprehensive classification metrics.
        
        Args:
            y_true: True labels (shape: [n_samples])
            y_pred: Predicted labels (shape: [n_samples])
            y_proba: Predicted probabilities (shape: [n_samples, n_classes], optional)
            
        Returns:
            ClassificationMetrics object with all metrics
        """
        # Overall metrics
        accuracy = np.mean(y_true == y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        # Per-class metrics
        per_class = self._calculate_per_class_metrics(y_true, y_pred, y_proba)
        
        return ClassificationMetrics(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            confusion_matrix=cm,
            per_class_metrics=per_class
        )
    
    def _calculate_per_class_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        y_proba: Optional[np.ndarray] = None
    ) -> Dict[str, Dict[str, float]]:
        """
        Calculate metrics for each class.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_proba: Predicted probabilities (optional)
            
        Returns:
            Dictionary mapping class names to their metrics
        """
        per_class = {}
        
        # Get unique classes
        classes = np.unique(np.concatenate([y_true, y_pred]))
        
        for cls_idx in classes:
            cls_name = self.class_names[cls_idx] if cls_idx < len(self.class_names) else f"Class_{cls_idx}"
            
            # Binary metrics for this class
            y_true_binary = (y_true == cls_idx).astype(int)
            y_pred_binary = (y_pred == cls_idx).astype(int)
            
            precision = precision_score(y_true_binary, y_pred_binary, zero_division=0)
            recall = recall_score(y_true_binary, y_pred_binary, zero_division=0)
            f1 = f1_score(y_true_binary, y_pred_binary, zero_division=0)
            
            # Support (number of samples)
            support = int(np.sum(y_true == cls_idx))
            
            metrics = {
                'precision': float(precision),
                'recall': float(recall),
                'f1_score': float(f1),
                'support': support
            }
            
            # Add AUC if probabilities provided
            if y_proba is not None and y_proba.shape[1] > cls_idx:
                try:
                    auc = roc_auc_score(y_true_binary, y_proba[:, cls_idx])
                    metrics['auc'] = float(auc)
                except:
                    pass
            
            per_class[cls_name] = metrics
        
        return per_class
    
    def generate_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        normalize: bool = False
    ) -> np.ndarray:
        """
        Generate confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            normalize: Whether to normalize by true labels
            
        Returns:
            Confusion matrix as numpy array
        """
        cm = confusion_matrix(y_true, y_pred)
        
        if normalize:
            cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        
        return cm
    
    def print_classification_report(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray
    ):
        """
        Print detailed classification report.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
        """
        report = classification_report(
            y_true,
            y_pred,
            target_names=self.class_names,
            zero_division=0
        )
        
        print("\nClassification Report:")
        print("="*60)
        print(report)
    
    def print_confusion_matrix(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        normalize: bool = False
    ):
        """
        Print confusion matrix in a readable format.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            normalize: Whether to normalize
        """
        cm = self.generate_confusion_matrix(y_true, y_pred, normalize)
        
        print("\nConfusion Matrix:")
        print("="*60)
        
        # Header
        header = "True\\Pred".ljust(12)
        for name in self.class_names:
            header += name.ljust(12)
        print(header)
        print("-"*60)
        
        # Rows
        for i, name in enumerate(self.class_names):
            row = name.ljust(12)
            for j in range(len(self.class_names)):
                if normalize:
                    row += f"{cm[i, j]:.2%}".ljust(12)
                else:
                    row += f"{cm[i, j]:.0f}".ljust(12)
            print(row)
    
    def calculate_confidence_metrics(
        self,
        y_true: np.ndarray,
        y_proba: np.ndarray,
        confidence_threshold: float = 0.7
    ) -> Dict[str, float]:
        """
        Calculate metrics related to prediction confidence.
        
        Args:
            y_true: True labels
            y_proba: Predicted probabilities
            confidence_threshold: Threshold for high confidence
            
        Returns:
            Dictionary of confidence-related metrics
        """
        # Get predicted labels and max probabilities
        y_pred = np.argmax(y_proba, axis=1)
        max_proba = np.max(y_proba, axis=1)
        
        # Overall metrics
        avg_confidence = float(np.mean(max_proba))
        
        # High confidence predictions
        high_conf_mask = max_proba >= confidence_threshold
        high_conf_accuracy = float(np.mean(y_true[high_conf_mask] == y_pred[high_conf_mask])) if np.any(high_conf_mask) else 0.0
        high_conf_ratio = float(np.mean(high_conf_mask))
        
        # Low confidence predictions
        low_conf_mask = max_proba < confidence_threshold
        low_conf_accuracy = float(np.mean(y_true[low_conf_mask] == y_pred[low_conf_mask])) if np.any(low_conf_mask) else 0.0
        low_conf_ratio = float(np.mean(low_conf_mask))
        
        # Correct vs incorrect confidence
        correct_mask = y_true == y_pred
        avg_correct_confidence = float(np.mean(max_proba[correct_mask])) if np.any(correct_mask) else 0.0
        avg_incorrect_confidence = float(np.mean(max_proba[~correct_mask])) if np.any(~correct_mask) else 0.0
        
        return {
            'avg_confidence': avg_confidence,
            'high_confidence_ratio': high_conf_ratio,
            'high_confidence_accuracy': high_conf_accuracy,
            'low_confidence_ratio': low_conf_ratio,
            'low_confidence_accuracy': low_conf_accuracy,
            'avg_correct_confidence': avg_correct_confidence,
            'avg_incorrect_confidence': avg_incorrect_confidence
        }
    
    def evaluate_model(
        self,
        model,
        test_data,
        verbose: bool = True
    ) -> ClassificationMetrics:
        """
        Evaluate a model on test data.
        
        Args:
            model: Trained model with predict() method
            test_data: Test dataset (images, labels)
            verbose: Whether to print results
            
        Returns:
            ClassificationMetrics object
        """
        # Extract data
        if isinstance(test_data, tuple):
            X_test, y_test = test_data
        else:
            # Assume it's a generator/dataset
            X_test = []
            y_test = []
            for batch_x, batch_y in test_data:
                X_test.append(batch_x)
                y_test.append(batch_y)
            X_test = np.concatenate(X_test)
            y_test = np.concatenate(y_test)
        
        # Get predictions
        y_proba = model.predict(X_test, verbose=0)
        y_pred = np.argmax(y_proba, axis=1)
        
        # Calculate metrics
        metrics = self.calculate_metrics(y_test, y_pred, y_proba)
        
        if verbose:
            print("\nModel Evaluation Results:")
            print("="*60)
            print(f"Accuracy:  {metrics.accuracy:.4f}")
            print(f"Precision: {metrics.precision:.4f}")
            print(f"Recall:    {metrics.recall:.4f}")
            print(f"F1-Score:  {metrics.f1_score:.4f}")
            
            self.print_confusion_matrix(y_test, y_pred)
            self.print_classification_report(y_test, y_pred)
            
            # Confidence metrics
            conf_metrics = self.calculate_confidence_metrics(y_test, y_proba)
            print("\nConfidence Metrics:")
            print("="*60)
            print(f"Average Confidence: {conf_metrics['avg_confidence']:.4f}")
            print(f"High Confidence Ratio: {conf_metrics['high_confidence_ratio']:.2%}")
            print(f"High Confidence Accuracy: {conf_metrics['high_confidence_accuracy']:.4f}")
        
        return metrics


if __name__ == "__main__":
    print("Model Evaluation Module")
    print("="*60)
    print("Provides comprehensive metrics for model evaluation:")
    print("- Accuracy, Precision, Recall, F1-Score")
    print("- Confusion Matrix")
    print("- Per-class metrics")
    print("- Confidence analysis")
    print("="*60)
