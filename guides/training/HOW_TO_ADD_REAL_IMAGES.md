# How to Add Real Product Images

## ✅ Sample Images Created!

I've created **30 sample images** in your `data/` folder for testing:
- 20 training images (10 original + 10 fake)
- 6 validation images (3 original + 3 fake)
- 4 test images (2 original + 2 fake)

**Location:** `data/train/`, `data/val/`, `data/test/`

---

## ⚠️ Important: These Are Sample Images

The current images are **synthetic/placeholder** images created for testing the system infrastructure. They will NOT provide accurate product detection.

For real product detection, you need **actual product photographs**.

---

## How to Add Real Images

### Option 1: Replace Sample Images (Recommended)

1. **Delete sample images**
   ```bash
   # Windows
   del /Q data\train\original\*.png
   del /Q data\train\fake\*.png
   del /Q data\val\original\*.png
   del /Q data\val\fake\*.png
   del /Q data\test\original\*.png
   del /Q data\test\fake\*.png
   
   # Linux/Mac
   rm data/train/original/*.png
   rm data/train/fake/*.png
   rm data/val/original/*.png
   rm data/val/fake/*.png
   rm data/test/original/*.png
   rm data/test/fake/*.png
   ```

2. **Add your real images**
   - Copy authentic product photos to `data/train/original/`
   - Copy counterfeit product photos to `data/train/fake/`
   - Repeat for `val/` and `test/` folders

3. **Maintain 70/15/15 split**
   - 70% of images → `train/`
   - 15% of images → `val/`
   - 15% of images → `test/`

### Option 2: Use Existing Images

If you already have product images:

```bash
# Copy your images
cp /path/to/your/original/images/* data/train/original/
cp /path/to/your/fake/images/* data/train/fake/
```

---

## Image Requirements

### Format
- ✅ JPEG (.jpg, .jpeg)
- ✅ PNG (.png)
- ✅ HEIC (.heic) - iPhone photos
- ❌ Other formats not supported

### Size
- Maximum: 10MB per image
- Recommended: 1-5MB per image
- Resolution: At least 500x500 pixels

### Quality
- ✅ Clear, well-lit photos
- ✅ Focused on product packaging
- ✅ Shows logos, text, and details
- ❌ Blurry or dark images
- ❌ Extreme angles
- ❌ Multiple products in one image

### Content
- **Original images**: Authentic product packaging
  - Official products from authorized retailers
  - Clear brand logos
  - Professional printing quality
  - Consistent colors

- **Fake images**: Counterfeit product packaging
  - Known counterfeit products
  - Poor printing quality
  - Misaligned text or logos
  - Color inconsistencies

---

## How Many Images Do You Need?

### Minimum (For Testing)
- 100 images per category (200 total)
- Will work but accuracy may be low

### Recommended (For Good Results)
- 500 images per category (1,000 total)
- Better accuracy and generalization

### Ideal (For Best Results)
- 1,000+ images per category (2,000+ total)
- High accuracy and robust detection

### Distribution
- **Training**: 70% of images
- **Validation**: 15% of images
- **Testing**: 15% of images

---

## Where to Get Real Images

### 1. Take Your Own Photos
**Best option for authentic images**

- Buy authentic products
- Take multiple photos:
  - Front view
  - Back view
  - Side views
  - Close-ups of logos
  - Close-ups of text
  - Packaging details

### 2. Collect Counterfeit Examples
**If available and legal**

- Seized counterfeit products
- Known fake products
- Online marketplace listings (with caution)
- **Important**: Ensure legal compliance

### 3. Web Scraping
**With permission**

- E-commerce websites (check terms of service)
- Brand official websites
- Product review sites
- **Important**: Respect copyright and robots.txt

### 4. Public Datasets
**If available**

- Search for product authentication datasets
- Academic research datasets
- Open-source image collections
- Kaggle datasets

### 5. Crowdsourcing
**For larger datasets**

- Ask users to submit photos
- Community contributions
- Ensure quality control

---

## Example: Adding Images Manually

### Step 1: Organize Your Images

```
my_product_images/
├── authentic/
│   ├── product1_front.jpg
│   ├── product1_back.jpg
│   ├── product2_front.jpg
│   └── ...
└── counterfeit/
    ├── fake1_front.jpg
    ├── fake1_back.jpg
    ├── fake2_front.jpg
    └── ...
```

### Step 2: Split Into Train/Val/Test

```python
# Use this Python script to split images
import shutil
from pathlib import Path
import random

def split_images(source_dir, dest_base, train_ratio=0.7, val_ratio=0.15):
    """Split images into train/val/test."""
    images = list(Path(source_dir).glob("*.jpg")) + list(Path(source_dir).glob("*.png"))
    random.shuffle(images)
    
    n = len(images)
    train_n = int(n * train_ratio)
    val_n = int(n * val_ratio)
    
    # Train
    for img in images[:train_n]:
        shutil.copy(img, f"{dest_base}/train/{img.name}")
    
    # Val
    for img in images[train_n:train_n+val_n]:
        shutil.copy(img, f"{dest_base}/val/{img.name}")
    
    # Test
    for img in images[train_n+val_n:]:
        shutil.copy(img, f"{dest_base}/test/{img.name}")

# Split authentic images
split_images("my_product_images/authentic", "data/original")

# Split counterfeit images
split_images("my_product_images/counterfeit", "data/fake")
```

### Step 3: Verify

```bash
# Count images
dir data\train\original /b | find /c /v ""
dir data\train\fake /b | find /c /v ""
```

---

## Testing Your Dataset

### 1. Check Image Quality

```python
python backend/src/preprocessor.py
```

### 2. Test Data Loading

```python
from backend.src.data_collection import DatasetOrganizer

organizer = DatasetOrganizer(base_dir="data")
train_images = organizer.get_image_paths("train")
print(f"Training images: {len(train_images)}")
```

### 3. Test Augmentation

```python
python backend/src/data_augmentation.py
```

---

## Current Dataset Status

Run this to check your current dataset:

```bash
# Windows
echo Training Original: & dir data\train\original /b | find /c /v ""
echo Training Fake: & dir data\train\fake /b | find /c /v ""
echo Validation Original: & dir data\val\original /b | find /c /v ""
echo Validation Fake: & dir data\val\fake /b | find /c /v ""
echo Test Original: & dir data\test\original /b | find /c /v ""
echo Test Fake: & dir data\test\fake /b | find /c /v ""
```

---

## After Adding Real Images

### 1. Verify Dataset

```python
python -c "from pathlib import Path; print('Train:', len(list(Path('data/train/original').glob('*'))), '+', len(list(Path('data/train/fake').glob('*'))))"
```

### 2. Train the Model

```bash
python backend/src/train_model.py
```

### 3. Evaluate Results

```bash
python backend/src/evaluation.py
```

---

## Tips for Best Results

### Image Collection
- ✅ Diverse products (different brands, categories)
- ✅ Multiple angles per product
- ✅ Consistent lighting
- ✅ Clear focus on packaging
- ✅ High resolution

### Dataset Balance
- ✅ Equal number of original and fake images
- ✅ Similar image quality across both classes
- ✅ Diverse counterfeit types

### Quality Control
- ✅ Review all images before training
- ✅ Remove duplicates
- ✅ Remove poor quality images
- ✅ Ensure correct labeling

---

## Need Help?

- **Check data/README.md** for dataset information
- **Run test_system.py** to verify system is working
- **See TESTING_GUIDE.md** for comprehensive testing

---

## Summary

✅ **Sample images created** - 30 images for testing  
📸 **Replace with real images** - For actual detection  
📊 **Recommended**: 500-1000 images per category  
🚀 **Then train**: `python backend/src/train_model.py`
