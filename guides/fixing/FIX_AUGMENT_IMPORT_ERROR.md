# Fix Augmentation Import Error

## Problem
```
ModuleNotFoundError: No module named 'data_augmentation'
```

The original augmentation script has complex import dependencies.

---

## ✅ Solution - Use Simple Version

I've created a simplified version that only needs PIL and numpy (already installed).

### Quick Fix - Just Run This:

```cmd
augment-dataset.bat 20
```

This now uses the simple version automatically!

---

## Manual Commands

### Option 1: Use Simple Script (Recommended)
```cmd
python scripts\utilities\augment_dataset_simple.py 20
```

### Option 2: Use Full Path
```cmd
cd scripts\utilities
python augment_dataset_simple.py 20
cd ..\..
```

---

## What's Different?

### Old Script (augment_dataset.py)
- ❌ Complex imports from backend modules
- ❌ Import path issues
- ❌ Requires specific module structure

### New Script (augment_dataset_simple.py)
- ✅ Only uses PIL and numpy
- ✅ No import issues
- ✅ Works from anywhere
- ✅ Same augmentation quality

---

## Features

The simple script creates augmented images with:

1. **Random Rotation** (±25°)
2. **Horizontal Flips**
3. **Brightness Adjustments** (0.7-1.3x)
4. **Contrast Adjustments** (0.7-1.3x)
5. **Random Zoom** (0.8-1.2x)

### Augmentation Levels

Based on the number you specify:

| Count | Level | Variations |
|-------|-------|------------|
| 1-10 | Light | Subtle changes |
| 11-30 | Medium | Moderate changes |
| 31+ | Aggressive | Strong variations |

---

## Usage Examples

### Create 10 augmentations (light)
```cmd
augment-dataset.bat 10
```

### Create 20 augmentations (medium)
```cmd
augment-dataset.bat 20
```

### Create 50 augmentations (aggressive)
```cmd
augment-dataset.bat 50
```

---

## Output

After running, you'll have:

```
data/
├── train/
│   ├── original/          # Your original images
│   └── fake/
└── train_augmented/       # NEW - Augmented images
    ├── original/
    │   ├── img1.png
    │   ├── img1_aug001.png
    │   ├── img1_aug002.png
    │   └── ...
    └── fake/
        ├── img1.png
        ├── img1_aug001.png
        └── ...
```

---

## After Augmentation

### Step 1: Verify Images

Check a few augmented images:
```cmd
explorer data\train_augmented\original
```

Make sure they look reasonable and recognizable.

### Step 2: Update train.py

Edit `train.py` (around line 30):

```python
# Change from:
TRAIN_DIR = "data/train"
VAL_DIR = "data/val"

# To:
TRAIN_DIR = "data/train_augmented"
VAL_DIR = "data/val_augmented"
```

### Step 3: Train Model

```cmd
python train.py
```

---

## Example Output

```
==================================================================
  🔄 DATASET AUGMENTATION (Simple Version)
==================================================================

  Creating 20 augmented versions per image
  Augmentation level: medium

  Using 'medium' augmentation settings

==================================================================
  AUGMENTING TRAINING DATA
==================================================================

📂 Processing: original
📁 Found 10 images
🔄 Creating 20 augmented versions per image...
   Created 10 augmented images...
   Created 20 augmented images...
   ...
✅ Created 200 augmented images
📊 Total images in output: 210

📂 Processing: fake
📁 Found 10 images
🔄 Creating 20 augmented versions per image...
✅ Created 200 augmented images
📊 Total images in output: 210

==================================================================
  ✅ AUGMENTATION COMPLETE
==================================================================

  📊 Statistics:
     Total augmented images created: 400
     Augmentation level: medium

  📁 Augmented data saved to:
     - data/train_augmented/original/
     - data/train_augmented/fake/
     - data/val_augmented/original/
     - data/val_augmented/fake/

  🚀 Next steps:
     1. Check augmented images to verify quality
     2. Update train.py:
        TRAIN_DIR = 'data/train_augmented'
        VAL_DIR = 'data/val_augmented'
     3. Train the model: python train.py
```

---

## Troubleshooting

### Error: "No images found"
**Solution:** Make sure you have images in:
- `data/train/original/`
- `data/train/fake/`
- `data/val/original/`
- `data/val/fake/`

### Error: "PIL not found"
**Solution:** Install Pillow:
```cmd
pip install Pillow
```

### Augmented images look weird
**Solution:** Use fewer augmentations or lighter level:
```cmd
augment-dataset.bat 10
```

---

## Quick Start

**Just run:**
```cmd
augment-dataset.bat 20
```

The import error is now fixed with the simple version!

---

**The batch file now automatically uses the simple version. Just run `augment-dataset.bat 20`!**
