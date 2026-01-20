"""
Simple Data Augmentation Script (No Complex Imports)

This script creates augmented versions of your images to increase dataset size.
Uses only PIL and numpy - no complex imports needed.

Usage:
    python augment_dataset_simple.py [num_augmentations]
    
Example:
    python augment_dataset_simple.py 20
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageEnhance
import random


def augment_image(image, augmentation_level='medium'):
    """
    Apply random augmentations to an image.
    
    Args:
        image: PIL Image
        augmentation_level: 'light', 'medium', or 'aggressive'
    
    Returns:
        Augmented PIL Image
    """
    # Convert to numpy for some operations
    img_array = np.array(image)
    
    # Set augmentation ranges based on level
    if augmentation_level == 'light':
        rotation_range = 10
        brightness_range = (0.9, 1.1)
        contrast_range = (0.9, 1.1)
    elif augmentation_level == 'aggressive':
        rotation_range = 40
        brightness_range = (0.6, 1.4)
        contrast_range = (0.6, 1.4)
    else:  # medium
        rotation_range = 25
        brightness_range = (0.7, 1.3)
        contrast_range = (0.7, 1.3)
    
    # 1. Random rotation
    if random.random() > 0.3:
        angle = random.uniform(-rotation_range, rotation_range)
        image = image.rotate(angle, resample=Image.BICUBIC, fillcolor=(128, 128, 128))
    
    # 2. Random horizontal flip
    if random.random() > 0.5:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    
    # 3. Random brightness
    if random.random() > 0.3:
        factor = random.uniform(*brightness_range)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(factor)
    
    # 4. Random contrast
    if random.random() > 0.3:
        factor = random.uniform(*contrast_range)
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(factor)
    
    # 5. Random zoom (crop and resize)
    if random.random() > 0.4:
        width, height = image.size
        zoom_factor = random.uniform(0.8, 1.2)
        
        new_width = int(width / zoom_factor)
        new_height = int(height / zoom_factor)
        
        # Calculate crop position (center with small random offset)
        left = (width - new_width) // 2 + random.randint(-10, 10)
        top = (height - new_height) // 2 + random.randint(-10, 10)
        
        # Ensure crop is within bounds
        left = max(0, min(left, width - new_width))
        top = max(0, min(top, height - new_height))
        
        # Crop and resize
        image = image.crop((left, top, left + new_width, top + new_height))
        image = image.resize((width, height), Image.BICUBIC)
    
    return image


def augment_directory(input_dir, output_dir, num_augmentations=10, augmentation_level='medium'):
    """
    Create augmented versions of all images in a directory.
    
    Args:
        input_dir: Directory containing original images
        output_dir: Directory to save augmented images
        num_augmentations: Number of augmented versions per image
        augmentation_level: 'light', 'medium', or 'aggressive'
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"❌ Input directory not found: {input_dir}")
        return 0
    
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
        return 0
    
    print(f"📁 Found {len(image_files)} images")
    print(f"🔄 Creating {num_augmentations} augmented versions per image...")
    
    total_created = 0
    
    for img_file in image_files:
        try:
            # Load image
            image = Image.open(img_file).convert('RGB')
            
            # Save original to output directory
            original_output = output_path / img_file.name
            image.save(original_output, quality=95)
            
            # Create augmented versions
            for i in range(num_augmentations):
                augmented = augment_image(image, augmentation_level)
                
                # Save with suffix
                stem = img_file.stem
                ext = img_file.suffix
                aug_filename = f"{stem}_aug{i+1:03d}{ext}"
                aug_path = output_path / aug_filename
                
                augmented.save(aug_path, quality=95)
                total_created += 1
                
                # Progress indicator
                if (total_created) % 10 == 0:
                    print(f"   Created {total_created} augmented images...")
        
        except Exception as e:
            print(f"⚠️  Error processing {img_file.name}: {e}")
            continue
    
    print(f"✅ Created {total_created} augmented images")
    print(f"📊 Total images in output: {len(image_files) + total_created}")
    
    return total_created


def main():
    """Main function to augment the entire dataset."""
    print("\n" + "="*70)
    print("  🔄 DATASET AUGMENTATION (Simple Version)")
    print("="*70)
    
    # Get number of augmentations from command line
    if len(sys.argv) > 1:
        try:
            num_aug = int(sys.argv[1])
        except ValueError:
            print("❌ Invalid number. Usage: python augment_dataset_simple.py [num]")
            print("   Example: python augment_dataset_simple.py 20")
            return 1
    else:
        num_aug = 10  # Default
    
    print(f"\n  Creating {num_aug} augmented versions per image")
    print(f"  Augmentation level: medium")
    print()
    
    # Determine augmentation level based on count
    if num_aug <= 10:
        aug_level = 'light'
    elif num_aug <= 30:
        aug_level = 'medium'
    else:
        aug_level = 'aggressive'
    
    print(f"  Using '{aug_level}' augmentation settings")
    print()
    
    total_augmented = 0
    
    # Augment training data
    print("="*70)
    print("  AUGMENTING TRAINING DATA")
    print("="*70)
    
    for class_name in ['original', 'fake']:
        input_dir = f"data/train/{class_name}"
        output_dir = f"data/train_augmented/{class_name}"
        
        print(f"\n📂 Processing: {class_name}")
        count = augment_directory(input_dir, output_dir, num_aug, aug_level)
        total_augmented += count
    
    # Augment validation data (fewer augmentations)
    print("\n" + "="*70)
    print("  AUGMENTING VALIDATION DATA")
    print("="*70)
    
    val_aug = max(1, num_aug // 3)  # Use 1/3 of training augmentations
    print(f"  Using {val_aug} augmentations for validation data")
    print()
    
    for class_name in ['original', 'fake']:
        input_dir = f"data/val/{class_name}"
        output_dir = f"data/val_augmented/{class_name}"
        
        print(f"\n📂 Processing: {class_name}")
        count = augment_directory(input_dir, output_dir, val_aug, 'light')
        total_augmented += count
    
    # Summary
    print("\n" + "="*70)
    print("  ✅ AUGMENTATION COMPLETE")
    print("="*70)
    print(f"\n  📊 Statistics:")
    print(f"     Total augmented images created: {total_augmented}")
    print(f"     Augmentation level: {aug_level}")
    
    print(f"\n  📁 Augmented data saved to:")
    print(f"     - data/train_augmented/original/")
    print(f"     - data/train_augmented/fake/")
    print(f"     - data/val_augmented/original/")
    print(f"     - data/val_augmented/fake/")
    
    print(f"\n  🚀 Next steps:")
    print(f"     1. Check augmented images to verify quality")
    print(f"     2. Update train.py:")
    print(f"        TRAIN_DIR = 'data/train_augmented'")
    print(f"        VAL_DIR = 'data/val_augmented'")
    print(f"     3. Train the model: python train.py")
    print()
    
    return 0


if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Augmentation cancelled by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
