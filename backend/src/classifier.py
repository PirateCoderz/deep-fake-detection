"""
CNN Classification Model for the Fake Product Detection System.

This module implements the ProductClassifier using transfer learning
with ResNet50 backbone for binary classification (Original vs Fake).
"""
import numpy as np
from pathlib import Path
from typing import Tuple, Dict, Optional
import json

# Optional TensorFlow/Keras import
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers, models
    from tensorflow.keras.applications import ResNet50
    from tensorflow.keras.optimizers import Adam
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    # Create dummy keras for type hints
    keras = None


class ProductClassifier:
    """
    CNN-based product authenticity classifier using ResNet50 backbone.
    
    Uses transfer learning with a pre-trained ResNet50 model and custom
    classification head for binary classification (Original vs Fake).
    """
    
    def __init__(
        self,
        input_shape: Tuple[int, int, int] = (224, 224, 3),
        num_classes: int = 2,
        model_path: Optional[str] = None
    ):
        """
        Initialize the product classifier.
        
        Args:
            input_shape: Input image shape (height, width, channels)
            num_classes: Number of output classes (default: 2 for binary)
            model_path: Path to pre-trained model weights (optional)
        """
        if not TF_AVAILABLE:
            raise ImportError(
                "TensorFlow is required for ProductClassifier. "
                "Install with: pip install tensorflow"
            )
        
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = None
        self.history = None
        
        if model_path:
            self.load_model(model_path)
        else:
            self.model = self._build_model()
    
    def _build_model(self):
        """
        Build the classification model with ResNet50 backbone.
        
        Returns:
            Compiled Keras model
        """
        # Load pre-trained ResNet50 (without top layers)
        base_model = ResNet50(
            weights='imagenet',
            include_top=False,
            input_shape=self.input_shape
        )
        
        # Freeze base model initially (for transfer learning)
        base_model.trainable = False
        
        # Build custom classification head
        inputs = keras.Input(shape=self.input_shape)
        
        # Preprocessing for ResNet50 (ImageNet normalization)
        x = keras.applications.resnet50.preprocess_input(inputs)
        
        # Base model
        x = base_model(x, training=False)
        
        # Classification head
        x = layers.GlobalAveragePooling2D()(x)
        x = layers.Dense(512, activation='relu', name='dense_512')(x)
        x = layers.Dropout(0.5, name='dropout_0.5')(x)
        x = layers.Dense(256, activation='relu', name='dense_256')(x)
        x = layers.Dropout(0.3, name='dropout_0.3')(x)
        outputs = layers.Dense(self.num_classes, activation='softmax', name='output')(x)
        
        # Create model
        model = keras.Model(inputs=inputs, outputs=outputs, name='ProductClassifier')
        
        return model
    
    def compile_model(
        self,
        learning_rate: float = 1e-4,
        class_weights: Optional[Dict[int, float]] = None
    ):
        """
        Compile the model with optimizer and loss function.
        
        Args:
            learning_rate: Learning rate for Adam optimizer
            class_weights: Optional class weights for imbalanced data
        """
        # Compile model with simple metrics to avoid shape issues
        self.model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"✅ Model compiled with learning rate: {learning_rate}")
    
    def unfreeze_base_model(self, num_layers: int = 20):
        """
        Unfreeze the last N layers of the base model for fine-tuning.
        
        Args:
            num_layers: Number of layers to unfreeze from the end
        """
        # Find the ResNet50 base model in the layers
        base_model = None
        for layer in self.model.layers:
            if isinstance(layer, keras.Model) and 'resnet' in layer.name.lower():
                base_model = layer
                break
        
        if base_model is None:
            print("⚠️  Warning: Could not find ResNet50 base model. Skipping unfreezing.")
            return
        
        # Unfreeze last N layers
        base_model.trainable = True
        
        # Freeze all layers except the last N
        for layer in base_model.layers[:-num_layers]:
            layer.trainable = False
        
        trainable_count = sum([1 for layer in base_model.layers if layer.trainable])
        print(f"✅ Unfroze last {num_layers} layers of base model ({trainable_count} layers trainable)")
    
    def predict(
        self,
        image: np.ndarray,
        return_probabilities: bool = False
    ) -> Tuple[str, float, Optional[np.ndarray]]:
        """
        Predict the authenticity of a product image.
        
        Args:
            image: Preprocessed image as numpy array (224, 224, 3)
            return_probabilities: Whether to return class probabilities
            
        Returns:
            Tuple of (label, confidence, probabilities)
            - label: "Original" or "Fake"
            - confidence: Confidence score (0-100%)
            - probabilities: Class probabilities (if requested)
        """
        if self.model is None:
            raise ValueError("Model not initialized. Build or load a model first.")
        
        # Ensure batch dimension
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Predict
        predictions = self.model.predict(image, verbose=0)
        
        # Get predicted class and confidence
        predicted_class = np.argmax(predictions[0])
        confidence = predictions[0][predicted_class] * 100
        
        # Map to label
        label = "Original" if predicted_class == 0 else "Fake"
        
        if return_probabilities:
            return label, confidence, predictions[0]
        else:
            return label, confidence, None
    
    def predict_batch(
        self,
        images: np.ndarray,
        batch_size: int = 32,
        return_probabilities: bool = False
    ) -> list:
        """
        Predict authenticity for a batch of images.
        
        Args:
            images: Batch of preprocessed images (N, 224, 224, 3)
            batch_size: Batch size for prediction
            return_probabilities: Whether to return class probabilities
            
        Returns:
            List of tuples (label, confidence, probabilities)
        """
        if self.model is None:
            raise ValueError("Model not initialized. Build or load a model first.")
        
        # Ensure 4D input
        if len(images.shape) == 3:
            images = np.expand_dims(images, axis=0)
        
        # Predict in batches
        predictions = self.model.predict(images, batch_size=batch_size, verbose=0)
        
        # Process results
        results = []
        for pred in predictions:
            predicted_class = np.argmax(pred)
            confidence = pred[predicted_class] * 100
            label = "Original" if predicted_class == 0 else "Fake"
            
            if return_probabilities:
                results.append((label, confidence, pred))
            else:
                results.append((label, confidence, None))
        
        return results
    
    def get_feature_maps(
        self,
        image: np.ndarray,
        layer_name: Optional[str] = None
    ) -> Dict[str, np.ndarray]:
        """
        Extract feature maps from intermediate layers.
        
        Args:
            image: Preprocessed image as numpy array
            layer_name: Specific layer name (optional)
            
        Returns:
            Dictionary of layer names to feature maps
        """
        if self.model is None:
            raise ValueError("Model not initialized.")
        
        # Ensure batch dimension
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Get all layer outputs or specific layer
        if layer_name:
            layer = self.model.get_layer(layer_name)
            feature_model = keras.Model(
                inputs=self.model.input,
                outputs=layer.output
            )
            features = feature_model.predict(image, verbose=0)
            return {layer_name: features}
        else:
            # Get outputs from key layers
            layer_names = ['dense_512', 'dense_256', 'output']
            feature_maps = {}
            
            for name in layer_names:
                try:
                    layer = self.model.get_layer(name)
                    feature_model = keras.Model(
                        inputs=self.model.input,
                        outputs=layer.output
                    )
                    features = feature_model.predict(image, verbose=0)
                    feature_maps[name] = features
                except:
                    pass
            
            return feature_maps
    
    def save_model(self, save_path: str, save_history: bool = True):
        """
        Save the model weights and configuration.
        
        Args:
            save_path: Path to save the model
            save_history: Whether to save training history
        """
        if self.model is None:
            raise ValueError("No model to save.")
        
        save_path = Path(save_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert .h5 to .keras for better compatibility
        if str(save_path).endswith('.h5'):
            save_path = Path(str(save_path).replace('.h5', '.keras'))
        
        # Save model in native Keras format
        self.model.save(str(save_path))
        
        # Save configuration
        config = {
            'input_shape': self.input_shape,
            'num_classes': self.num_classes,
            'model_architecture': 'ResNet50'
        }
        
        config_path = save_path.parent / f"{save_path.stem}_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Save training history if available
        if save_history and self.history:
            history_path = save_path.parent / f"{save_path.stem}_history.json"
            history_dict = {k: [float(v) for v in vals] for k, vals in self.history.history.items()}
            with open(history_path, 'w') as f:
                json.dump(history_dict, f, indent=2)
        
        print(f"✅ Model saved to {save_path}")
    
    def load_model(self, model_path: str):
        """
        Load a pre-trained model.
        
        Args:
            model_path: Path to saved model
        """
        model_path = Path(model_path)
        
        # Try .keras format first, then .h5
        keras_path = Path(str(model_path).replace('.h5', '.keras'))
        
        if keras_path.exists():
            model_path = keras_path
        elif not model_path.exists():
            raise FileNotFoundError(f"Model not found: {model_path}")
        
        # Load model with compile=False to avoid custom layer issues
        self.model = keras.models.load_model(str(model_path), compile=False)
        
        # Recompile the model
        self.compile_model()
        
        # Load configuration if available
        config_path = model_path.parent / f"{model_path.stem}_config.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.input_shape = tuple(config['input_shape'])
                self.num_classes = config['num_classes']
        
        print(f"✅ Model loaded from {model_path}")
    
    def get_model_summary(self) -> str:
        """
        Get a summary of the model architecture.
        
        Returns:
            Model summary as string
        """
        if self.model is None:
            return "No model initialized."
        
        # Capture summary
        summary_lines = []
        self.model.summary(print_fn=lambda x: summary_lines.append(x))
        return '\n'.join(summary_lines)
    
    def count_parameters(self) -> Dict[str, int]:
        """
        Count trainable and non-trainable parameters.
        
        Returns:
            Dictionary with parameter counts
        """
        if self.model is None:
            return {'trainable': 0, 'non_trainable': 0, 'total': 0}
        
        trainable = sum([tf.size(w).numpy() for w in self.model.trainable_weights])
        non_trainable = sum([tf.size(w).numpy() for w in self.model.non_trainable_weights])
        
        return {
            'trainable': int(trainable),
            'non_trainable': int(non_trainable),
            'total': int(trainable + non_trainable)
        }


def create_mock_classifier():
    """
    Create a mock classifier for testing without TensorFlow.
    
    Returns:
        Mock classifier object
    """
    class MockClassifier:
        def __init__(self):
            self.input_shape = (224, 224, 3)
            self.num_classes = 2
        
        def predict(self, image, return_probabilities=False):
            # Mock prediction
            label = "Original"
            confidence = 85.5
            probabilities = np.array([0.855, 0.145]) if return_probabilities else None
            return label, confidence, probabilities
        
        def get_feature_maps(self, image, layer_name=None):
            return {'mock_layer': np.random.rand(1, 512)}
    
    return MockClassifier()


if __name__ == "__main__":
    if TF_AVAILABLE:
        print("ProductClassifier - CNN Model")
        print("="*50)
        
        # Create classifier
        classifier = ProductClassifier()
        classifier.compile_model(learning_rate=1e-4)
        
        # Print summary
        print("\nModel Architecture:")
        print(classifier.get_model_summary())
        
        # Count parameters
        params = classifier.count_parameters()
        print(f"\nParameters:")
        print(f"  Trainable: {params['trainable']:,}")
        print(f"  Non-trainable: {params['non_trainable']:,}")
        print(f"  Total: {params['total']:,}")
    else:
        print("⚠️  TensorFlow not available. Install with: pip install tensorflow")
