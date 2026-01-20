# Fix Training Import Error

## Problem
```
ModuleNotFoundError: No module named 'src'
```

This happens when running `python train.py` because of Python import path issues.

---

## ✅ Solution - Already Fixed!

I've updated the files to fix this issue. Just run the training command again:

```cmd
python train.py
```

---

## What Was Fixed

### 1. Updated `backend/src/train_model.py`
Changed the import to handle both cases:
```python
try:
    from src.classifier import ProductClassifier
except ImportError:
    from classifier import ProductClassifier
```

### 2. Updated `train.py`
Improved the path handling:
```python
backend_src = str(Path(__file__).parent / 'backend' / 'src')
if backend_src not in sys.path:
    sys.path.insert(0, backend_src)
```

---

## How to Train the Model

### Step 1: Activate Virtual Environment (if using one)
```cmd
.venv\Scripts\activate
```

### Step 2: Run Training
```cmd
python train.py
```

### Step 3: Wait for Training to Complete
- Phase 1: ~5-10 minutes (10 epochs)
- Phase 2: ~10-20 minutes (20 epochs)
- Total: ~15-30 minutes depending on your hardware

---

## Training Output

You should see:
```
==================================================================
  🎯 FAKE PRODUCT DETECTION - MODEL TRAINING
==================================================================

STEP 1: LOADING DATA
==================================================================
📊 Creating data generators...
   Training directory: data/train
   Validation directory: data/val
   ...

STEP 2: CREATING MODEL
==================================================================
🤖 Building classifier...
   Architecture: ResNet50 (transfer learning)
   ...

STEP 3: PREPARING TRAINING
==================================================================
🎯 Creating trainer...
   ...

STEP 4: PHASE 1 - TRANSFER LEARNING
==================================================================
🚀 Starting Phase 1...
   Epochs: 10
   ...

STEP 5: PHASE 2 - FINE-TUNING
==================================================================
🚀 Starting Phase 2...
   Epochs: 20
   ...

STEP 6: SAVING MODEL
==================================================================
💾 Saving final model...
   ✅ Model saved to: models/fake_detector_final.keras

✅ TRAINING COMPLETE!
```

---

## After Training

### Test the Model
```cmd
python scripts\utilities\test_trained_model.py
```

### View Training Progress
```cmd
tensorboard --logdir=models/logs
```
Then open: http://localhost:6006

### Start the System
```cmd
start-both.bat
```

---

## Common Issues

### Issue: "Training directory not found"
**Solution:** Make sure you have data in these folders:
- `data/train/original/` - Original product images
- `data/train/fake/` - Fake product images
- `data/val/original/` - Validation original images
- `data/val/fake/` - Validation fake images

### Issue: "Only X training samples found"
**Solution:** You need more images. Minimum 50, recommended 100+ per class.

See: `guides/training/HOW_TO_ADD_REAL_IMAGES.md`

### Issue: "Out of memory"
**Solution:** Reduce batch size in `train.py`:
```python
BATCH_SIZE = 4  # Change from 8 to 4
```

---

## Training Tips

1. **More Data = Better Accuracy**
   - Minimum: 50 images per class
   - Good: 100-200 images per class
   - Excellent: 500+ images per class

2. **Monitor Training**
   - Watch for overfitting (train accuracy >> val accuracy)
   - Use TensorBoard to visualize progress

3. **Adjust Parameters**
   - Increase epochs if accuracy is still improving
   - Decrease learning rate if loss is unstable
   - Add more data augmentation if overfitting

---

## Need Help?

See these guides:
- `guides/training/HOW_TO_TRAIN_MODEL.md` - Detailed training guide
- `guides/training/HOW_TO_ADD_REAL_IMAGES.md` - Adding training data
- `guides/training/IMPROVING_MODEL_ACCURACY.md` - Accuracy tips

---

**The import error is now fixed. Just run `python train.py` again!**
