"""
Create Sample Product Images Dataset

This script creates sample images locally for testing the system.
No internet connection required.

Run: python create_sample_dataset.py
"""
import numpy as np
import cv2
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

def create_directories():
    """Create the data directory structure."""
    print("📁 Creating directory structure...")
    
    dirs = [
        "data/train/original",
        "data/train/fake",
        "data/val/original",
        "data/val/fake",
        "data/test/original",
        "data/test/fake"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {dir_path}")
    
    return dirs

def create_sample_image(category, index, quality="high"):
    """
    Create a sample product image.
    
    Args:
        category: "original" or "fake"
        index: Image number
        quality: "high" or "low" (simulates authentic vs counterfeit)
    """
    # Create base image
    img = np.ones((500, 500, 3), dtype=np.uint8) * 255
    
    # Color scheme
    if category == "original":
        # Green tones for original
        color = (100, 200, 100)  # BGR
        text_color = (0, 100, 0)
    else:
        # Red tones for fake
        color = (100, 100, 200)  # BGR
        text_color = (0, 0, 150)
    
    # Add colored background
    img[:, :] = color
    
    # Add "product" rectangle (simulating packaging)
    cv2.rectangle(img, (100, 100), (400, 400), (255, 255, 255), -1)
    cv2.rectangle(img, (100, 100), (400, 400), (0, 0, 0), 3)
    
    # Add "logo" circle
    center = (250, 200)
    radius = 50
    cv2.circle(img, center, radius, text_color, -1)
    cv2.circle(img, center, radius, (0, 0, 0), 2)
    
    # Add text (simulating product name)
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = category.upper()
    
    if quality == "low":
        # Simulate poor quality for fake products
        # Add blur
        img = cv2.GaussianBlur(img, (5, 5), 0)
        # Reduce contrast
        img = cv2.convertScaleAbs(img, alpha=0.8, beta=20)
    
    # Add text
    cv2.putText(img, text, (150, 280), font, 1, text_color, 2, cv2.LINE_AA)
    cv2.putText(img, f"#{index}", (220, 320), font, 0.7, text_color, 2, cv2.LINE_AA)
    
    # Add some noise for realism
    noise = np.random.randint(0, 20, img.shape, dtype=np.uint8)
    img = cv2.add(img, noise)
    
    return img

def create_dataset():
    """Create sample dataset with images."""
    print("\n🎨 Creating sample images...")
    
    # Number of images per split
    n_train = 10
    n_val = 3
    n_test = 2
    
    stats = {
        "train": {"original": 0, "fake": 0},
        "val": {"original": 0, "fake": 0},
        "test": {"original": 0, "fake": 0}
    }
    
    # Create training images
    print("\n   Creating training images...")
    for i in range(1, n_train + 1):
        # Original
        img = create_sample_image("original", i, quality="high")
        cv2.imwrite(f"data/train/original/original_{i}.png", img)
        stats["train"]["original"] += 1
        
        # Fake
        img = create_sample_image("fake", i, quality="low")
        cv2.imwrite(f"data/train/fake/fake_{i}.png", img)
        stats["train"]["fake"] += 1
    
    print(f"   ✓ Created {n_train} original + {n_train} fake training images")
    
    # Create validation images
    print("\n   Creating validation images...")
    for i in range(1, n_val + 1):
        # Original
        img = create_sample_image("original", i + 100, quality="high")
        cv2.imwrite(f"data/val/original/original_{i}.png", img)
        stats["val"]["original"] += 1
        
        # Fake
        img = create_sample_image("fake", i + 100, quality="low")
        cv2.imwrite(f"data/val/fake/fake_{i}.png", img)
        stats["val"]["fake"] += 1
    
    print(f"   ✓ Created {n_val} original + {n_val} fake validation images")
    
    # Create test images
    print("\n   Creating test images...")
    for i in range(1, n_test + 1):
        # Original
        img = create_sample_image("original", i + 200, quality="high")
        cv2.imwrite(f"data/test/original/original_{i}.png", img)
        stats["test"]["original"] += 1
        
        # Fake
        img = create_sample_image("fake", i + 200, quality="low")
        cv2.imwrite(f"data/test/fake/fake_{i}.png", img)
        stats["test"]["fake"] += 1
    
    print(f"   ✓ Created {n_test} original + {n_test} fake test images")
    
    return stats

def print_summary(stats):
    """Print dataset summary."""
    print("\n" + "="*70)
    print("  📊 DATASET CREATED")
    print("="*70)
    
    print("\n  Training Set:")
    print(f"    Original: {stats['train']['original']} images")
    print(f"    Fake:     {stats['train']['fake']} images")
    print(f"    Total:    {stats['train']['original'] + stats['train']['fake']} images")
    
    print("\n  Validation Set:")
    print(f"    Original: {stats['val']['original']} images")
    print(f"    Fake:     {stats['val']['fake']} images")
    print(f"    Total:    {stats['val']['original'] + stats['val']['fake']} images")
    
    print("\n  Test Set:")
    print(f"    Original: {stats['test']['original']} images")
    print(f"    Fake:     {stats['test']['fake']} images")
    print(f"    Total:    {stats['test']['original'] + stats['test']['fake']} images")
    
    total = sum(stats['train'].values()) + sum(stats['val'].values()) + sum(stats['test'].values())
    print(f"\n  📦 Total Images: {total}")
    
    print("\n" + "="*70)
    print("  ⚠️  IMPORTANT: SAMPLE IMAGES ONLY")
    print("="*70)
    print("\n  These are synthetic images for testing the system.")
    print("  They are NOT real product photos.")
    
    print("\n  🎯 What You Can Do Now:")
    print("    1. Test the preprocessing: python backend/src/preprocessor.py")
    print("    2. Test data loading: python backend/src/data_collection.py")
    print("    3. Test augmentation: python backend/src/data_augmentation.py")
    print("    4. Try training (will work but won't be accurate)")
    
    print("\n  📸 For Real Product Detection:")
    print("    1. Replace these images with real product photos")
    print("    2. Collect 500-1000 images per category")
    print("    3. Use actual authentic and counterfeit products")
    print("    4. Ensure high-quality, clear images")
    
    print("\n  📂 Dataset Location:")
    print("    data/train/  - Training images")
    print("    data/val/    - Validation images")
    print("    data/test/   - Test images")
    
    print()

def create_readme():
    """Create README file."""
    readme = """# Sample Product Images Dataset

## ⚠️ IMPORTANT

These are **SYNTHETIC SAMPLE IMAGES** created for testing the system infrastructure.
They are NOT real product photos and will NOT provide accurate detection results.

## What's Included

- **30 images total**
  - 10 training images per class (20 total)
  - 3 validation images per class (6 total)
  - 2 test images per class (4 total)

## Image Characteristics

- **Original images**: High quality, clear, good contrast
- **Fake images**: Lower quality, blurred, reduced contrast

## Purpose

These images allow you to:
- ✅ Test the preprocessing pipeline
- ✅ Test data loading and augmentation
- ✅ Run the training script (for testing)
- ✅ Verify the system infrastructure

## For Real Product Detection

Replace these images with:
1. **Real product photographs**
   - Authentic product packaging
   - Counterfeit product packaging

2. **Sufficient quantity**
   - Minimum: 500 images per category
   - Recommended: 1000+ images per category

3. **High quality**
   - Clear, well-lit photos
   - Shows logos, text, packaging details
   - Multiple angles

4. **Balanced dataset**
   - Equal number of original and fake images
   - Diverse product types

## Next Steps

1. Test the system with these sample images
2. Collect real product photos
3. Replace sample images with real ones
4. Train the model for actual detection

## Directory Structure

```
data/
├── train/
│   ├── original/  (10 images)
│   └── fake/      (10 images)
├── val/
│   ├── original/  (3 images)
│   └── fake/      (3 images)
└── test/
    ├── original/  (2 images)
    └── fake/      (2 images)
```
"""
    
    with open("data/README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    
    print("   ✓ Created data/README.md")

def main():
    """Main function."""
    print("\n" + "="*70)
    print("  🎨 CREATE SAMPLE PRODUCT IMAGES DATASET")
    print("="*70)
    print("\n  This will create synthetic sample images for testing.")
    print("  No internet connection required.")
    print()
    
    try:
        # Create directories
        create_directories()
        
        # Create sample images
        stats = create_dataset()
        
        # Create README
        print()
        create_readme()
        
        # Print summary
        print_summary(stats)
        
        print("  ✅ DATASET CREATED SUCCESSFULLY!")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
