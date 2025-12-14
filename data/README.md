# Sample Product Images Dataset

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
