"""
Quick Training Script for Fake Product Detection Model

This script trains the CNN model using two-phase training:
1. Phase 1: Transfer learning (classification head only)
2. Phase 2: Fine-tuning (unfreeze last layers)

Usage:
    python train.py

Requirements:
    - Training data in data/train/ and data/val/
    - TensorFlow installed
    - At least 100+ images per class (recommended 500+)
"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

from classifier import ProductClassifier
from train_model import ModelTrainer, create_data_generators

# ============================================================================
# CONFIGURATION
# ============================================================================

# Data directories
TRAIN_DIR = "data/train"
VAL_DIR = "data/val"

# Training parameters
BATCH_SIZE = 8               # Small batch size for small datasets (use 32 for larger datasets)
IMAGE_SIZE = (224, 224)      # ResNet50 default

# Phase 1: Transfer Learning
PHASE1_EPOCHS = 10           # Train classification head only
PHASE1_LR = 1e-3            # Higher learning rate

# Phase 2: Fine-Tuning
PHASE2_EPOCHS = 20           # Fine-tune last layers
PHASE2_LR = 1e-5            # Lower learning rate
PHASE2_UNFREEZE = 20         # Number of layers to unfreeze

# Output
OUTPUT_DIR = "models"
MODEL_NAME = "fake_detector_final.keras"  # Using native Keras format


# ============================================================================
# MAIN TRAINING FUNCTION
# ============================================================================

def main():
    """Main training function."""
    print("\n" + "="*70)
    print("  🎯 FAKE PRODUCT DETECTION - MODEL TRAINING")
    print("="*70)
    print("\n  This will train a CNN model to detect fake products.")
    print("  Training uses two phases:")
    print("    1. Transfer Learning (10 epochs)")
    print("    2. Fine-Tuning (20 epochs)")
    print()
    
    # Check if data directories exist
    if not Path(TRAIN_DIR).exists():
        print(f"❌ Error: Training directory not found: {TRAIN_DIR}")
        print(f"   Please organize your data first.")
        print(f"   See HOW_TO_ADD_REAL_IMAGES.md for instructions.")
        return 1
    
    if not Path(VAL_DIR).exists():
        print(f"❌ Error: Validation directory not found: {VAL_DIR}")
        print(f"   Please organize your data first.")
        return 1
    
    try:
        # Step 1: Create data generators
        print("="*70)
        print("STEP 1: LOADING DATA")
        print("="*70)
        print(f"\n📊 Creating data generators...")
        print(f"   Training directory: {TRAIN_DIR}")
        print(f"   Validation directory: {VAL_DIR}")
        print(f"   Batch size: {BATCH_SIZE}")
        print(f"   Image size: {IMAGE_SIZE}")
        
        train_gen, val_gen = create_data_generators(
            train_dir=TRAIN_DIR,
            val_dir=VAL_DIR,
            batch_size=BATCH_SIZE,
            image_size=IMAGE_SIZE
        )
        
        print(f"\n✅ Data loaded successfully!")
        print(f"   Training samples: {train_gen.samples}")
        print(f"   Validation samples: {val_gen.samples}")
        print(f"   Classes found: {list(train_gen.class_indices.keys())}")
        print(f"   Class mapping: {train_gen.class_indices}")
        
        # Check if we have enough data
        if train_gen.samples < 50:
            print(f"\n⚠️  Warning: Only {train_gen.samples} training samples found.")
            print(f"   Recommended: At least 100+ samples per class (500+ ideal)")
            response = input("\n   Continue anyway? (y/n): ")
            if response.lower() != 'y':
                print("   Training cancelled.")
                return 0
        
        # Step 2: Create classifier
        print("\n" + "="*70)
        print("STEP 2: CREATING MODEL")
        print("="*70)
        print(f"\n🤖 Building classifier...")
        print(f"   Architecture: ResNet50 (transfer learning)")
        print(f"   Input shape: {IMAGE_SIZE + (3,)}")
        print(f"   Number of classes: 2 (Original, Fake)")
        
        classifier = ProductClassifier(
            input_shape=IMAGE_SIZE + (3,),
            num_classes=2
        )
        # Model is automatically built in __init__
        
        print(f"\n✅ Model created successfully!")
        param_counts = classifier.count_parameters()
        print(f"   Total parameters: {param_counts['total']:,}")
        print(f"   Trainable parameters: {param_counts['trainable']:,}")
        print(f"   Non-trainable parameters: {param_counts['non_trainable']:,}")
        
        # Step 3: Create trainer
        print("\n" + "="*70)
        print("STEP 3: PREPARING TRAINING")
        print("="*70)
        print(f"\n🎯 Creating trainer...")
        print(f"   Output directory: {OUTPUT_DIR}")
        
        trainer = ModelTrainer(
            classifier=classifier,
            output_dir=OUTPUT_DIR
        )
        
        # Calculate class weights for imbalanced data
        print(f"\n⚖️  Calculating class weights...")
        class_weights = trainer.calculate_class_weights(train_gen.labels)
        print(f"   Class weights will help with imbalanced datasets")
        
        print(f"\n✅ Training preparation complete!")
        
        # Step 4: Phase 1 - Transfer Learning
        print("\n" + "="*70)
        print("STEP 4: PHASE 1 - TRANSFER LEARNING")
        print("="*70)
        print(f"\n🚀 Starting Phase 1...")
        print(f"   Strategy: Train classification head only")
        print(f"   Epochs: {PHASE1_EPOCHS}")
        print(f"   Learning rate: {PHASE1_LR}")
        print(f"   Base model: Frozen (ResNet50)")
        print()
        
        history1 = trainer.train_phase1(
            train_data=train_gen,
            val_data=val_gen,
            epochs=PHASE1_EPOCHS,
            learning_rate=PHASE1_LR,
            class_weights=class_weights
        )
        
        best_phase1_acc = max(history1.history['val_accuracy'])
        print(f"\n✅ Phase 1 complete!")
        print(f"   Best validation accuracy: {best_phase1_acc:.4f} ({best_phase1_acc*100:.2f}%)")
        
        # Step 5: Phase 2 - Fine-Tuning
        print("\n" + "="*70)
        print("STEP 5: PHASE 2 - FINE-TUNING")
        print("="*70)
        print(f"\n🚀 Starting Phase 2...")
        print(f"   Strategy: Fine-tune last {PHASE2_UNFREEZE} layers")
        print(f"   Epochs: {PHASE2_EPOCHS}")
        print(f"   Learning rate: {PHASE2_LR} (lower to prevent forgetting)")
        print(f"   Base model: Partially unfrozen")
        print()
        
        history2 = trainer.train_phase2(
            train_data=train_gen,
            val_data=val_gen,
            epochs=PHASE2_EPOCHS,
            learning_rate=PHASE2_LR,
            unfreeze_layers=PHASE2_UNFREEZE,
            class_weights=class_weights
        )
        
        best_phase2_acc = max(history2.history['val_accuracy'])
        print(f"\n✅ Phase 2 complete!")
        print(f"   Best validation accuracy: {best_phase2_acc:.4f} ({best_phase2_acc*100:.2f}%)")
        
        # Step 6: Save final model
        print("\n" + "="*70)
        print("STEP 6: SAVING MODEL")
        print("="*70)
        print(f"\n💾 Saving final model...")
        
        model_path = Path(OUTPUT_DIR) / MODEL_NAME
        classifier.save_model(str(model_path))
        print(f"   ✅ Model saved to: {model_path}")
        
        # Step 7: Save training summary
        print(f"\n📝 Saving training summary...")
        trainer.save_training_summary("training_summary.json")
        
        # Final summary
        print("\n" + "="*70)
        print("  ✅ TRAINING COMPLETE!")
        print("="*70)
        print(f"\n  📊 Training Results:")
        print(f"     Phase 1 Best Accuracy: {best_phase1_acc:.4f} ({best_phase1_acc*100:.2f}%)")
        print(f"     Phase 2 Best Accuracy: {best_phase2_acc:.4f} ({best_phase2_acc*100:.2f}%)")
        print(f"     Improvement: {(best_phase2_acc - best_phase1_acc)*100:.2f}%")
        
        print(f"\n  📁 Output Files:")
        print(f"     Model: {model_path}")
        print(f"     Summary: {OUTPUT_DIR}/training_summary.json")
        print(f"     Logs: {OUTPUT_DIR}/logs/")
        print(f"     Checkpoints: {OUTPUT_DIR}/checkpoint_*.h5")
        
        print(f"\n  📈 View Training Progress:")
        print(f"     tensorboard --logdir={OUTPUT_DIR}/logs")
        print(f"     Then open: http://localhost:6006")
        
        print(f"\n  🎯 Next Steps:")
        print(f"     1. Evaluate model on test set")
        print(f"     2. Test with real images: python demo_system.py")
        print(f"     3. Deploy to production")
        
        if best_phase2_acc < 0.85:
            print(f"\n  ⚠️  Note: Accuracy is below 85%")
            print(f"     Consider:")
            print(f"     - Collecting more training data")
            print(f"     - Training for more epochs")
            print(f"     - Checking data quality/labels")
        
        print()
        return 0
        
    except Exception as e:
        print(f"\n❌ Error during training: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())