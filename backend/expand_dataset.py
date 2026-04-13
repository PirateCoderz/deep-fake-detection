"""
Dataset Expansion Script for Fake Product Detection.

Takes the existing 20 training images (10 original, 10 fake) and creates
augmented copies to expand the dataset to 500+ images per class.

Augmentations include:
- Rotation (±15°, ±30°)
- Horizontal flip
- Brightness variations (brighter/darker)
- Contrast variations
- Zoom (crop and resize)
- Gaussian noise
- Color jitter
- Combined augmentations

This ensures the model has sufficient training data for meaningful results.
"""
import os
import sys
import random
import numpy as np
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

# Configuration
AUGMENTATIONS_PER_IMAGE = 50  # Each image generates 50 variants → 500+ per class
TARGET_SIZE = (224, 224)
RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)


def rotate_image(img, angle):
    """Rotate image by given angle with white background fill."""
    return img.rotate(angle, resample=Image.BICUBIC, expand=False, fillcolor=(255, 255, 255))


def flip_horizontal(img):
    """Flip image horizontally."""
    return ImageOps.mirror(img)


def flip_vertical(img):
    """Flip image vertically."""
    return ImageOps.flip(img)


def adjust_brightness(img, factor):
    """Adjust brightness. factor > 1 = brighter, < 1 = darker."""
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)


def adjust_contrast(img, factor):
    """Adjust contrast."""
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)


def adjust_saturation(img, factor):
    """Adjust color saturation."""
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)


def adjust_sharpness(img, factor):
    """Adjust sharpness."""
    enhancer = ImageEnhance.Sharpness(img)
    return enhancer.enhance(factor)


def add_gaussian_noise(img, intensity=20):
    """Add gaussian noise to image."""
    arr = np.array(img).astype(np.float32)
    noise = np.random.normal(0, intensity, arr.shape)
    arr = np.clip(arr + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(arr)


def random_crop_and_resize(img, crop_fraction=0.85):
    """Randomly crop a portion of the image and resize back."""
    w, h = img.size
    new_w = int(w * crop_fraction)
    new_h = int(h * crop_fraction)
    
    left = random.randint(0, w - new_w)
    top = random.randint(0, h - new_h)
    
    cropped = img.crop((left, top, left + new_w, top + new_h))
    return cropped.resize((w, h), Image.BICUBIC)


def apply_blur(img, radius=1):
    """Apply slight gaussian blur."""
    return img.filter(ImageFilter.GaussianBlur(radius=radius))


def perspective_transform(img):
    """Apply a slight perspective distortion."""
    w, h = img.size
    # Small random perspective coefficients
    offset = random.randint(5, 15)
    coeffs = [
        random.uniform(-0.0005, 0.0005),
        random.uniform(-0.0005, 0.0005),
        random.randint(-offset, offset),
        random.uniform(-0.0005, 0.0005),
        random.uniform(-0.0005, 0.0005),
        random.randint(-offset, offset),
        random.uniform(-0.000005, 0.000005),
        random.uniform(-0.000005, 0.000005),
    ]
    return img.transform((w, h), Image.PERSPECTIVE, coeffs, Image.BICUBIC, fillcolor=(255, 255, 255))


def generate_augmented_image(img, aug_index):
    """
    Generate a single augmented version of the image.
    Uses a deterministic combination based on aug_index for reproducibility.
    """
    result = img.copy()
    
    # Choose augmentation strategy based on index
    strategy = aug_index % 10
    
    if strategy == 0:
        # Rotation only
        angle = random.choice([-30, -20, -15, -10, -5, 5, 10, 15, 20, 30])
        result = rotate_image(result, angle)
    
    elif strategy == 1:
        # Horizontal flip + slight rotation
        result = flip_horizontal(result)
        angle = random.uniform(-10, 10)
        result = rotate_image(result, angle)
    
    elif strategy == 2:
        # Brightness + contrast adjustment
        brightness = random.uniform(0.6, 1.4)
        contrast = random.uniform(0.7, 1.3)
        result = adjust_brightness(result, brightness)
        result = adjust_contrast(result, contrast)
    
    elif strategy == 3:
        # Random crop + resize
        crop_frac = random.uniform(0.7, 0.95)
        result = random_crop_and_resize(result, crop_frac)
    
    elif strategy == 4:
        # Add noise + blur
        noise_intensity = random.randint(10, 30)
        result = add_gaussian_noise(result, noise_intensity)
        if random.random() > 0.5:
            result = apply_blur(result, radius=random.uniform(0.5, 1.5))
    
    elif strategy == 5:
        # Saturation + sharpness
        sat = random.uniform(0.5, 1.5)
        sharp = random.uniform(0.5, 2.0)
        result = adjust_saturation(result, sat)
        result = adjust_sharpness(result, sharp)
    
    elif strategy == 6:
        # Flip + brightness + crop
        result = flip_horizontal(result)
        result = adjust_brightness(result, random.uniform(0.7, 1.3))
        result = random_crop_and_resize(result, random.uniform(0.8, 0.95))
    
    elif strategy == 7:
        # Rotation + noise + contrast
        result = rotate_image(result, random.uniform(-25, 25))
        result = add_gaussian_noise(result, random.randint(5, 20))
        result = adjust_contrast(result, random.uniform(0.8, 1.2))
    
    elif strategy == 8:
        # Perspective + brightness
        try:
            result = perspective_transform(result)
        except Exception:
            result = rotate_image(result, random.uniform(-15, 15))
        result = adjust_brightness(result, random.uniform(0.8, 1.2))
    
    elif strategy == 9:
        # Full combo: flip + rotate + brightness + noise
        if random.random() > 0.5:
            result = flip_horizontal(result)
        result = rotate_image(result, random.uniform(-20, 20))
        result = adjust_brightness(result, random.uniform(0.7, 1.3))
        result = add_gaussian_noise(result, random.randint(5, 15))
    
    # Ensure correct size
    if result.size != TARGET_SIZE:
        result = result.resize(TARGET_SIZE, Image.BICUBIC)
    
    return result


def expand_dataset(data_dir="data"):
    """
    Expand the dataset by generating augmented images.
    
    Directory structure:
    data/
    ├── train/
    │   ├── original/  (10 images → 500+)
    │   └── fake/      (10 images → 500+)
    ├── val/
    │   ├── original/
    │   └── fake/
    └── test/
        ├── original/
        └── fake/
    """
    base_path = Path(data_dir)
    
    splits = ["train", "val", "test"]
    categories = ["original", "fake"]
    
    # Ensure all directories exist
    for split in splits:
        for cat in categories:
            dir_path = base_path / split / cat
            dir_path.mkdir(parents=True, exist_ok=True)
    
    total_generated = 0
    
    for split in splits:
        for cat in categories:
            source_dir = base_path / split / cat
            
            # Find existing source images
            source_images = []
            for ext in ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp"]:
                source_images.extend(source_dir.glob(ext))
            
            if not source_images:
                print(f"  ⚠️  No images found in {source_dir}")
                continue
            
            # Filter out already-augmented images
            original_images = [
                img for img in source_images 
                if "_aug_" not in img.stem
            ]
            
            if not original_images:
                print(f"  ⚠️  No original (non-augmented) images in {source_dir}")
                continue
            
            # Calculate augmentations needed
            if split == "train":
                augs_per_image = AUGMENTATIONS_PER_IMAGE  # 50 per image
            elif split == "val":
                augs_per_image = 10  # Fewer for validation
            else:
                augs_per_image = 5  # Minimal for test
            
            print(f"\n📁 {split}/{cat}: {len(original_images)} source images → generating {len(original_images) * augs_per_image} augmented images...")
            
            count = 0
            for img_path in original_images:
                try:
                    img = Image.open(img_path).convert("RGB")
                    img = img.resize(TARGET_SIZE, Image.BICUBIC)
                    
                    for aug_i in range(augs_per_image):
                        aug_img = generate_augmented_image(img, aug_i)
                        
                        # Save augmented image
                        aug_filename = f"{img_path.stem}_aug_{aug_i:03d}.png"
                        aug_path = source_dir / aug_filename
                        aug_img.save(aug_path, "PNG")
                        count += 1
                        
                except Exception as e:
                    print(f"  ❌ Error processing {img_path.name}: {e}")
            
            total_generated += count
            print(f"  ✅ Generated {count} augmented images in {source_dir}")
    
    return total_generated


def print_dataset_stats(data_dir="data"):
    """Print the final dataset statistics."""
    base_path = Path(data_dir)
    
    print("\n" + "=" * 60)
    print("📊 DATASET STATISTICS")
    print("=" * 60)
    
    total = 0
    for split in ["train", "val", "test"]:
        print(f"\n  {split.upper()}:")
        for cat in ["original", "fake"]:
            dir_path = base_path / split / cat
            if dir_path.exists():
                images = list(dir_path.glob("*.png")) + list(dir_path.glob("*.jpg")) + list(dir_path.glob("*.jpeg"))
                count = len(images)
                total += count
                print(f"    {cat:>10}: {count:>5} images")
            else:
                print(f"    {cat:>10}:     0 images (directory missing)")
    
    print(f"\n  {'TOTAL':>12}: {total:>5} images")
    print("=" * 60)


def main():
    """Main entry point."""
    # Determine data directory
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        print("   Please ensure the data/ directory exists with train/original and train/fake folders.")
        sys.exit(1)
    
    print("=" * 60)
    print("🔧 FAKE PRODUCT DETECTION - DATASET EXPANSION")
    print("=" * 60)
    print(f"\nData directory: {data_dir}")
    print(f"Augmentations per training image: {AUGMENTATIONS_PER_IMAGE}")
    print(f"Target image size: {TARGET_SIZE}")
    
    # Show current stats
    print("\n📊 BEFORE EXPANSION:")
    print_dataset_stats(str(data_dir))
    
    # Expand the dataset
    print("\n🚀 EXPANDING DATASET...")
    total = expand_dataset(str(data_dir))
    
    # Show final stats
    print(f"\n✅ EXPANSION COMPLETE: {total} new images generated")
    print("\n📊 AFTER EXPANSION:")
    print_dataset_stats(str(data_dir))
    
    print("\n💡 TIP: You can also add more real images from Kaggle datasets like:")
    print("   - 'Fake and Real Product Image Dataset'")
    print("   - 'Product Authenticity Dataset'")
    print("   Place them in data/train/original/ and data/train/fake/")


if __name__ == "__main__":
    main()
