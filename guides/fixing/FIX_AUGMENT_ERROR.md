# Fix Augment Dataset Error

## Problem
```
can't open file 'augment_dataset.py': [Errno 2] No such file or directory
```

The script is in a subfolder, not the root directory.

---

## ✅ Quick Fix - 3 Easy Ways

### Method 1: Use the Batch File (Easiest)

I've created a convenient batch file for you:

```cmd
augment-dataset.bat 20
```

This will:
- Automatically find the script
- Activate virtual environment
- Create 20 augmented versions per image

---

### Method 2: Use Full Path

```cmd
python scripts\utilities\augment_dataset.py 20
```

---

### Method 3: Navigate to Folder First

```cmd
cd scripts\utilities
python augment_dataset.py 20
cd ..\..
```

---

## What This Script Does

The augmentation script:
1. Takes your existing images
2. Creates multiple variations with:
   - Rotation (up to 30°)
   - Brightness changes
   - Contrast changes
   - Zoom variations
   - Horizontal flips
3. Saves them to `data/train_augmented/` and `data/val_augmented/`

**Example:** If you have 10 images and use `20` augmentations:
- Original: 10 images
- After augmentation: 10 + (10 × 20) = 210 images

---

## Usage Examples

### Create 10 augmentations per image (default)
```cmd
augment-dataset.bat
```

### Create 20 augmentations per image
```cmd
augment-dataset.bat 20
```

### Create 50 augmentations per image
```cmd
augment-dataset.bat 50
```

---

## After Augmentation

### Step 1: Update train.py

Edit `train.py` and change these lines:

```python
# Change from:
TRAIN_DIR = "data/train"
VAL_DIR = "data/val"

# To:
TRAIN_DIR = "data/train_augmented"
VAL_DIR = "data/val_augmented"
```

### Step 2: Train the Model

```cmd
python train.py
```

---

## Output Structure

After running augmentation, you'll have:

```
data/
├── train/                    # Original training data
│   ├── original/
│   └── fake/
├── train_augmented/          # Augmented training data (NEW)
│   ├── original/
│   │   ├── original_1.png
│   │   ├── original_1_aug1.png
│   │   ├── original_1_aug2.png
│   │   └── ...
│   └── fake/
│       ├── fake_1.png
│       ├── fake_1_aug1.png
│       └── ...
├── val/                      # Original validation data
│   ├── original/
│   └── fake/
└── val_augmented/            # Augmented validation data (NEW)
    ├── original/
    └── fake/
```

---

## Tips

### How Many Augmentations?

| Current Images | Recommended Augmentations | Final Count |
|----------------|---------------------------|-------------|
| 10 per class   | 50                        | 510         |
| 20 per class   | 25                        | 520         |
| 50 per class   | 10                        | 550         |
| 100+ per class | 5                         | 600+        |

### Warning: Don't Over-Augment

- Too many augmentations can lead to overfitting
- Better to collect real images when possible
- Use augmentation as a temporary solution

### Check Augmented Images

Before training, check a few augmented images to make sure they look reasonable:
- Open `data/train_augmented/original/` folder
- View some `*_aug*.png` files
- Make sure they're still recognizable

---

## Troubleshooting

### Error: "No images found"
**Solution:** Make sure you have images in:
- `data/train/original/`
- `data/train/fake/`
- `data/val/original/`
- `data/val/fake/`

### Error: "ModuleNotFoundError"
**Solution:** Install dependencies:
```cmd
.venv\Scripts\activate
pip install -r backend\requirements.txt
```

### Augmentation Takes Too Long
**Solution:** Reduce the number of augmentations:
```cmd
augment-dataset.bat 10
```

---

## Quick Start

**Just run:**
```cmd
augment-dataset.bat 20
```

Then update `train.py` to use `data/train_augmented` and train!

---

**The script location issue is now fixed. Use `augment-dataset.bat` for easy access!**
