# Kaggle training — guide for new engineers

This guide walks you from **empty notebook** to **saved model + metrics**. Follow the steps **in order**; later steps assume earlier ones are done.

---

## End-to-end checklist (follow in sequence)

1. Build your **folder structure** (`train/` and `val/` with class subfolders) — **Step 1**.  
2. Add the **`kaggle/`** Python files to Kaggle and skim what each file does — **Step 2**.  
3. Set **`TRAIN_DIR`** and **`VAL_DIR`** — **Step 3**.  
4. Enable **GPU**, run **`part3_run_training.py`** — **Step 4**.  
5. Open **`training_summary.json`** and the saved **`.keras`** model — **Step 5**.  
6. If metrics are poor, use **If training looks wrong** at the bottom.

---

## Step 1: Prepare your dataset folders

The training code does **not** split data for you. **You** create folders and split images yourself.

### 1a. The two top-level folders you need

| Folder name | Role |
|-------------|------|
| **`train`** | Every image the model **learns** from. |
| **`val`** | Images used only to **score** the model each epoch (never used to update weights during training). |

### 1b. Class folders inside `train` and `val`

Under **both** `train` and `val`, create **the same two subfolder names** (same spelling). Example:

| Subfolder | Meaning |
|-----------|---------|
| **`Original`** | Authentic / not-fake images. |
| **`Fake`** | Fake or manipulated images. |

You can use other names (e.g. `real` / `fake`), but **train** and **val** must use the **same** names.

### 1c. Example layout (copy this shape)

```text
your_dataset/
  train/
    Original/     ← .jpg / .png here (training only)
    Fake/
  val/
    Original/     ← different files from train/Original
    Fake/
```

**Rules:**

- Each image file lives in **exactly one** class folder.
- **Do not** put the same file in both `train` and `val` (no duplicates across splits).
- A common split is **80% of images in `train`**, **20% in `val`**, per class.

### 1d. What you will type in the script later

- **`TRAIN_DIR`** = full path to the **`train`** folder (the folder that **directly contains** `Original/` and `Fake/`).
- **`VAL_DIR`** = full path to the **`val`** folder (also contains `Original/` and `Fake/`).

On Kaggle, after you **Add Data**, paths often look like:

`/kaggle/input/<your-dataset-name>/train`  
`/kaggle/input/<your-dataset-name>/val`

---

## Step 2: The three Python files

Run them **in concept** as: build model → train → run script. On disk they are three files:

| Order | File | In one sentence |
|-------|------|-----------------|
| 1 | `part1_classifier.py` | Builds the neural network (ResNet50 + small head on top). |
| 2 | `part2_train_model.py` | Loads images from folders, runs **phase 1** then **phase 2** training, saves metrics. |
| 3 | `part3_run_training.py` | **You edit this**: set paths, then run it to start everything. |

You only need to **run** `part3_run_training.py`. The other two are **imported** automatically.

---

## Step 3: Point the script at your data

1. Open **`part3_run_training.py`**.
2. Find **`TRAIN_DIR`** and **`VAL_DIR`** near the top.
3. Replace the placeholder paths with your real paths (see Step 1d).

Optional: instead of editing the file, you can set **environment variables** in the notebook before running:

`TRAIN_DIR`, `VAL_DIR`, `OUTPUT_DIR`, `BATCH_SIZE`, `PHASE1_EPOCHS`, `PHASE2_EPOCHS`, `LR_PHASE1`, `LR_PHASE2`, `UNFREEZE_LAYERS`.

---

## Step 4: Run training on Kaggle

1. Create a **Kaggle Notebook** (or Script) and **attach your dataset** (Add Data).
2. Upload the **`kaggle/`** folder (or clone the repo) so `part1_*`, `part2_*`, and `part3_*` sit in the **same working directory**.
3. Open **Session options** → set **Accelerator** to **GPU** (recommended).
4. In a notebook cell, run:

```bash
cd /kaggle/working
# adjust path if your .py files live elsewhere
python part3_run_training.py
```

5. Watch the log: you should see **Phase 1** (train head only), then **Phase 2** (fine-tune part of ResNet). Wait until it finishes without errors.

---

## Step 5: Outputs and how to read them

### Where files go

By default, outputs are under **`/kaggle/working/models/`** (or whatever you set as `OUTPUT_DIR`).

### What to download or keep

| File | What it is |
|------|------------|
| **`training_summary.json`** | Text file with metrics (KPIs) from both training phases. |
| **`checkpoint_phase1_*.h5`**, **`checkpoint_phase2_*.h5`** | Best weights during each phase (HDF5). |
| **`product_classifier_final.keras`** | Final saved model after both phases. |
| **`logs/`** | TensorBoard logs (optional to inspect). |

### Reading `training_summary.json` (main KPIs)

**Top of file:** when it ran, model name (`ResNet50`), input size, number of classes.

**For each phase (`phase1`, `phase2`):**

| Field | Plain English |
|-------|----------------|
| **`best_val_accuracy`** | Best **validation accuracy** in that phase — main number to compare runs. |
| **`final_val_accuracy`** | Accuracy on validation at the **last** epoch. |
| **`final_train_accuracy`** | Accuracy on training at the last epoch. |
| **`best_val_loss`** / **`final_val_loss`** | Loss (lower is usually better). |
| **`epochs_ran`** | How many epochs actually ran (early stopping may stop sooner than max). |

**Early stopping** picks the weights that had the **best `val_accuracy`**, not necessarily the last epoch.

---

## Class index (folder names vs labels)

Keras assigns **class numbers from folder names in alphabetical order**.

Example: folders **`Fake`** and **`Original`** → **`Fake` = 0**, **`Original` = 1** (because `F` comes before `O`).

This app’s backend expects **class 0 = Original** and **class 1 = Fake**. To avoid swapping labels, name folders so **Original sorts first**, for example:

- **`0_Original`** and **`1_Fake`**, or  
- change mapping in code after you know your folder order.

---

## If training looks wrong — what to change

Use this **after** a run when accuracy is poor or loss is weird. Match your **symptom** to the table.

### Train and validation both low (model still “weak”)

| Try | Knobs |
|-----|--------|
| Train longer | `PHASE1_EPOCHS`, `PHASE2_EPOCHS` (or patience in `part2_train_model.py`) |
| Slightly higher learning rate | `LR_PHASE1`, `LR_PHASE2` (only if loss is smooth) |
| Let ResNet adapt more | `UNFREEZE_LAYERS` increase (e.g. 20 → 40) |
| Batch size | `BATCH_SIZE` — try 16 or 32 |

### Train high, validation low (overfitting)

| Try | Knobs |
|-----|--------|
| Stronger image augmentation | `ImageDataGenerator` in `part2_train_model.py` |
| Less backbone tuning | `UNFREEZE_LAYERS` decrease |
| Gentler fine-tuning | `LR_PHASE2` lower |
| Data | More images; fix wrong labels; ensure no train/val overlap |

### Unstable loss (NaNs or wild jumps)

| Try | Knobs |
|-----|--------|
| Lower learning rates | `LR_PHASE1`, `LR_PHASE2` |
| Larger batch | `BATCH_SIZE` increase |

### One class much rarer than the other

Use **class weights** in training — helper `calculate_class_weights` is in `part2_train_model.py`; you need to pass `class_weight` into the `fit` calls (may require a small code change in `part3`).

### Metrics look good but predictions are wrong

Check **wrong folder**, **wrong label**, or **class index** mismatch (section above).

**Simple rule:** if **validation loss goes down** and **validation accuracy goes up** over time, you are usually on track. If **train loss** keeps dropping but **validation loss** rises, treat it as overfitting (table above).
