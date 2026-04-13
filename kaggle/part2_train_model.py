"""
Kaggle copy — two-phase training + generators (same logic as backend/src/train_model.py).
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau,
    TensorBoard,
)
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from part1_classifier import ProductClassifier


class ModelTrainer:
    def __init__(self, classifier: ProductClassifier, output_dir: str = "/kaggle/working/models"):
        self.classifier = classifier
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.phase1_history = None
        self.phase2_history = None

    def train_phase1(
        self,
        train_data,
        val_data,
        epochs: int = 10,
        learning_rate: float = 1e-3,
        class_weights: Optional[Dict[int, float]] = None,
    ):
        print("\n=== PHASE 1: head only (transfer learning) ===")
        self.classifier.compile_model(learning_rate=learning_rate)
        callbacks = self._create_callbacks("phase1", patience=3)
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
        print(f"Phase 1 best val_accuracy: {max(history.history['val_accuracy']):.4f}")
        return history

    def train_phase2(
        self,
        train_data,
        val_data,
        epochs: int = 20,
        learning_rate: float = 1e-5,
        unfreeze_layers: int = 20,
        class_weights: Optional[Dict[int, float]] = None,
    ):
        print("\n=== PHASE 2: fine-tune last ResNet layers ===")
        self.classifier.unfreeze_base_model(num_layers=unfreeze_layers)
        self.classifier.compile_model(learning_rate=learning_rate)
        callbacks = self._create_callbacks("phase2", patience=5)
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
        print(f"Phase 2 best val_accuracy: {max(history.history['val_accuracy']):.4f}")
        return history

    def _create_callbacks(self, phase: str, patience: int = 5):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        monitor = "val_accuracy"
        cb = [
            EarlyStopping(
                monitor=monitor,
                patience=patience,
                restore_best_weights=True,
                verbose=1,
                mode="max",
            ),
            ModelCheckpoint(
                str(self.output_dir / f"checkpoint_{phase}_{ts}.h5"),
                monitor=monitor,
                save_best_only=True,
                verbose=1,
                mode="max",
            ),
            ReduceLROnPlateau(
                monitor=monitor,
                factor=0.5,
                patience=2,
                min_lr=1e-7,
                verbose=1,
                mode="max",
            ),
            TensorBoard(
                log_dir=str(self.output_dir / "logs" / f"{phase}_{ts}"),
                histogram_freq=1,
                write_graph=True,
                update_freq="epoch",
            ),
        ]
        return cb

    def calculate_class_weights(self, labels: np.ndarray) -> Dict[int, float]:
        from sklearn.utils.class_weight import compute_class_weight

        classes = np.unique(labels)
        weights = compute_class_weight(
            class_weight="balanced", classes=classes, y=labels
        )
        out = {int(c): float(w) for c, w in zip(classes, weights)}
        print(f"Class weights: {out}")
        return out

    def save_training_summary(self, filename: str = "training_summary.json"):
        summary = {
            "timestamp": datetime.now().isoformat(),
            "model_architecture": "ResNet50",
            "input_shape": list(self.classifier.input_shape),
            "num_classes": self.classifier.num_classes,
            "kpi_notes": {
                "primary": "val_accuracy (max over epochs per phase)",
                "loss": "sparse_categorical_crossentropy",
            },
        }
        if self.phase1_history:
            h = self.phase1_history.history
            summary["phase1"] = {
                "epochs_ran": len(h["loss"]),
                "final_train_accuracy": float(h["accuracy"][-1]),
                "final_val_accuracy": float(h["val_accuracy"][-1]),
                "best_val_accuracy": float(max(h["val_accuracy"])),
                "final_train_loss": float(h["loss"][-1]),
                "final_val_loss": float(h["val_loss"][-1]),
                "best_val_loss": float(min(h["val_loss"])),
            }
        if self.phase2_history:
            h = self.phase2_history.history
            summary["phase2"] = {
                "epochs_ran": len(h["loss"]),
                "final_train_accuracy": float(h["accuracy"][-1]),
                "final_val_accuracy": float(h["val_accuracy"][-1]),
                "best_val_accuracy": float(max(h["val_accuracy"])),
                "final_train_loss": float(h["loss"][-1]),
                "final_val_loss": float(h["val_loss"][-1]),
                "best_val_loss": float(min(h["val_loss"])),
            }
        path = self.output_dir / filename
        with open(path, "w") as f:
            json.dump(summary, f, indent=2)
        print(f"Training summary saved: {path}")


def create_data_generators(
    train_dir: str,
    val_dir: str,
    batch_size: int = 32,
    image_size: Tuple[int, int] = (224, 224),
):
    train_datagen = ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        zoom_range=0.2,
        brightness_range=[0.8, 1.2],
        fill_mode="nearest",
    )
    val_datagen = ImageDataGenerator()
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
