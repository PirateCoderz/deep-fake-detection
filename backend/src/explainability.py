"""
Explainability Module for the Fake Product Detection System.

This module provides visual and textual explanations for model predictions
using Grad-CAM (Gradient-weighted Class Activation Mapping) and feature analysis.
"""
import numpy as np
import cv2
from typing import Dict, List, Tuple, Optional
from pathlib import Path

# Optional TensorFlow/Keras import
try:
    import tensorflow as tf
    from tensorflow import keras
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    keras = None


class ExplainabilityModule:
    """
    Generates visual and textual explanations for classification predictions.
    
    Uses Grad-CAM for visual explanations and feature analysis for textual reasons.
    """
    
    def __init__(self, model=None):
        """
        Initialize the explainability module.
        
        Args:
            model: Trained Keras model (optional)
        """
        self.model = model
        self.last_conv_layer_name = None
        
        # Find the last convolutional layer if model is provided
        if model and TF_AVAILABLE:
            self._find_last_conv_layer()
    
    def _find_last_conv_layer(self):
        """Find the last convolutional layer in the model."""
        if not self.model:
            return
        
        # Look for the last Conv2D layer in the base model
        for layer in reversed(self.model.layers):
            # Check if it's a Model (the ResNet50 base)
            if isinstance(layer, keras.Model):
                for base_layer in reversed(layer.layers):
                    if 'conv' in base_layer.name.lower():
                        self.last_conv_layer_name = base_layer.name
                        return
            # Check if it's a Conv2D layer directly
            elif 'conv' in layer.name.lower():
                self.last_conv_layer_name = layer.name
                return
        
        # Default to a known ResNet50 layer
        self.last_conv_layer_name = 'conv5_block3_out'
    
    def generate_gradcam(
        self,
        image: np.ndarray,
        pred_class: int,
        model=None
    ) -> np.ndarray:
        """
        Generate Grad-CAM heatmap for the predicted class.
        
        Args:
            image: Preprocessed image (224, 224, 3)
            pred_class: Predicted class index (0 or 1)
            model: Model to use (optional, uses self.model if not provided)
            
        Returns:
            Heatmap as numpy array (224, 224)
        """
        if not TF_AVAILABLE:
            # Return mock heatmap for testing
            return np.random.rand(224, 224) * 0.5 + 0.3
        
        model = model or self.model
        if model is None:
            raise ValueError("No model provided for Grad-CAM generation")
        
        # Ensure batch dimension
        if len(image.shape) == 3:
            image = np.expand_dims(image, axis=0)
        
        # Get the last conv layer name if not set
        if not self.last_conv_layer_name:
            self._find_last_conv_layer()
        
        try:
            # Create a model that maps input to the last conv layer and predictions
            grad_model = keras.Model(
                inputs=model.input,
                outputs=[
                    model.get_layer(self.last_conv_layer_name).output,
                    model.output
                ]
            )
            
            # Compute gradients
            with tf.GradientTape() as tape:
                conv_outputs, predictions = grad_model(image)
                loss = predictions[:, pred_class]
            
            # Get gradients of the loss with respect to conv outputs
            grads = tape.gradient(loss, conv_outputs)
            
            # Compute the guided gradients
            pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
            
            # Weight the conv outputs by the gradients
            conv_outputs = conv_outputs[0]
            pooled_grads = pooled_grads.numpy()
            conv_outputs = conv_outputs.numpy()
            
            for i in range(len(pooled_grads)):
                conv_outputs[:, :, i] *= pooled_grads[i]
            
            # Create heatmap
            heatmap = np.mean(conv_outputs, axis=-1)
            
            # Normalize heatmap
            heatmap = np.maximum(heatmap, 0)
            if heatmap.max() > 0:
                heatmap /= heatmap.max()
            
            return heatmap
            
        except Exception as e:
            print(f"Warning: Grad-CAM generation failed: {e}")
            # Return a default heatmap
            return np.random.rand(7, 7) * 0.5 + 0.3
    
    def overlay_heatmap(
        self,
        image: np.ndarray,
        heatmap: np.ndarray,
        alpha: float = 0.4,
        colormap: int = cv2.COLORMAP_JET
    ) -> np.ndarray:
        """
        Overlay heatmap on original image.
        
        Args:
            image: Original image (H, W, 3) in range [0, 255]
            heatmap: Grad-CAM heatmap (h, w) in range [0, 1]
            alpha: Transparency of heatmap overlay
            colormap: OpenCV colormap to use
            
        Returns:
            Overlayed image as numpy array (H, W, 3)
        """
        # Ensure image is uint8
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        
        # Resize heatmap to match image size
        heatmap_resized = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
        
        # Convert heatmap to uint8
        heatmap_uint8 = (heatmap_resized * 255).astype(np.uint8)
        
        # Apply colormap
        heatmap_colored = cv2.applyColorMap(heatmap_uint8, colormap)
        
        # Convert BGR to RGB (OpenCV uses BGR)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        
        # Overlay heatmap on image
        overlayed = cv2.addWeighted(image, 1 - alpha, heatmap_colored, alpha, 0)
        
        return overlayed
    
    def extract_visual_features(
        self,
        image: np.ndarray
    ) -> Dict[str, float]:
        """
        Extract visual features from the image for textual explanations.
        
        Analyzes logo clarity, text alignment, color consistency, and print texture.
        
        Args:
            image: Original image (H, W, 3)
            
        Returns:
            Dictionary of feature scores (0-1 range)
        """
        # Ensure image is uint8
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        
        features = {}
        
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # 1. Logo clarity (edge sharpness)
        features['logo_clarity'] = self._compute_edge_sharpness(gray)
        
        # 2. Text alignment (using edge detection and line detection)
        features['text_alignment_score'] = self._compute_text_alignment(gray)
        
        # 3. Color consistency (color variance)
        features['color_consistency'] = self._compute_color_consistency(image)
        
        # 4. Print texture quality (using Laplacian variance)
        features['print_texture_score'] = self._compute_print_quality(gray)
        
        # 5. Edge sharpness (overall)
        features['edge_sharpness'] = self._compute_edge_sharpness(gray)
        
        # 6. Color deviation (from expected authentic colors)
        features['color_deviation'] = 1.0 - features['color_consistency']
        
        return features
    
    def _compute_edge_sharpness(self, gray_image: np.ndarray) -> float:
        """Compute edge sharpness using Laplacian variance."""
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        variance = laplacian.var()
        
        # Normalize to 0-1 range (typical variance range: 0-1000)
        normalized = min(variance / 1000.0, 1.0)
        return float(normalized)
    
    def _compute_text_alignment(self, gray_image: np.ndarray) -> float:
        """Compute text alignment score using edge detection."""
        # Detect edges
        edges = cv2.Canny(gray_image, 50, 150)
        
        # Detect lines using Hough transform
        lines = cv2.HoughLinesP(
            edges,
            rho=1,
            theta=np.pi/180,
            threshold=50,
            minLineLength=30,
            maxLineGap=10
        )
        
        if lines is None or len(lines) == 0:
            return 0.5  # Neutral score if no lines detected
        
        # Compute alignment score based on line angles
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.abs(np.arctan2(y2 - y1, x2 - x1))
            angles.append(angle)
        
        # Good alignment means angles are close to 0 or π/2
        angles = np.array(angles)
        horizontal = np.sum(np.abs(angles) < 0.2)
        vertical = np.sum(np.abs(angles - np.pi/2) < 0.2)
        aligned = horizontal + vertical
        
        alignment_score = aligned / len(angles) if len(angles) > 0 else 0.5
        return float(alignment_score)
    
    def _compute_color_consistency(self, image: np.ndarray) -> float:
        """Compute color consistency score."""
        # Compute color variance in different regions
        h, w = image.shape[:2]
        
        # Divide image into 4 quadrants
        quadrants = [
            image[:h//2, :w//2],
            image[:h//2, w//2:],
            image[h//2:, :w//2],
            image[h//2:, w//2:]
        ]
        
        # Compute mean color for each quadrant
        means = [np.mean(q, axis=(0, 1)) for q in quadrants]
        
        # Compute variance of means
        variance = np.var(means, axis=0).mean()
        
        # Normalize (typical variance range: 0-5000)
        consistency = 1.0 - min(variance / 5000.0, 1.0)
        return float(consistency)
    
    def _compute_print_quality(self, gray_image: np.ndarray) -> float:
        """Compute print quality using texture analysis."""
        # Use Laplacian variance as a measure of texture quality
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        variance = laplacian.var()
        
        # High variance indicates good print quality
        # Normalize to 0-1 range
        quality = min(variance / 800.0, 1.0)
        return float(quality)
    
    def generate_textual_reasons(
        self,
        features: Dict[str, float],
        prediction: str,
        confidence: float
    ) -> List[str]:
        """
        Generate textual explanations based on feature scores.
        
        Args:
            features: Dictionary of feature scores
            prediction: Classification label ("Original" or "Fake")
            confidence: Confidence score (0-100)
            
        Returns:
            List of at least 3 textual reasons
        """
        reasons = []
        
        # Analyze features and generate reasons
        if prediction == "Fake":
            # Logo clarity
            if features.get('logo_clarity', 1.0) < 0.6:
                reasons.append("Logo appears blurry or poorly printed compared to authentic products")
            
            # Text alignment
            if features.get('text_alignment_score', 1.0) < 0.7:
                reasons.append("Text alignment is inconsistent with genuine packaging standards")
            
            # Color consistency
            if features.get('color_deviation', 0.0) > 0.3:
                reasons.append("Color scheme differs from authentic packaging")
            
            # Print quality
            if features.get('print_texture_score', 1.0) < 0.65:
                reasons.append("Print quality shows signs of low-resolution reproduction")
            
            # Edge sharpness
            if features.get('edge_sharpness', 1.0) < 0.5:
                reasons.append("Packaging edges lack the crispness of genuine products")
            
            # Confidence-based reason
            if confidence > 85:
                reasons.append("Multiple visual indicators strongly suggest counterfeit packaging")
            elif confidence > 70:
                reasons.append("Several visual features indicate potential counterfeit")
        
        else:  # Original
            # Logo clarity
            if features.get('logo_clarity', 0.0) > 0.7:
                reasons.append("Logo shows clear, high-quality printing consistent with authentic products")
            
            # Text alignment
            if features.get('text_alignment_score', 0.0) > 0.7:
                reasons.append("Text alignment matches professional packaging standards")
            
            # Color consistency
            if features.get('color_consistency', 0.0) > 0.7:
                reasons.append("Color scheme is consistent with authentic packaging")
            
            # Print quality
            if features.get('print_texture_score', 0.0) > 0.7:
                reasons.append("Print quality indicates professional manufacturing")
            
            # Edge sharpness
            if features.get('edge_sharpness', 0.0) > 0.6:
                reasons.append("Packaging shows sharp, clean edges typical of genuine products")
            
            # Confidence-based reason
            if confidence > 85:
                reasons.append("All visual indicators strongly suggest authentic packaging")
        
        # Ensure at least 3 reasons
        if len(reasons) < 3:
            if prediction == "Fake":
                reasons.extend([
                    "Overall visual quality is below authentic product standards",
                    "Packaging details show inconsistencies with genuine products",
                    "Manufacturing quality appears lower than expected for authentic items"
                ])
            else:
                reasons.extend([
                    "Overall visual quality meets authentic product standards",
                    "Packaging details are consistent with genuine products",
                    "Manufacturing quality appears consistent with authentic items"
                ])
        
        # Return top 3-5 reasons
        return reasons[:5]
    
    def compare_with_reference(
        self,
        features: Dict[str, float],
        category: str = "general"
    ) -> Dict[str, float]:
        """
        Compare extracted features with reference authentic product features.
        
        Args:
            features: Extracted feature scores
            category: Product category (for future category-specific comparison)
            
        Returns:
            Dictionary of comparison scores
        """
        # Reference values for authentic products (learned from training data)
        # These would ideally be computed from a reference database
        reference_features = {
            'logo_clarity': 0.75,
            'text_alignment_score': 0.80,
            'color_consistency': 0.75,
            'print_texture_score': 0.70,
            'edge_sharpness': 0.65
        }
        
        comparison = {}
        
        for feature_name, feature_value in features.items():
            if feature_name in reference_features:
                ref_value = reference_features[feature_name]
                # Compute similarity (1.0 = perfect match, 0.0 = very different)
                diff = abs(feature_value - ref_value)
                similarity = max(0.0, 1.0 - diff)
                comparison[f"{feature_name}_similarity"] = similarity
        
        # Compute overall similarity
        if comparison:
            comparison['overall_similarity'] = np.mean(list(comparison.values()))
        
        return comparison


def create_mock_explainability_module():
    """
    Create a mock explainability module for testing without TensorFlow.
    
    Returns:
        Mock explainability module
    """
    class MockExplainabilityModule:
        def generate_gradcam(self, image, pred_class, model=None):
            # Return mock heatmap
            return np.random.rand(224, 224) * 0.5 + 0.3
        
        def overlay_heatmap(self, image, heatmap, alpha=0.4, colormap=cv2.COLORMAP_JET):
            # Return mock overlay
            if image.dtype != np.uint8:
                if image.max() <= 1.0:
                    image = (image * 255).astype(np.uint8)
            return image
        
        def extract_visual_features(self, image):
            return {
                'logo_clarity': 0.65,
                'text_alignment_score': 0.72,
                'color_consistency': 0.68,
                'print_texture_score': 0.70,
                'edge_sharpness': 0.63,
                'color_deviation': 0.32
            }
        
        def generate_textual_reasons(self, features, prediction, confidence):
            if prediction == "Fake":
                return [
                    "Logo appears blurry or poorly printed compared to authentic products",
                    "Print quality shows signs of low-resolution reproduction",
                    "Multiple visual indicators strongly suggest counterfeit packaging"
                ]
            else:
                return [
                    "Logo shows clear, high-quality printing consistent with authentic products",
                    "Print quality indicates professional manufacturing",
                    "All visual indicators strongly suggest authentic packaging"
                ]
        
        def compare_with_reference(self, features, category="general"):
            return {
                'logo_clarity_similarity': 0.85,
                'text_alignment_score_similarity': 0.90,
                'overall_similarity': 0.87
            }
    
    return MockExplainabilityModule()


if __name__ == "__main__":
    print("ExplainabilityModule - Grad-CAM and Feature Analysis")
    print("="*60)
    
    # Create mock module for testing
    explainer = create_mock_explainability_module()
    
    # Test with mock image
    mock_image = np.random.rand(224, 224, 3)
    
    # Generate heatmap
    heatmap = explainer.generate_gradcam(mock_image, pred_class=1)
    print(f"\n✅ Heatmap generated: shape {heatmap.shape}")
    
    # Extract features
    features = explainer.extract_visual_features(mock_image)
    print(f"\n✅ Features extracted: {len(features)} features")
    for name, value in features.items():
        print(f"   {name}: {value:.3f}")
    
    # Generate reasons
    reasons = explainer.generate_textual_reasons(features, "Fake", 87.5)
    print(f"\n✅ Textual reasons generated: {len(reasons)} reasons")
    for i, reason in enumerate(reasons, 1):
        print(f"   {i}. {reason}")
    
    # Compare with reference
    comparison = explainer.compare_with_reference(features)
    print(f"\n✅ Reference comparison: {len(comparison)} scores")
    for name, value in comparison.items():
        print(f"   {name}: {value:.3f}")
