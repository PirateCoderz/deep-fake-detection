# How to Train the Fake Product Detection Model

## Overview

This guide shows you how to train the CNN model for fake product detection. The system uses **two-phase training** with ResNet50 transfer learning.

## Prerequisites

Before training, you need:

1. ✅ **Training data** organized in the correct structure
2. ✅ **TensorFlow installed** (already in requirements.txt)
3. ✅ **Sufficient images** (recommended: 500+ per class)

## Data Structure Required

Your data should be organized like this:

```
data/
├── train/
│   ├── original/    # Authentic product images
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   └── fake/        # Counterfeit product images
│       ├── img1.jpg
│       ├── img2.jpg
│       └── ...
├── val/
│   ├── original/
│   └── fake/
└── test/
    ├── original/
    └── fake/
```

**Note:** If you don't have real images yet, see `HOW_TO_ADD_REAL_IMAGES.md` for instructions on collecting data.

## Training Methods Available

### Method 1: Quick Training Script (Recommended)

Create a simple training script:

```python
# train.py
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

from classifier import ProductClassifier
from train_model import ModelTrainer, create_data_generators

# Configuration
TRAIN_DIR = "data/train"
VAL_DIR = "data/val"
BATCH_SIZE = 32
EPOCHS_PHASE1 = 10
EPOCHS_PHASE2 = 20

def main():
    print("="*70)
    print("  FAKE PRODUCT DETECTION - MODEL TRAINING")
    print("="*70)
    
    # Step 1: Create data generators
    print("\n📊 Creating data generators...")
    train_gen, val_gen = create_data_generators(
        train_dir=TRAIN_DIR,
        val_dir=VAL_DIR,
        batch_size=BATCH_SIZE,
        image_size=(224, 224)
    )
    
    print(f"   Training samples: {train_gen.samples}")
    print(f"   Validation samples: {val_gen.samples}")
    print(f"   Classes: {train_gen.class_indices}")
    
    # Step 2: Create classifier
    print("\n🤖 Creating classifier...")
    classifier = ProductClassifier(
        input_shape=(224, 224, 3),
        num_classes=2
    )
    # Model is automatically built in __init__
    print(f"   Total parameters: {classifier.count_parameters():,}")
    print(f"   Trainable parameters: {classifier.count_trainable_parameters():,}")
    
    # Step 3: Create trainer
    print("\n🎯 Creating trainer...")
    trainer = ModelTrainer(
        classifier=classifier,
        output_dir="models"
    )
    
    # Step 4: Calculate class weights (for imbalanced data)
    print("\n⚖️  Calculating class weights...")
    class_weights = trainer.calculate_class_weights(train_gen.labels)
    
    # Step 5: Phase 1 - Transfer Learning
    print("\n" + "="*70)
    print("  PHASE 1: TRANSFER LEARNING")
    print("="*70)
    history1 = trainer.train_phase1(
        train_data=train_gen,
        val_data=val_gen,
        epochs=EPOCHS_PHASE1,
        learning_rate=1e-3,
        class_weights=class_weights
    )
    
    # Step 6: Phase 2 - Fine-Tuning
    print("\n" + "="*70)
    print("  PHASE 2: FINE-TUNING")
    print("="*70)
    history2 = trainer.train_phase2(
        train_data=train_gen,
        val_data=val_gen,
        epochs=EPOCHS_PHASE2,
        learning_rate=1e-5,
        unfreeze_layers=20,
        class_weights=class_weights
    )
    
    # Step 7: Save final model
    print("\n💾 Saving final model...")
    model_path = "models/fake_detector_final.h5"
    classifier.save_model(model_path)
    print(f"   Model saved to: {model_path}")
    
    # Step 8: Save training summary
    print("\n📝 Saving training summary...")
    trainer.save_training_summary("training_summary.json")
    
    print("\n" + "="*70)
    print("  ✅ TRAINING COMPLETE!")
    print("="*70)
    print(f"\n  Phase 1 Best Accuracy: {max(history1.history['val_accuracy']):.4f}")
    print(f"  Phase 2 Best Accuracy: {max(history2.history['val_accuracy']):.4f}")
    print(f"\n  Model saved to: {model_path}")
    print(f"  Logs saved to: models/logs/")
    print()

if __name__ == "__main__":
    main()
```

Run it:
```bash
python train.py
```

### Method 2: Using the Training Module Directly

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

from classifier import ProductClassifier
from train_model import ModelTrainer, create_data_generators

# Create data generators
train_gen, val_gen = create_data_generators(
    train_dir="data/train",
    val_dir="data/val",
    batch_size=32
)

# Create classifier (model is automatically built)
classifier = ProductClassifier()

# Create trainer
trainer = ModelTrainer(classifier, output_dir="models")

# Train Phase 1
trainer.train_phase1(
    train_data=train_gen,
    val_data=val_gen,
    epochs=10
)

# Train Phase 2
trainer.train_phase2(
    train_data=train_gen,
    val_data=val_gen,
    epochs=20
)

# Save model
classifier.save_model("models/fake_detector.h5")
```

## Two-Phase Training Explained

### Phase 1: Transfer Learning (10 epochs)
- **What happens:** Only trains the classification head (last layers)
- **Base model:** ResNet50 layers are frozen
- **Learning rate:** 1e-3 (higher)
- **Purpose:** Learn task-specific features quickly
- **Expected time:** 5-15 minutes (depends on dataset size)

### Phase 2: Fine-Tuning (20 epochs)
- **What happens:** Unfreezes last 20 layers of ResNet50
- **Base model:** Last layers adapt to your specific data
- **Learning rate:** 1e-5 (lower to prevent catastrophic forgetting)
- **Purpose:** Fine-tune features for better accuracy
- **Expected time:** 10-30 minutes

## Training Configuration

### Adjustable Parameters

```python
# Data parameters
BATCH_SIZE = 32              # Reduce if out of memory (16, 8)
IMAGE_SIZE = (224, 224)      # ResNet50 default

# Phase 1 parameters
PHASE1_EPOCHS = 10           # Increase if not converging
PHASE1_LR = 1e-3            # Learning rate
PHASE1_PATIENCE = 3          # Early stopping patience

# Phase 2 parameters
PHASE2_EPOCHS = 20           # Increase for better accuracy
PHASE2_LR = 1e-5            # Lower learning rate
PHASE2_UNFREEZE = 20         # Number of layers to unfreeze
PHASE2_PATIENCE = 5          # Early stopping patience
```

### Data Augmentation

The training automatically applies augmentation:
- Rotation: ±20°
- Width/Height shift: 20%
- Horizontal flip: Yes
- Zoom: 20%
- Brightness: 0.8-1.2x

## Monitoring Training

### TensorBoard (Real-time)

```bash
# In a separate terminal
tensorboard --logdir=models/logs
```

Then open: http://localhost:6006

### Training Output

You'll see:
```
PHASE 1: Transfer Learning (Classification Head Only)
============================================================
Epoch 1/10
45/45 [==============================] - 23s 512ms/step
  loss: 0.4523 - accuracy: 0.7812 - val_loss: 0.3421 - val_accuracy: 0.8456
Epoch 2/10
...
✅ Phase 1 complete. Best val_accuracy: 0.8654
```

## After Training

### 1. Check Training Summary

```bash
cat models/training_summary.json
```

Example output:
```json
{
  "timestamp": "2025-12-13T10:30:00",
  "model_architecture": "ResNet50",
  "input_shape": [224, 224, 3],
  "num_classes": 2,
  "phase1": {
    "epochs": 10,
    "final_train_accuracy": 0.8923,
    "final_val_accuracy": 0.8654,
    "best_val_accuracy": 0.8789
  },
  "phase2": {
    "epochs": 20,
    "final_train_accuracy": 0.9456,
    "final_val_accuracy": 0.9123,
    "best_val_accuracy": 0.9234
  }
}
```

### 2. Evaluate on Test Set

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

from classifier import ProductClassifier
from evaluation import ModelEvaluator
from train_model import create_data_generators

# Load trained model
classifier = ProductClassifier()
classifier.load_model("models/fake_detector_final.h5")

# Create test generator
_, test_gen = create_data_generators(
    train_dir="data/train",  # Not used
    val_dir="data/test",     # Use test set
    batch_size=32
)

# Get predictions
y_true = test_gen.labels
y_pred = []
y_proba = []

for i in range(len(test_gen)):
    batch_images, _ = test_gen[i]
    probs = classifier.model.predict(batch_images, verbose=0)
    y_proba.extend(probs)
    y_pred.extend(probs.argmax(axis=1))

# Evaluate
evaluator = ModelEvaluator(class_names=["Original", "Fake"])
metrics = evaluator.calculate_metrics(y_true, y_pred, y_proba)

print(f"Test Accuracy: {metrics.accuracy:.4f}")
print(f"Test Precision: {metrics.precision:.4f}")
print(f"Test Recall: {metrics.recall:.4f}")
print(f"Test F1-Score: {metrics.f1_score:.4f}")
```

### 3. Use the Trained Model

```python
from classifier import ProductClassifier
from preprocessor import ImagePreprocessor

# Load model
classifier = ProductClassifier()
classifier.load_model("models/fake_detector_final.h5")

# Preprocess and predict
preprocessor = ImagePreprocessor()
with open("test_image.jpg", "rb") as f:
    image_bytes = f.read()

processed, metadata, error = preprocessor.preprocess(image_bytes)
if not error:
    label, confidence, probs = classifier.predict(processed, return_probabilities=True)
    print(f"Prediction: {label} ({confidence:.1f}% confidence)")
```

## Troubleshooting

### Out of Memory Error
```python
# Reduce batch size
BATCH_SIZE = 16  # or 8
```

### Model Not Converging
```python
# Increase epochs
PHASE1_EPOCHS = 20
PHASE2_EPOCHS = 40

# Or adjust learning rate
PHASE1_LR = 5e-4  # Lower
```

### Overfitting (train acc >> val acc)
```python
# Add more dropout in classifier.py
# Or collect more training data
# Or increase data augmentation
```

### Low Accuracy
- Check data quality (images labeled correctly?)
- Ensure balanced classes (similar number of original/fake)
- Increase training data
- Train for more epochs

## Expected Results

With good quality data (500+ images per class):
- **Phase 1:** 75-85% validation accuracy
- **Phase 2:** 85-95% validation accuracy
- **Training time:** 15-45 minutes total

## Files Generated

After training:
```
models/
├── fake_detector_final.h5           # Final trained model
├── checkpoint_phase1_*.h5           # Best Phase 1 checkpoint
├── checkpoint_phase2_*.h5           # Best Phase 2 checkpoint
├── training_summary.json            # Training metrics
└── logs/                            # TensorBoard logs
    ├── phase1_*/
    └── phase2_*/
```

## Next Steps

1. ✅ Train the model using this guide
2. ✅ Evaluate on test set
3. ✅ Integrate with backend API (already done)
4. ✅ Test with real product images
5. ✅ Deploy to production

## Quick Reference

```bash
# 1. Organize your data
python -c "from backend.src.data_collection import DatasetOrganizer; DatasetOrganizer().create_directory_structure()"

# 2. Train the model
python train.py

# 3. Monitor training
tensorboard --logdir=models/logs

# 4. Test the system
python demo_system.py
```

---

**Need help?** Check:
- `HOW_TO_ADD_REAL_IMAGES.md` - How to collect training data
- `TESTING_GUIDE.md` - How to test the system
- `6_cnn_model_training_progress.md` - Technical details
