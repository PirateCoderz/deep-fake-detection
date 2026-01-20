"""
Data Augmentation Script

This script creates augmented versions of your images to increase dataset size.
Use this as a temporary solution until you can collect more real images.

Usage:
    python augment_dataset.py
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
import random

# Add backend to path
backend_src = str(Path(__file__).parent.parent.parent / 'backend' / 'src')
if backend_src not in sys.path:
    sys.path.insert(0, backend_src)

try:
    from data_augmentation import ImageAugmentor
except ImportError:
    print("⚠️  Warning: Could not import ImageAugmentor")
    print("   Make sure you're in the project root directory")
    print("   Or install dependencies: pip install -r backend/requirements.txt")
    sys.exit(1)


def augment_directory(input_dir: str, output_dir: str, num_augmentations: int = 10):
    """
    Create augmented versions of all images in a directory.
    
    Args:
        input_dir: Directory containing original images
        output_dir: Directory to save augmented images
        num_augmentations: Number of augmented versions per image
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return
    
    # Create output directory
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all images
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(input_path.glob(f"*{ext}"))
        image_files.extend(input_path.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"❌ No images found in: {input_dir}")
        return
    
    print(f"📁 Found {len(image_files)} images in {input_dir}")
    print(f"🔄 Creating {num_augmentations} augmented versions per image...")
    
    # Create augmentor with aggressive settings
    augmentor = ImageAugmentor(
        rotation_range=30.0,      # More rotation
        horizontal_flip=True,
        brightness_range=(0.7, 1.3),  # More brightness variation
        contrast_range=(0.7, 1.3),    # More contrast variation
        zoom_range=(0.7, 1.3)         # More zoom variation
    )
    
    total_created = 0
    
    for img_file in image_files:
        # Load image
        image = np.array(Image.open(img_file))
        
        # Copy original
        original_output = output_path / img_file.name
        Image.fromarray(image).save(original_output)
        
        # Create augmented versions
        for i in range(num_augmentations):
            augmented = augmentor.augment(image)
            
            # Save with suffix
            stem = img_file.stem
            ext = img_file.suffix
            aug_filename = f"{stem}_aug{i+1}{ext}"
            aug_path = output_path / aug_filename
            
            Image.fromarray(augmented).save(aug_path)
            total_created += 1
    
    print(f"✅ Created {total_created} augmented images")
    print(f"📁 Saved to: {output_dir}")
    print(f"📊 Total images: {len(image_files) + total_created}")


def augment_full_dataset(num_augmentations: int = 10):
    """Augment the entire dataset (train, val, test)."""
    print("\n" + "="*70)
    print("  🔄 DATASET AUGMENTATION")
    print("="*70)
    print(f"\n  Creating {num_augmentations} augmented versions per image")
    print(f"  This will significantly increase your dataset size")
    print()
    
    # Augment training data
    print("\n" + "="*70)
    print("  AUGMENTING TRAINING DATA")
    print("="*70)
    
    for class_name in ['original', 'fake']:
        input_dir = f"data/train/{class_name}"
        output_dir = f"data/train_augmented/{class_name}"
        
        print(f"\n📂 Processing: {class_name}")
        augment_directory(input_dir, output_dir, num_augmentations)
    
    # Augment validation data (fewer augmentations)
    print("\n" + "="*70)
    print("  AUGMENTING VALIDATION DATA")
    print("="*70)
    
    for class_name in ['original', 'fake']:
        input_dir = f"data/val/{class_name}"
        output_dir = f"data/val_augmented/{class_name}"
        
        print(f"\n📂 Processing: {class_name}")
        augment_directory(input_dir, output_dir, num_augmentations // 2)
    
    # Don't augment test data (keep it original)
    print("\n" + "="*70)
    print("  ℹ️  Test data not augmented (keeping original for fair evaluation)")
    print("="*70)
    
    print("\n" + "="*70)
    print("  ✅ AUGMENTATION COMPLETE")
    print("="*70)
    print("\n  📁 Augmented data saved to:")
    print("     - data/train_augmented/")
    print("     - data/val_augmented/")
    print("\n  🚀 Next steps:")
    print("     1. Update train.py to use augmented directories:")
    print("        TRAIN_DIR = 'data/train_augmented'")
    print("        VAL_DIR = 'data/val_augmented'")
    print("     2. Retrain the model: python train.py")
    print()


if __name__ == "__main__":
    # Check if user wants custom augmentation count
    if len(sys.argv) > 1:
        try:
            num_aug = int(sys.argv[1])
        except ValueError:
            print("Usage: python augment_dataset.py [num_augmentations]")
            print("Example: python augment_dataset.py 20")
            sys.exit(1)
    else:
        num_aug = 10  # Default
    
    augment_full_dataset(num_aug)
