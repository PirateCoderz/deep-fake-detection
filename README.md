# Deep Fake Detection

## Frontend

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```

## Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Set `NEXT_PUBLIC_API_URL` if the API is not `http://localhost:8000`.

## What’s here

- **frontend** — Next.js app: upload image, view result (label, score, heatmap, text reasons, optional feedback).
- **backend** — FastAPI (`src/main.py`): classify endpoint, health/stats, feedback. Uses **TensorFlow** CNN (`classifier.py`, ResNet50), **preprocessor**, **explainability** (Grad-CAM-style heatmaps). **PostgreSQL** + SQLAlchemy for runs and feedback; **Redis** for rate limits when available.
- **data** — training images (you fill this).
- **models** — saved weights and config for inference.

Scripts worth knowing: `backend/src/train_model.py` (train), `backend/expand_dataset.py` (dataset helpers), Alembic under `backend/alembic` for DB migrations.

## Flow

1. Start frontend (`:3000`) and backend (`:8000`).
2. User picks an image → **POST** `/api/v1/classify` with the file.
3. API validates the image, preprocesses it, runs the model, builds explanations, stores a row, returns JSON (request id, class, confidence, heatmap, reasons).
4. Browser saves the payload in `sessionStorage` and opens `/results/<request_id>`.
5. User can submit feedback → **POST** `/api/v1/feedback` (linked to that classification).

## Training flow

1. **Dataset** — Split images into `train/` and `val/`. Under each, one folder per class (binary: real vs fake). Same layout Keras `flow_from_directory` expects.
2. **Load** — `create_data_generators` in `backend/src/train_model.py` builds train/val streams. Training set gets light augmentation (flip, shift, zoom, brightness); validation does not.
3. **Phase 1** — ResNet50 backbone stays frozen. Only the new classification head trains (transfer learning, higher LR).
4. **Phase 2** — Unfreeze the last block of ResNet layers. Retrain with a lower LR (fine-tuning). Early stopping, checkpoints, and LR-on-plateau are wired in `ModelTrainer`.
5. **Artifacts** — Best weights and `training_summary.json` land under `models/` (plus TensorBoard logs there). Wire that checkpoint into the app/config the API uses for inference.
