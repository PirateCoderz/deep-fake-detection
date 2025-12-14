# Improving Model Accuracy

## Current Problem

Your model is classifying everything as "Fake" because it was trained on only **20 images** (10 per class). This is far too small for deep learning.

## Why This Happens

1. **Insufficient data**: Deep learning needs 100s-1000s of images per class
2. **Overfitting**: Model memorized training images but can't generalize
3. **Class bias**: Model learned to always predict one class

## Solutions

### Solution 1: Collect More Real Data (BEST)

**Minimum recommended**: 100 images per class  
**Good performance**: 500+ images per class  
**Excellent performance**: 1000+ images per class

#### Where to Get Images:

1. **Take your own photos**:
   - Photograph authentic products
   - Photograph fake/counterfeit products
   - Use different angles, lighting, backgrounds

2. **Online sources**:
   - Product review websites
   - E-commerce platforms
   - Counterfeit detection databases
   - Public datasets (search for "product authentication dataset")

3. **Synthetic data**:
   - Use image generation tools
   - Create variations of existing images

#### Organize Your Data:

```
data/
├── train/
│   ├── original/  (100-500 images)
│   └── fake/      (100-500 images)
├── val/
│   ├── original/  (20-100 images)
│   └── fake/      (20-100 images)
└── test/
    ├── original/  (20-100 images)
    └── fake/      (20-100 images)
```

Then retrain:
```bash
python train.py
```

---

### Solution 2: Use Data Augmentation (TEMPORARY)

If you can't get more images immediately, augment your existing images:

#### Step 1: Augment Your Dataset

```bash
# Create 20 augmented versions per image
python augment_dataset.py 20
```

This will create:
- `data/train_augmented/` with 20x more training images
- `data/val_augmented/` with 10x more validation images

#### Step 2: Update Training Script

Edit `train.py` and change:

```python
# OLD
TRAIN_DIR = "data/train"
VAL_DIR = "data/val"

# NEW
TRAIN_DIR = "data/train_augmented"
VAL_DIR = "data/val_augmented"
```

#### Step 3: Retrain

```bash
python train.py
```

**Note**: Augmentation helps but is NOT a replacement for real diverse data. The model will still perform worse than with real images.

---

### Solution 3: Adjust Training Parameters

If you must work with limited data, try these adjustments:

#### Edit `train.py`:

```python
# Reduce epochs to prevent overfitting
PHASE1_EPOCHS = 5   # Instead of 10
PHASE2_EPOCHS = 10  # Instead of 20

# Increase dropout in classifier.py
# Edit backend/src/classifier.py:
x = layers.Dropout(0.7, name='dropout_0.7')(x)  # Instead of 0.5
x = layers.Dropout(0.5, name='dropout_0.5')(x)  # Instead of 0.3
```

---

## Expected Results by Dataset Size

| Dataset Size | Expected Accuracy | Notes |
|--------------|-------------------|-------|
| 20 images | 50-60% | Random guessing, not useful |
| 100 images | 65-75% | Minimal, may work for simple cases |
| 500 images | 80-90% | Good performance |
| 1000+ images | 90-95%+ | Excellent performance |

---

## Quick Test: Check Your Current Model

Test on all your test images:

```bash
python test_trained_model.py data/test/
```

Look at the summary:
- If accuracy is ~50%, model is guessing randomly
- If all predictions are one class, model is biased
- If accuracy is 70%+, model is learning something

---

## Recommended Action Plan

### Short Term (Today):
1. **Augment your data**:
   ```bash
   python augment_dataset.py 20
   ```

2. **Update train.py** to use augmented data

3. **Retrain**:
   ```bash
   python train.py
   ```

4. **Test again**:
   ```bash
   python test_trained_model.py data/test/
   ```

### Medium Term (This Week):
1. **Collect 50-100 real images** per class
2. **Add them to your dataset**
3. **Retrain with real + augmented data**

### Long Term (Best Results):
1. **Collect 500+ real images** per class
2. **Ensure diversity**: different products, angles, lighting
3. **Balance classes**: equal numbers of original and fake
4. **Retrain for production use**

---

## Checking If Your Model Is Learning

After retraining, a good model should show:

1. **Balanced predictions**: Not all one class
2. **Confidence variation**: Some high (>80%), some medium (60-80%)
3. **Correct classifications**: At least 70%+ on test set
4. **Different predictions**: Original images → "Original", Fake images → "Fake"

---

## Need Help?

If you're still getting poor results after augmentation:

1. Check your images are labeled correctly
2. Ensure images are actually different (not duplicates)
3. Verify original and fake images have visible differences
4. Consider if the task is too difficult (images too similar)

---

## Summary

**Current situation**: 20 images → Model can't learn  
**Quick fix**: Augment to 200+ images → Model might learn basic patterns  
**Best solution**: Collect 500+ real images → Model will learn well  

The model is working correctly - it just needs more data to learn from!
