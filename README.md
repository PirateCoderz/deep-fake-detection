# Fake Product Detection System

A machine learning-powered application that analyzes product packaging images to determine authenticity using CNN-based classification with explainable AI.

## Features

- Image-based product authenticity classification (Original/Fake)
- Confidence scoring (0-100%)
- Visual explanations using Grad-CAM heatmaps
- Textual reasoning for classification decisions
- Web-based interface with drag-and-drop upload
- REST API for integration
- Support for JPEG, PNG, and HEIC formats

## Project Structure

```
.
├── backend/           # FastAPI backend application
│   ├── src/          # Source code
│   └── requirements.txt
├── frontend/         # React frontend application
│   └── src/
├── models/           # Trained model weights
├── data/             # Training and test datasets
├── tests/            # Test suite
├── docker-compose.yml
└── .env.example
```

## Prerequisites

- Python 3.9+
- Node.js 18+ (for frontend)
- Docker and Docker Compose (for local development)
- PostgreSQL 14+
- Redis 7+

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd fake-product-detection
```

### 2. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Development Services

Using Docker Compose (recommended):

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Redis cache on port 6379

### 4. Set Up Python Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 5. Run Database Migrations

```bash
# From backend directory
alembic upgrade head
```

### 6. Start Backend Server

```bash
# Development mode
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000
API documentation at http://localhost:8000/docs

### 7. Set Up Frontend (Optional)

```bash
cd frontend
npm install
npm start
```

The frontend will be available at http://localhost:3000

## Development Workflow

### Running Tests

```bash
# From backend directory
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run property-based tests
pytest -v tests/property_tests/
```

### Training the Model

```bash
# From backend directory
python src/training/train_model.py --data-dir ../data --output-dir ../models
```

### API Endpoints

- `POST /api/v1/classify` - Classify product image
- `POST /api/v1/feedback` - Submit user feedback
- `GET /api/v1/health` - Health check
- `GET /api/v1/stats` - System statistics (admin)

## Configuration

Key configuration options in `.env`:

- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `MODEL_PATH` - Path to trained model weights
- `MAX_FILE_SIZE_MB` - Maximum upload size (default: 10MB)
- `RATE_LIMIT_PER_HOUR` - API rate limit (default: 100)
- `CONFIDENCE_THRESHOLD` - Low confidence warning threshold (default: 60%)

## Technology Stack

**Backend:**
- FastAPI (REST API)
- TensorFlow 2.x (Deep Learning)
- OpenCV (Image Processing)
- PostgreSQL (Database)
- Redis (Caching & Rate Limiting)

**Frontend:**
- React 18+ with TypeScript
- Material-UI / Tailwind CSS
- Axios (HTTP Client)

**ML Architecture:**
- ResNet50 backbone (transfer learning)
- Custom classification head
- Grad-CAM for explainability

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]
