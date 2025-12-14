"""
Image preprocessing pipeline for the Fake Product Detection System.

This module handles image validation, quality assessment, and preprocessing
to prepare images for model inference.
"""
import io
from typing import Tuple, Optional
import numpy as np
from PIL import Image
import cv2
from src.config import settings


class ImagePreprocessor:
    """
    Image preprocessing pipeline for product authenticity detection.
    
    Handles validation, quality assessment, and transformation of raw images
    into model-ready format.
    """
    
    def __init__(self, target_size: int = None):
        """
        Initialize the image preprocessor.
        
        Args:
            target_size: Target image size for model input (default from settings)
        """
        self.target_size = target_size or settings.target_image_size
        self.max_file_size = settings.max_file_size_mb * 1024 * 1024  # Convert to bytes
        self.allowed_formats = [fmt.upper() for fmt in settings.allowed_formats]
    
    def validate_image(self, image_bytes: bytes) -> Tuple[bool, str]:
        """
        Validate image file format and size.
        
        Args:
            image_bytes: Raw image file bytes
            
        Returns:
            Tuple of (is_valid, error_message)
            - is_valid: True if image passes validation
            - error_message: Empty string if valid, error description if invalid
        """
        # Check file size
        file_size = len(image_bytes)
        if file_size == 0:
            return False, "Image file is empty"
        
        if file_size > self.max_file_size:
            max_mb = self.max_file_size / (1024 * 1024)
            return False, f"Image file exceeds {max_mb:.0f}MB limit"
        
        # Try to open and validate format
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Check format
            if image.format not in self.allowed_formats:
                allowed = ", ".join(self.allowed_formats)
                return False, f"Unsupported file format: {image.format}. Allowed formats: {allowed}"
            
            # Check if image can be loaded
            image.verify()
            
            # Re-open after verify (verify closes the file)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Check dimensions
            width, height = image.size
            if width < 50 or height < 50:
                return False, "Image dimensions too small (minimum 50x50 pixels)"
            
            if width > 10000 or height > 10000:
                return False, "Image dimensions too large (maximum 10000x10000 pixels)"
            
            # Check mode (should be RGB or convertible to RGB)
            if image.mode not in ['RGB', 'RGBA', 'L', 'P']:
                return False, f"Unsupported image mode: {image.mode}"
            
            return True, ""
            
        except Exception as e:
            return False, f"Unable to decode image file: {str(e)}"
    
    def decode_image(self, image_bytes: bytes) -> Tuple[Optional[np.ndarray], str]:
        """
        Decode image bytes to numpy array.
        
        Args:
            image_bytes: Raw image file bytes
            
        Returns:
            Tuple of (image_array, error_message)
            - image_array: RGB numpy array or None if failed
            - error_message: Empty if successful, error description if failed
        """
        try:
            # Open image with PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert to RGB (handles RGBA, L, P modes)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to numpy array
            image_array = np.array(image)
            
            return image_array, ""
            
        except Exception as e:
            return None, f"Failed to decode image: {str(e)}"
    
    def get_image_format(self, image_bytes: bytes) -> str:
        """
        Get the format of an image file.
        
        Args:
            image_bytes: Raw image file bytes
            
        Returns:
            Image format string (e.g., "JPEG", "PNG") or "UNKNOWN"
        """
        try:
            image = Image.open(io.BytesIO(image_bytes))
            return image.format if image.format else "UNKNOWN"
        except:
            return "UNKNOWN"
    
    def assess_image_quality(self, image: np.ndarray) -> Tuple[float, bool]:
        """
        Assess image quality based on blur detection and glare.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            Tuple of (quality_score, has_glare)
            - quality_score: 0-1, where 1 is highest quality
            - has_glare: True if glare detected
        """
        # Convert to grayscale for analysis
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        # Detect blur using Laplacian variance
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Normalize blur score (higher variance = sharper image)
        # Typical values: <100 = blurry, 100-500 = acceptable, >500 = sharp
        blur_score = min(laplacian_var / 500.0, 1.0)
        
        # Detect glare using brightness analysis
        # Check for very bright regions that might indicate glare
        brightness = np.mean(gray)
        bright_pixels = np.sum(gray > 240) / gray.size
        
        # Glare detected if >5% of pixels are very bright and overall brightness is high
        has_glare = bool((bright_pixels > 0.05) and (brightness > 180))
        
        # Quality score is primarily based on sharpness
        quality_score = blur_score
        
        # Penalize for glare
        if has_glare:
            quality_score *= 0.8
        
        return quality_score, has_glare
    
    def resize_image(self, image: np.ndarray, target_size: Tuple[int, int] = None) -> np.ndarray:
        """
        Resize image to target dimensions.
        
        Args:
            image: RGB image as numpy array
            target_size: Target (width, height) or None to use default
            
        Returns:
            Resized image as numpy array
        """
        if target_size is None:
            target_size = (self.target_size, self.target_size)
        
        # Use PIL for high-quality resizing
        pil_image = Image.fromarray(image)
        resized = pil_image.resize(target_size, Image.Resampling.LANCZOS)
        
        return np.array(resized)
    
    def normalize_lighting(self, image: np.ndarray) -> np.ndarray:
        """
        Normalize lighting using CLAHE (Contrast Limited Adaptive Histogram Equalization).
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            Image with normalized lighting
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
        
        # Split channels
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l_clahe = clahe.apply(l)
        
        # Merge channels
        lab_clahe = cv2.merge([l_clahe, a, b])
        
        # Convert back to RGB
        result = cv2.cvtColor(lab_clahe, cv2.COLOR_LAB2RGB)
        
        return result
    
    def reduce_glare(self, image: np.ndarray) -> np.ndarray:
        """
        Reduce glare using bilateral filtering.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            Image with reduced glare
        """
        # Apply bilateral filter to reduce glare while preserving edges
        # d: diameter of pixel neighborhood
        # sigmaColor: filter sigma in color space
        # sigmaSpace: filter sigma in coordinate space
        result = cv2.bilateralFilter(image, d=9, sigmaColor=75, sigmaSpace=75)
        
        return result
    
    def detect_primary_product(self, image: np.ndarray) -> np.ndarray:
        """
        Detect and crop to primary product in image.
        
        Uses center-crop heuristic assuming product is in center of frame.
        
        Args:
            image: RGB image as numpy array
            
        Returns:
            Cropped image focused on primary product
        """
        height, width = image.shape[:2]
        
        # Use center crop (80% of image)
        crop_ratio = 0.8
        
        new_width = int(width * crop_ratio)
        new_height = int(height * crop_ratio)
        
        left = (width - new_width) // 2
        top = (height - new_height) // 2
        right = left + new_width
        bottom = top + new_height
        
        cropped = image[top:bottom, left:right]
        
        return cropped
    
    def normalize_pixels(self, image: np.ndarray, method: str = "standard") -> np.ndarray:
        """
        Normalize pixel values.
        
        Args:
            image: RGB image as numpy array (0-255)
            method: "standard" for ImageNet stats, "simple" for [0,1] scaling
            
        Returns:
            Normalized image as float array
        """
        # Convert to float
        image_float = image.astype(np.float32)
        
        if method == "simple":
            # Scale to [0, 1]
            return image_float / 255.0
        
        elif method == "standard":
            # ImageNet normalization
            # Mean: [0.485, 0.456, 0.406]
            # Std: [0.229, 0.224, 0.225]
            mean = np.array([0.485, 0.456, 0.406], dtype=np.float32) * 255.0
            std = np.array([0.229, 0.224, 0.225], dtype=np.float32) * 255.0
            
            normalized = (image_float - mean) / std
            
            return normalized.astype(np.float32)
        
        else:
            raise ValueError(f"Unknown normalization method: {method}")
    
    def preprocess(
        self,
        image_bytes: bytes,
        apply_lighting_norm: bool = True,
        apply_glare_reduction: bool = True,
        detect_product: bool = False
    ) -> Tuple[Optional[np.ndarray], dict, str]:
        """
        Complete preprocessing pipeline.
        
        Args:
            image_bytes: Raw image file bytes
            apply_lighting_norm: Whether to apply lighting normalization
            apply_glare_reduction: Whether to apply glare reduction
            detect_product: Whether to detect and crop to primary product
            
        Returns:
            Tuple of (preprocessed_image, metadata, error_message)
            - preprocessed_image: Preprocessed image ready for model or None if failed
            - metadata: Dictionary with preprocessing information
            - error_message: Empty if successful, error description if failed
        """
        # Validate image
        is_valid, error = self.validate_image(image_bytes)
        if not is_valid:
            return None, {}, error
        
        # Decode image
        image, error = self.decode_image(image_bytes)
        if image is None:
            return None, {}, error
        
        # Store original dimensions
        original_height, original_width = image.shape[:2]
        
        # Get format
        image_format = self.get_image_format(image_bytes)
        
        # Assess quality
        quality_score, has_glare = self.assess_image_quality(image)
        
        # Track preprocessing steps
        preprocessing_applied = []
        
        # Apply glare reduction if needed
        if apply_glare_reduction and has_glare:
            image = self.reduce_glare(image)
            preprocessing_applied.append("glare_reduction")
        
        # Apply lighting normalization
        if apply_lighting_norm:
            image = self.normalize_lighting(image)
            preprocessing_applied.append("lighting_normalization")
        
        # Detect primary product
        if detect_product:
            image = self.detect_primary_product(image)
            preprocessing_applied.append("product_detection")
        
        # Resize to target size
        image = self.resize_image(image)
        preprocessing_applied.append("resize")
        
        # Normalize pixels
        image = self.normalize_pixels(image, method="simple")
        preprocessing_applied.append("normalize")
        
        # Build metadata
        metadata = {
            "original_width": original_width,
            "original_height": original_height,
            "file_format": image_format,
            "file_size_bytes": len(image_bytes),
            "quality_score": float(quality_score),
            "has_glare": bool(has_glare),
            "preprocessing_applied": preprocessing_applied
        }
        
        return image, metadata, ""
