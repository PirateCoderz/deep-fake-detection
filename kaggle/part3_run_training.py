"""
Run on Kaggle: set paths, then execute this file (or paste into notebook cells).

Expected layout:
  TRAIN_DIR/class_a/*.jpg
  TRAIN_DIR/class_b/*.jpg
  VAL_DIR/class_a/*.jpg
  VAL_DIR/class_b/*.jpg
"""
import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# --- set these to your dataset (Kaggle Input) ---
TRAIN_DIR = os.environ.get(
    "TRAIN_DIR",
    "/kaggle/input/your-dataset-name/train",
)
VAL_DIR = os.environ.get(
    "VAL_DIR",
    "/kaggle/input/your-dataset-name/val",
)
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/kaggle/working/models")

BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "32"))
PHASE1_EPOCHS = int(os.environ.get("PHASE1_EPOCHS", "10"))
PHASE2_EPOCHS = int(os.environ.get("PHASE2_EPOCHS", "20"))
LR1 = float(os.environ.get("LR_PHASE1", "1e-3"))
LR2 = float(os.environ.get("LR_PHASE2", "1e-5"))
UNFREEZE = int(os.environ.get("UNFREEZE_LAYERS", "20"))


def main():
    if not Path(TRAIN_DIR).is_dir() or not Path(VAL_DIR).is_dir():
        raise FileNotFoundError(
            f"Set TRAIN_DIR / VAL_DIR to real paths. Got:\n  {TRAIN_DIR}\n  {VAL_DIR}"
        )

    from part1_classifier import ProductClassifier
    from part2_train_model import ModelTrainer, create_data_generators

    train_gen, val_gen = create_data_generators(
        TRAIN_DIR, VAL_DIR, batch_size=BATCH_SIZE
    )

    clf = ProductClassifier()
    trainer = ModelTrainer(clf, output_dir=OUTPUT_DIR)

    trainer.train_phase1(
        train_gen,
        val_gen,
        epochs=PHASE1_EPOCHS,
        learning_rate=LR1,
    )
    trainer.train_phase2(
        train_gen,
        val_gen,
        epochs=PHASE2_EPOCHS,
        learning_rate=LR2,
        unfreeze_layers=UNFREEZE,
    )

    trainer.save_training_summary()

    final_path = Path(OUTPUT_DIR) / "product_classifier_final.keras"
    clf.save_model(str(final_path), save_history=True)
    print("Done. Download from Kaggle Output: models/ + training_summary.json")


if __name__ == "__main__":
    main()
