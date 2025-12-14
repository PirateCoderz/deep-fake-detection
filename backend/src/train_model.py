"""
Model Training Script for Fake Product Detection System.

This module implements two-phase training:
1. Transfer learning: Train only the classification head
2. Fine-tuning: Unfreeze and train the last layers of ResNet50
"""

import numpy as np
from pathlib import Path
from typing import Optional, Dict, Tuple
import json
from datetime import datetime

# Optional TensorFlow import
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras.callbacks import (
        EarlyStopping,
        ModelCheckpoint,
        ReduceLROnPlateau,
        TensorBoard,
    )

    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

from src.classifier import ProductClassifier


class ModelTrainer:
    """
    Handles two-phase training of the product classifier.
    """

    def __init__(self, classifier: ProductClassifier, output_dir: str = "models"):
        """
        Initialize the model trainer.

        Args:
            classifier: ProductClassifier instance
            output_dir: Directory to save models and logs
        """
        if not TF_AVAILABLE:
            raise ImportError("TensorFlow is required for training.")

        self.classifier = classifier
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Training history
        self.phase1_history = None
        self.phase2_history = None

    def train_phase1(
        self,
        train_data,
        val_data,
        epochs: int = 10,
        batch_size: int = 32,
        learning_rate: float = 1e-3,
        class_weights: Optional[Dict[int, float]] = None,
    ) -> "keras.callbacks.History":
        """
        Phase 1: Transfer learning - train only classification head.

        Args:
            train_data: Training dataset (tf.data.Dataset or generator)
            val_data: Validation dataset
            epochs: Number of training epochs
            batch_size: Batch size
            learning_rate: Learning rate for optimizer
            class_weights: Optional class weights for imbalanced data

        Returns:
            Training history
        """
        print("\n" + "=" * 60)
        print("PHASE 1: Transfer Learning (Classification Head Only)")
        print("=" * 60)

        # Compile model with higher learning rate
        self.classifier.compile_model(learning_rate=learning_rate)

        # Setup callbacks
        callbacks = self._create_callbacks(
            phase="phase1", monitor="val_accuracy", patience=3
        )

        # Train
        history = self.classifier.model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs,
            callbacks=callbacks,
            class_weight=class_weights,
            verbose=1,
        )

        self.phase1_history = history
        self.classifier.history = history

        print(
            f"\n✅ Phase 1 complete. Best val_accuracy: {max(history.history['val_accuracy']):.4f}"
        )

        return history

    def train_phase2(
        self,
        train_data,
        val_data,
        epochs: int = 20,
        batch_size: int = 32,
        learning_rate: float = 1e-5,
        unfreeze_layers: int = 20,
        class_weights: Optional[Dict[int, float]] = None,
    ) -> "keras.callbacks.History":
        """
        Phase 2: Fine-tuning - unfreeze and train last layers of base model.

        Args:
            train_data: Training dataset
            val_data: Validation dataset
            epochs: Number of training epochs
            batch_size: Batch size
            learning_rate: Lower learning rate for fine-tuning
            unfreeze_layers: Number of base model layers to unfreeze
            class_weights: Optional class weights

        Returns:
            Training history
        """
        print("\n" + "=" * 60)
        print("PHASE 2: Fine-Tuning (Last Layers of ResNet50)")
        print("=" * 60)

        # Unfreeze base model layers
        self.classifier.unfreeze_base_model(num_layers=unfreeze_layers)

        # Recompile with lower learning rate
        self.classifier.compile_model(learning_rate=learning_rate)

        # Setup callbacks
        callbacks = self._create_callbacks(
            phase="phase2", monitor="val_accuracy", patience=5
        )

        # Train
        history = self.classifier.model.fit(
            train_data,
            validation_data=val_data,
            epochs=epochs,
            callbacks=callbacks,
            class_weight=class_weights,
            verbose=1,
        )

        self.phase2_history = history
        self.classifier.history = history

        print(
            f"\n✅ Phase 2 complete. Best val_accuracy: {max(history.history['val_accuracy']):.4f}"
        )

        return history

    def _create_callbacks(
        self, phase: str, monitor: str = "val_accuracy", patience: int = 5
    ) -> list:
        """
        Create training callbacks.

        Args:
            phase: Training phase name ("phase1" or "phase2")
            monitor: Metric to monitor
            patience: Early stopping patience

        Returns:
            List of callbacks
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        callbacks = []

        # Early stopping
        early_stop = EarlyStopping(
            monitor=monitor,
            patience=patience,
            restore_best_weights=True,
            verbose=1,
            mode="max",
        )
        callbacks.append(early_stop)

        # Model checkpoint
        checkpoint_path = self.output_dir / f"checkpoint_{phase}_{timestamp}.h5"
        checkpoint = ModelCheckpoint(
            str(checkpoint_path),
            monitor=monitor,
            save_best_only=True,
            verbose=1,
            mode="max",
        )
        callbacks.append(checkpoint)

        # Learning rate reduction
        reduce_lr = ReduceLROnPlateau(
            monitor=monitor, factor=0.5, patience=2, min_lr=1e-7, verbose=1, mode="max"
        )
        callbacks.append(reduce_lr)

        # TensorBoard logging
        log_dir = self.output_dir / "logs" / f"{phase}_{timestamp}"
        tensorboard = TensorBoard(
            log_dir=str(log_dir),
            histogram_freq=1,
            write_graph=True,
            update_freq="epoch",
        )
        callbacks.append(tensorboard)

        return callbacks

    def calculate_class_weights(self, labels: np.ndarray) -> Dict[int, float]:
        """
        Calculate class weights for imbalanced datasets.

        Args:
            labels: Array of class labels

        Returns:
            Dictionary mapping class indices to weights
        """
        from sklearn.utils.class_weight import compute_class_weight

        classes = np.unique(labels)
        weights = compute_class_weight(
            class_weight="balanced", classes=classes, y=labels
        )

        class_weights = {
            int(cls): float(weight) for cls, weight in zip(classes, weights)
        }

        print(f"Class weights: {class_weights}")

        return class_weights

    def save_training_summary(self, filename: str = "training_summary.json"):
        """
        Save training summary to JSON file.

        Args:
            filename: Output filename
        """
        summary = {
            "timestamp": datetime.now().isoformat(),
            "model_architecture": "ResNet50",
            "input_shape": self.classifier.input_shape,
            "num_classes": self.classifier.num_classes,
        }

        # Add phase 1 metrics
        if self.phase1_history:
            summary["phase1"] = {
                "epochs": len(self.phase1_history.history["loss"]),
                "final_train_accuracy": float(
                    self.phase1_history.history["accuracy"][-1]
                ),
                "final_val_accuracy": float(
                    self.phase1_history.history["val_accuracy"][-1]
                ),
                "best_val_accuracy": float(
                    max(self.phase1_history.history["val_accuracy"])
                ),
            }

        # Add phase 2 metrics
        if self.phase2_history:
            summary["phase2"] = {
                "epochs": len(self.phase2_history.history["loss"]),
                "final_train_accuracy": float(
                    self.phase2_history.history["accuracy"][-1]
                ),
                "final_val_accuracy": float(
                    self.phase2_history.history["val_accuracy"][-1]
                ),
                "best_val_accuracy": float(
                    max(self.phase2_history.history["val_accuracy"])
                ),
            }

        # Save to file
        output_path = self.output_dir / filename
        with open(output_path, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"✅ Training summary saved to {output_path}")


def create_data_generators(
    train_dir: str,
    val_dir: str,
    batch_size: int = 32,
    image_size: Tuple[int, int] = (224, 224),
):
    """
    Create data generators for training and validation.

    Args:
        train_dir: Training data directory
        val_dir: Validation data directory
        batch_size: Batch size
        image_size: Target image size

    Returns:
        Tuple of (train_generator, val_generator)
    """
    if not TF_AVAILABLE:
        raise ImportError("TensorFlow is required.")

    from tensorflow.keras.preprocessing.image import ImageDataGenerator

    # Training data augmentation
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        brightness_range=[0.8, 1.2],
        fill_mode="nearest",
    )

    # Validation data (no augmentation)
    val_datagen = ImageDataGenerator()

    # Create generators
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode="sparse",
        shuffle=True,
    )

    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=image_size,
        batch_size=batch_size,
        class_mode="sparse",
        shuffle=False,
    )

    return train_generator, val_generator


if __name__ == "__main__":
    print("Model Training Script")
    print("=" * 60)
    print("This script implements two-phase training:")
    print("1. Transfer learning (classification head only)")
    print("2. Fine-tuning (unfreeze last layers)")
    print("=" * 60)
