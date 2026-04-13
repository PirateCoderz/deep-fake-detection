"""
Kaggle copy — ResNet50 + head (same as backend/src/classifier.py).
"""
import json
from pathlib import Path
from typing import Dict, Optional, Tuple

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.optimizers import Adam


class ProductClassifier:
    def __init__(
        self,
        input_shape: Tuple[int, int, int] = (224, 224, 3),
        num_classes: int = 2,
        model_path: Optional[str] = None,
    ):
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        self.history = None

        if model_path:
            self.load_model(model_path)
        else:
            self.model = self._build_model()

    def _build_model(self):
        base_model = ResNet50(
            weights="imagenet",
            include_top=False,
            input_shape=self.input_shape,
        )
        base_model.trainable = False

        inputs = keras.Input(shape=self.input_shape)
        x = keras.applications.resnet50.preprocess_input(inputs)
        x = base_model(x, training=False)
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(512, activation="relu", name="dense_512")(x)
        x = layers.Dropout(0.5, name="dropout_0.5")(x)
        x = layers.Dense(256, activation="relu", name="dense_256")(x)
        x = layers.Dropout(0.3, name="dropout_0.3")(x)
        outputs = layers.Dense(self.num_classes, activation="softmax", name="output")(x)
        return keras.Model(inputs=inputs, outputs=outputs, name="ProductClassifier")

    def compile_model(
        self,
        learning_rate: float = 1e-4,
        class_weights: Optional[Dict[int, float]] = None,
    ):
        self.model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )
        print(f"Model compiled, lr={learning_rate}")

    def unfreeze_base_model(self, num_layers: int = 20):
        base_model = None
        for layer in self.model.layers:
            if isinstance(layer, keras.Model) and "resnet" in layer.name.lower():
                base_model = layer
                break
        if base_model is None:
            print("Warning: ResNet50 submodel not found; skip unfreeze.")
            return
        base_model.trainable = True
        for layer in base_model.layers[:-num_layers]:
            layer.trainable = False
        trainable_count = sum(1 for layer in base_model.layers if layer.trainable)
        print(f"Unfroze last {num_layers} base layers ({trainable_count} trainable)")

    def save_model(self, save_path: str, save_history: bool = True):
        if self.model is None:
            raise ValueError("No model to save.")
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        if str(save_path).endswith(".h5"):
            save_path = Path(str(save_path).replace(".h5", ".keras"))
        self.model.save(str(save_path))
        config = {
            "input_shape": list(self.input_shape),
            "num_classes": self.num_classes,
            "model_architecture": "ResNet50",
        }
        config_path = save_path.parent / f"{save_path.stem}_config.json"
        with open(config_path, "w") as f:
            json.dump(config, f, indent=2)
        if save_history and self.history:
            history_path = save_path.parent / f"{save_path.stem}_history.json"
            history_dict = {
                k: [float(v) for v in vals] for k, vals in self.history.history.items()
            }
            with open(history_path, "w") as f:
                json.dump(history_dict, f, indent=2)
        print(f"Model saved to {save_path}")

    def load_model(self, model_path: str):
        model_path = Path(model_path)
        keras_path = Path(str(model_path).replace(".h5", ".keras"))
        if keras_path.exists():
            model_path = keras_path
        elif not model_path.exists():
            raise FileNotFoundError(model_path)
        self.model = keras.models.load_model(str(model_path), compile=False)
        self.compile_model()
        config_path = model_path.parent / f"{model_path.stem}_config.json"
        if config_path.exists():
            with open(config_path) as f:
                config = json.load(f)
                self.input_shape = tuple(config["input_shape"])
                self.num_classes = config["num_classes"]
        print(f"Model loaded from {model_path}")
