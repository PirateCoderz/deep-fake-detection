"""
Data augmentation pipeline for the Fake Product Detection System.

This module provides data augmentation functions and generators for
training the classification model with augmented data.
"""
import numpy as np
from PIL import Image, ImageEnhance
import random
from typing import Tuple, List, Callable

# Optional TensorFlow import
try:
    import tensorflow as tf
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False


class ImageAugmentor:
    """
    Image augmentation utilities for training data.
    
    Applies random transformations to increase dataset diversity and
    improve model generalization.
    """
    
    def __init__(
        self,
        rotation_range: float = 15.0,
        horizontal_flip: bool = True,
        brightness_range: Tuple[float, float] = (0.8, 1.2),
        contrast_range: Tuple[float, float] = (0.8, 1.2),
        zoom_range: Tuple[float, float] = (0.8, 1.2),
        apply_probability: float = 0.8
    ):
        """
        Initialize image augmentor.
        
        Args:
            rotation_range: Maximum rotation angle in degrees (±)
            horizontal_flip: Whether to apply random horizontal flips
            brightness_range: Range for brightness adjustment (min, max)
            contrast_range: Range for contrast adjustment (min, max)
            zoom_range: Range for zoom (min, max)
            apply_probability: Probability of applying each augmentation
        """
        self.rotation_range = rotation_range
        self.horizontal_flip = horizontal_flip
        self.brightness_range = brightness_range
        self.contrast_range = contrast_range
        self.zoom_range = zoom_range
        self.apply_probability = apply_probability
    
    def random_rotation(self, image: np.ndarray) -> np.ndarray:
        """
        Apply random rotation to image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Rotated image
        """
        if random.random() > self.apply_probability:
            return image
        
        angle = random.uniform(-self.rotation_range, self.rotation_range)
        
        # Convert to PIL for rotation
        pil_image = Image.fromarray(image.astype('uint8'))
        rotated = pil_image.rotate(angle, resample=Image.BICUBIC, fillcolor=(128, 128, 128))
        
        return np.array(rotated)
    
    def random_horizontal_flip(self, image: np.ndarray) -> np.ndarray:
        """
        Apply random horizontal flip to image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Flipped or original image
        """
        if not self.horizontal_flip:
            return image
        
        if random.random() > self.apply_probability:
            return image
        
        return np.fliplr(image)
    
    def random_brightness(self, image: np.ndarray) -> np.ndarray:
        """
        Apply random brightness adjustment.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Brightness-adjusted image
        """
        if random.random() > self.apply_probability:
            return image
        
        factor = random.uniform(*self.brightness_range)
        
        # Convert to PIL for brightness adjustment
        pil_image = Image.fromarray(image.astype('uint8'))
        enhancer = ImageEnhance.Brightness(pil_image)
        adjusted = enhancer.enhance(factor)
        
        return np.array(adjusted)
    
    def random_contrast(self, image: np.ndarray) -> np.ndarray:
        """
        Apply random contrast adjustment.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Contrast-adjusted image
        """
        if random.random() > self.apply_probability:
            return image
        
        factor = random.uniform(*self.contrast_range)
        
        # Convert to PIL for contrast adjustment
        pil_image = Image.fromarray(image.astype('uint8'))
        enhancer = ImageEnhance.Contrast(pil_image)
        adjusted = enhancer.enhance(factor)
        
        return np.array(adjusted)
    
    def random_zoom(self, image: np.ndarray) -> np.ndarray:
        """
        Apply random zoom (crop and resize).
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Zoomed image
        """
        if random.random() > self.apply_probability:
            return image
        
        zoom_factor = random.uniform(*self.zoom_range)
        
        height, width = image.shape[:2]
        
        # Calculate crop dimensions
        new_height = int(height / zoom_factor)
        new_width = int(width / zoom_factor)
        
        # Calculate crop position (center)
        top = (height - new_height) // 2
        left = (width - new_width) // 2
        
        # Crop
        cropped = image[top:top+new_height, left:left+new_width]
        
        # Resize back to original size
        pil_image = Image.fromarray(cropped.astype('uint8'))
        resized = pil_image.resize((width, height), Image.BICUBIC)
        
        return np.array(resized)
    
    def augment(self, image: np.ndarray) -> np.ndarray:
        """
        Apply all augmentations to an image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Augmented image
        """
        # Apply augmentations in sequence
        image = self.random_rotation(image)
        image = self.random_horizontal_flip(image)
        image = self.random_brightness(image)
        image = self.random_contrast(image)
        image = self.random_zoom(image)
        
        return image


class DataGenerator:
    """
    Data generator for training with augmentation and class balancing.
    
    Generates batches of augmented images for model training.
    """
    
    def __init__(
        self,
        image_paths: List[str],
        labels: List[int],
        batch_size: int = 32,
        target_size: Tuple[int, int] = (224, 224),
        augmentor: ImageAugmentor = None,
        shuffle: bool = True,
        balance_classes: bool = True
    ):
        """
        Initialize data generator.
        
        Args:
            image_paths: List of paths to images
            labels: List of labels (0 or 1)
            batch_size: Batch size
            target_size: Target image size (height, width)
            augmentor: ImageAugmentor instance (None for no augmentation)
            shuffle: Whether to shuffle data
            balance_classes: Whether to balance classes in each batch
        """
        self.image_paths = np.array(image_paths)
        self.labels = np.array(labels)
        self.batch_size = batch_size
        self.target_size = target_size
        self.augmentor = augmentor or ImageAugmentor()
        self.shuffle = shuffle
        self.balance_classes = balance_classes
        
        self.n_samples = len(image_paths)
        self.indices = np.arange(self.n_samples)
        
        # Separate indices by class for balancing
        if balance_classes:
            self.class_0_indices = np.where(self.labels == 0)[0]
            self.class_1_indices = np.where(self.labels == 1)[0]
        
        self.on_epoch_end()
    
    def __len__(self) -> int:
        """Return number of batches per epoch."""
        return int(np.ceil(self.n_samples / self.batch_size))
    
    def __getitem__(self, index: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate one batch of data.
        
        Args:
            index: Batch index
            
        Returns:
            Tuple of (images, labels)
        """
        # Generate batch indices
        if self.balance_classes:
            batch_indices = self._get_balanced_batch_indices()
        else:
            start_idx = index * self.batch_size
            end_idx = min((index + 1) * self.batch_size, self.n_samples)
            batch_indices = self.indices[start_idx:end_idx]
        
        # Generate batch
        batch_images = []
        batch_labels = []
        
        for idx in batch_indices:
            # Load image
            image = self._load_image(self.image_paths[idx])
            
            # Apply augmentation
            if self.augmentor:
                image = self.augmentor.augment(image)
            
            # Normalize
            image = image.astype(np.float32) / 255.0
            
            batch_images.append(image)
            batch_labels.append(self.labels[idx])
        
        return np.array(batch_images), np.array(batch_labels)
    
    def _load_image(self, image_path: str) -> np.ndarray:
        """
        Load and resize an image.
        
        Args:
            image_path: Path to image
            
        Returns:
            Image as numpy array
        """
        image = Image.open(image_path).convert('RGB')
        image = image.resize(self.target_size, Image.BICUBIC)
        return np.array(image)
    
    def _get_balanced_batch_indices(self) -> np.ndarray:
        """
        Get balanced batch indices (equal number from each class).
        
        Returns:
            Array of indices
        """
        half_batch = self.batch_size // 2
        
        # Sample from each class
        class_0_sample = np.random.choice(self.class_0_indices, size=half_batch, replace=True)
        class_1_sample = np.random.choice(self.class_1_indices, size=half_batch, replace=True)
        
        # Combine and shuffle
        batch_indices = np.concatenate([class_0_sample, class_1_sample])
        np.random.shuffle(batch_indices)
        
        return batch_indices
    
    def on_epoch_end(self):
        """Update indices after each epoch."""
        if self.shuffle:
            np.random.shuffle(self.indices)


def create_tf_dataset(
    image_paths: List[str],
    labels: List[int],
    batch_size: int = 32,
    target_size: Tuple[int, int] = (224, 224),
    augment: bool = True,
    shuffle: bool = True
):
    """
    Create a TensorFlow dataset with augmentation.
    
    Args:
        image_paths: List of paths to images
        labels: List of labels (0 or 1)
        batch_size: Batch size
        target_size: Target image size
        augment: Whether to apply augmentation
        shuffle: Whether to shuffle data
        
    Returns:
        TensorFlow dataset
    """
    if not TF_AVAILABLE:
        raise ImportError("TensorFlow is required for create_tf_dataset. Install with: pip install tensorflow")
    
    def load_and_preprocess(path, label):
        """Load and preprocess a single image."""
        # Load image
        image = tf.io.read_file(path)
        image = tf.image.decode_jpeg(image, channels=3)
        
        # Resize
        image = tf.image.resize(image, target_size)
        
        # Normalize
        image = image / 255.0
        
        return image, label
    
    def augment_image(image, label):
        """Apply augmentation to image."""
        # Random rotation (approximate with flips)
        image = tf.image.random_flip_left_right(image)
        
        # Random brightness
        image = tf.image.random_brightness(image, max_delta=0.2)
        
        # Random contrast
        image = tf.image.random_contrast(image, lower=0.8, upper=1.2)
        
        # Random saturation
        image = tf.image.random_saturation(image, lower=0.8, upper=1.2)
        
        # Clip values
        image = tf.clip_by_value(image, 0.0, 1.0)
        
        return image, label
    
    # Create dataset
    dataset = tf.data.Dataset.from_tensor_slices((image_paths, labels))
    
    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(image_paths))
    
    # Load and preprocess
    dataset = dataset.map(load_and_preprocess, num_parallel_calls=tf.data.AUTOTUNE)
    
    # Apply augmentation
    if augment:
        dataset = dataset.map(augment_image, num_parallel_calls=tf.data.AUTOTUNE)
    
    # Batch and prefetch
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(tf.data.AUTOTUNE)
    
    return dataset


def calculate_class_weights(labels: List[int]) -> dict:
    """
    Calculate class weights for imbalanced datasets.
    
    Args:
        labels: List of labels
        
    Returns:
        Dictionary of class weights
    """
    labels_array = np.array(labels)
    n_samples = len(labels_array)
    n_classes = len(np.unique(labels_array))
    
    class_counts = np.bincount(labels_array)
    
    # Calculate weights (inverse frequency)
    weights = n_samples / (n_classes * class_counts)
    
    return {i: weights[i] for i in range(n_classes)}


if __name__ == "__main__":
    # Example usage
    print("Image Augmentation Pipeline")
    print("="*50)
    
    # Create augmentor
    augmentor = ImageAugmentor(
        rotation_range=15.0,
        horizontal_flip=True,
        brightness_range=(0.8, 1.2),
        contrast_range=(0.8, 1.2),
        zoom_range=(0.8, 1.2)
    )
    
    print("✅ Augmentor configured with:")
    print(f"   - Rotation: ±{augmentor.rotation_range}°")
    print(f"   - Horizontal flip: {augmentor.horizontal_flip}")
    print(f"   - Brightness: {augmentor.brightness_range}")
    print(f"   - Contrast: {augmentor.contrast_range}")
    print(f"   - Zoom: {augmentor.zoom_range}")
