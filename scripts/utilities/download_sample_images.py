"""
Download Sample Product Images for Testing

This script downloads sample product images and organizes them into:
- data/train/original/
- data/train/fake/
- data/val/original/
- data/val/fake/
- data/test/original/
- data/test/fake/

Run: python download_sample_images.py
"""
import os
import urllib.request
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

from data_collection import DatasetOrganizer

def create_directory_structure():
    """Create the data directory structure."""
    print("📁 Creating directory structure...")
    
    organizer = DatasetOrganizer(base_dir="data")
    
    # Create directories
    dirs = [
        "data/train/original",
        "data/train/fake",
        "data/val/original",
        "data/val/fake",
        "data/test/original",
        "data/test/fake",
        "data/raw"
    ]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"   ✓ Created {dir_path}")
    
    return organizer

def download_image(url, filepath):
    """Download an image from URL."""
    try:
        urllib.request.urlretrieve(url, filepath)
        return True
    except Exception as e:
        print(f"   ⚠️  Failed to download {url}: {e}")
        return False

def download_sample_images():
    """Download sample product images from free sources."""
    print("\n📥 Downloading sample images...")
    print("   Note: Using placeholder images for demonstration")
    
    # Sample image URLs (using placeholder services)
    # In production, you would use real product images
    sample_urls = {
        "original": [
            "https://via.placeholder.com/500x500/4CAF50/FFFFFF?text=Original+Product+1",
            "https://via.placeholder.com/500x500/2196F3/FFFFFF?text=Original+Product+2",
            "https://via.placeholder.com/500x500/FF9800/FFFFFF?text=Original+Product+3",
            "https://via.placeholder.com/500x500/9C27B0/FFFFFF?text=Original+Product+4",
            "https://via.placeholder.com/500x500/00BCD4/FFFFFF?text=Original+Product+5",
        ],
        "fake": [
            "https://via.placeholder.com/500x500/F44336/FFFFFF?text=Fake+Product+1",
            "https://via.placeholder.com/500x500/E91E63/FFFFFF?text=Fake+Product+2",
            "https://via.placeholder.com/500x500/FF5722/FFFFFF?text=Fake+Product+3",
            "https://via.placeholder.com/500x500/795548/FFFFFF?text=Fake+Product+4",
            "https://via.placeholder.com/500x500/607D8B/FFFFFF?text=Fake+Product+5",
        ]
    }
    
    downloaded = {"original": 0, "fake": 0}
    
    # Download original images
    print("\n   Downloading original product images...")
    for i, url in enumerate(sample_urls["original"], 1):
        filepath = f"data/raw/original_{i}.png"
        if download_image(url, filepath):
            print(f"   ✓ Downloaded original_{i}.png")
            downloaded["original"] += 1
    
    # Download fake images
    print("\n   Downloading fake product images...")
    for i, url in enumerate(sample_urls["fake"], 1):
        filepath = f"data/raw/fake_{i}.png"
        if download_image(url, filepath):
            print(f"   ✓ Downloaded fake_{i}.png")
            downloaded["fake"] += 1
    
    return downloaded

def organize_images():
    """Organize downloaded images into train/val/test splits."""
    print("\n📊 Organizing images into train/val/test splits...")
    
    import shutil
    
    # Get all downloaded images
    raw_dir = Path("data/raw")
    original_images = list(raw_dir.glob("original_*.png"))
    fake_images = list(raw_dir.glob("fake_*.png"))
    
    def split_and_copy(images, category):
        """Split images into train/val/test (70/15/15)."""
        n = len(images)
        train_n = int(n * 0.7)
        val_n = int(n * 0.15)
        
        # Train
        for i, img in enumerate(images[:train_n], 1):
            dest = f"data/train/{category}/{category}_{i}.png"
            shutil.copy(img, dest)
        
        # Val
        for i, img in enumerate(images[train_n:train_n+val_n], 1):
            dest = f"data/val/{category}/{category}_{i}.png"
            shutil.copy(img, dest)
        
        # Test
        for i, img in enumerate(images[train_n+val_n:], 1):
            dest = f"data/test/{category}/{category}_{i}.png"
            shutil.copy(img, dest)
        
        return train_n, val_n, len(images) - train_n - val_n
    
    # Split original images
    orig_train, orig_val, orig_test = split_and_copy(original_images, "original")
    print(f"   ✓ Original: {orig_train} train, {orig_val} val, {orig_test} test")
    
    # Split fake images
    fake_train, fake_val, fake_test = split_and_copy(fake_images, "fake")
    print(f"   ✓ Fake: {fake_train} train, {fake_val} val, {fake_test} test")
    
    return {
        "train": {"original": orig_train, "fake": fake_train},
        "val": {"original": orig_val, "fake": fake_val},
        "test": {"original": orig_test, "fake": fake_test}
    }

def print_summary(stats):
    """Print summary of downloaded images."""
    print("\n" + "="*70)
    print("  📊 DATASET SUMMARY")
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
    print("  ⚠️  IMPORTANT NOTE")
    print("="*70)
    print("\n  These are PLACEHOLDER images for testing the system.")
    print("  For real product detection, you need:")
    print("\n  1. Real product photos (original packaging)")
    print("  2. Counterfeit product photos (fake packaging)")
    print("  3. At least 500-1000 images per category")
    print("  4. High-quality images showing logos, text, packaging details")
    
    print("\n  📖 Where to get real images:")
    print("    • Take photos of authentic products")
    print("    • Collect counterfeit examples (if available)")
    print("    • Use web scraping (with permission)")
    print("    • Public datasets (if available)")
    
    print("\n  🚀 Next Steps:")
    print("    1. Replace placeholder images with real product photos")
    print("    2. Ensure balanced dataset (equal original/fake)")
    print("    3. Run training: python backend/src/train_model.py")
    print()

def create_readme():
    """Create README in data folder."""
    readme_content = """# Product Images Dataset

## Directory Structure

```
data/
├── train/
│   ├── original/  - Training images of authentic products
│   └── fake/      - Training images of counterfeit products
├── val/
│   ├── original/  - Validation images of authentic products
│   └── fake/      - Validation images of counterfeit products
├── test/
│   ├── original/  - Test images of authentic products
│   └── fake/      - Test images of counterfeit products
└── raw/           - Raw downloaded images (before splitting)
```

## Current Status

⚠️ **PLACEHOLDER IMAGES ONLY**

The current images are placeholders for testing the system infrastructure.

## To Use Real Images

1. **Collect Images**
   - Take photos of authentic products
   - Collect counterfeit product photos
   - Aim for 500-1000 images per category

2. **Image Requirements**
   - Format: JPEG, PNG
   - Size: < 10MB per image
   - Resolution: At least 500x500 pixels
   - Content: Clear view of packaging, logos, text

3. **Replace Placeholders**
   - Delete placeholder images
   - Add your real images to train/val/test folders
   - Maintain 70/15/15 split ratio

4. **Train Model**
   ```bash
   python backend/src/train_model.py
   ```

## Image Guidelines

### Good Images
- Clear, well-lit photos
- Focused on product packaging
- Shows logos, text, and details
- Multiple angles of same product
- Consistent background

### Avoid
- Blurry or dark images
- Extreme angles
- Heavily cropped images
- Images with multiple products
- Low resolution images

## Data Sources

- **Authentic Products**: Official brand websites, retail stores
- **Counterfeit Products**: Seized items, online marketplaces (with caution)
- **Public Datasets**: Search for product authentication datasets
- **Web Scraping**: Use with permission and respect copyright

## Privacy & Legal

- Ensure you have rights to use images
- Remove any personal information
- Respect copyright and trademarks
- Follow data protection regulations
"""
    
    with open("data/README.md", "w") as f:
        f.write(readme_content)
    
    print("\n   ✓ Created data/README.md")

def main():
    """Main function."""
    print("\n" + "="*70)
    print("  📥 DOWNLOAD SAMPLE PRODUCT IMAGES")
    print("="*70)
    print("\n  This script will:")
    print("    1. Create data directory structure")
    print("    2. Download sample placeholder images")
    print("    3. Organize into train/val/test splits")
    print()
    
    try:
        # Step 1: Create directories
        organizer = create_directory_structure()
        
        # Step 2: Download images
        downloaded = download_sample_images()
        
        # Step 3: Organize images
        stats = organize_images()
        
        # Step 4: Create README
        create_readme()
        
        # Step 5: Print summary
        print_summary(stats)
        
        print("  ✅ SETUP COMPLETE!")
        print()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
