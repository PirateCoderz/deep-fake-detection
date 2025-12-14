# Design Document: Fake Product Detection System

## Overview

The Fake Product Detection System is a machine learning-powered application that analyzes product packaging images to determine authenticity. The system uses a Convolutional Neural Network (CNN) architecture to classify products as "Original" or "Fake" while providing explainable results through visual highlighting and textual reasoning. The design emphasizes generalizability across product categories, robustness to real-world image variations, and user trust through transparency.

The system consists of four major components:
1. **Image Preprocessing Pipeline** - Handles image normalization, augmentation, and quality enhancement
2. **CNN Classification Model** - Deep learning model for binary classification with confidence scoring
3. **Explainability Module** - Generates visual and textual explanations using Grad-CAM and feature analysis
4. **Web Application Interface** - User-facing application with REST API for image upload and result display

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│  (React Frontend with drag-drop upload & camera capture)    │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/REST API
┌────────────────────▼────────────────────────────────────────┐
│                    API Gateway Layer                         │
│  (FastAPI - Request validation, rate limiting, auth)        │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼──────────┐    ┌────────▼─────────────┐
│  Preprocessing   │    │   Logging &          │
│     Service      │    │   Metrics Service    │
└───────┬──────────┘    └──────────────────────┘
        │
┌───────▼──────────────────────────────────────┐
│         CNN Classification Model             │
│  (TensorFlow/PyTorch - ResNet50 backbone)   │
└───────┬──────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────┐
│        Explainability Module                 │
│  (Grad-CAM + Feature Extraction)            │
└───────┬──────────────────────────────────────┘
        │
┌───────▼──────────────────────────────────────┐
│         Response Formatter                   │
└──────────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.9+
- FastAPI (REST API framework)
- TensorFlow 2.x or PyTorch 1.13+ (Deep Learning)
- OpenCV 4.x (Image preprocessing)
- NumPy, Pillow (Image manipulation)
- Uvicorn (ASGI server)

**Frontend:**
- React 18+ with TypeScript
- Axios (HTTP client)
- Material-UI or Tailwind CSS (UI components)
- React Dropzone (File upload)

**Model Training:**
- Jupyter Notebooks (Experimentation)
- TensorBoard (Training visualization)
- scikit-learn (Metrics and evaluation)

**Infrastructure:**
- Docker (Containerization)
- PostgreSQL (Logging and metrics storage)
- Redis (Caching and rate limiting)
- AWS S3 or local storage (Temporary image storage)

## Components and Interfaces

### 1. Image Preprocessing Pipeline

**Purpose:** Transform raw user images into model-ready tensors while handling various real-world conditions.

**Key Functions:**

```python
class ImagePreprocessor:
    def validate_image(image_bytes: bytes) -> Tuple[bool, str]
    def resize_image(image: np.ndarray, target_size: Tuple[int, int]) -> np.ndarray
    def normalize_lighting(image: np.ndarray) -> np.ndarray
    def reduce_glare(image: np.ndarray) -> np.ndarray
    def detect_primary_product(image: np.ndarray) -> np.ndarray
    def prepare_for_model(image: np.ndarray) -> tf.Tensor
```

**Processing Steps:**
1. **Validation** - Check file format, size (<10MB), and basic image properties
2. **Decoding** - Convert bytes to numpy array using OpenCV or Pillow
3. **Quality Assessment** - Detect blur, low resolution, or extreme lighting
4. **Glare Reduction** - Apply bilateral filtering and adaptive histogram equalization
5. **Product Detection** - Use simple object detection or center-crop heuristic
6. **Resizing** - Resize to 224x224 or 299x299 (depending on model architecture)
7. **Normalization** - Scale pixel values to [0,1] or standardize using ImageNet statistics
8. **Tensor Conversion** - Convert to framework-specific tensor format

**Interface:**
- Input: Raw image bytes from HTTP request
- Output: Preprocessed tensor ready for model inference + metadata (original dimensions, quality score)

### 2. CNN Classification Model

**Architecture Choice:** Transfer learning with ResNet50 or EfficientNetB3 backbone

**Rationale:**
- Pre-trained on ImageNet provides strong feature extraction
- ResNet50 offers good balance of accuracy and inference speed
- EfficientNet provides better accuracy with similar computational cost
- Both architectures are well-suited for fine-tuning on custom datasets

**Model Structure:**

```
Input (224x224x3)
    ↓
Backbone (ResNet50 pre-trained)
    ↓
Global Average Pooling
    ↓
Dense Layer (512 units, ReLU)
    ↓
Dropout (0.5)
    ↓
Dense Layer (256 units, ReLU)
    ↓
Dropout (0.3)
    ↓
Output Layer (2 units, Softmax)
    ↓
[Original_prob, Fake_prob]
```

**Training Strategy:**
1. **Phase 1 (Transfer Learning):** Freeze backbone, train only classification head for 10 epochs
2. **Phase 2 (Fine-tuning):** Unfreeze last 20 layers of backbone, train end-to-end with lower learning rate for 20 epochs
3. **Data Augmentation:** Random rotation (±15°), horizontal flip, brightness/contrast adjustment, zoom (0.8-1.2x)
4. **Loss Function:** Categorical cross-entropy with class weights to handle imbalance
5. **Optimizer:** Adam with learning rate 1e-4 (phase 1), 1e-5 (phase 2)
6. **Regularization:** L2 regularization (1e-4), dropout, early stopping

**Key Functions:**

```python
class ProductClassifier:
    def __init__(self, model_path: str)
    def predict(self, image_tensor: tf.Tensor) -> Tuple[str, float, np.ndarray]
    def get_feature_maps(self, image_tensor: tf.Tensor) -> Dict[str, np.ndarray]
    def load_model(self, path: str) -> None
```

**Interface:**
- Input: Preprocessed image tensor (batch_size, 224, 224, 3)
- Output: 
  - Classification label ("Original" or "Fake")
  - Confidence score (0-100%)
  - Feature maps from intermediate layers (for explainability)

### 3. Explainability Module

**Purpose:** Generate human-understandable explanations for model predictions using Grad-CAM and feature analysis.

**Techniques:**

**A. Grad-CAM (Gradient-weighted Class Activation Mapping)**
- Computes gradients of predicted class with respect to final convolutional layer
- Generates heatmap showing which regions influenced the decision
- Overlays heatmap on original image to highlight suspicious areas

**B. Feature-based Reasoning**
- Analyzes specific visual aspects: logo clarity, text sharpness, color consistency, print quality
- Compares extracted features against learned authentic patterns
- Generates textual explanations based on feature deviations

**Key Functions:**

```python
class ExplainabilityModule:
    def generate_gradcam(self, image: np.ndarray, model: tf.keras.Model, 
                         pred_class: int) -> np.ndarray
    def overlay_heatmap(self, image: np.ndarray, heatmap: np.ndarray) -> np.ndarray
    def extract_visual_features(self, image: np.ndarray) -> Dict[str, float]
    def generate_textual_reasons(self, features: Dict, prediction: str) -> List[str]
    def compare_with_reference(self, features: Dict, category: str) -> Dict[str, float]
```

**Explanation Generation Logic:**

```python
def generate_explanation(image, prediction, confidence, features):
    reasons = []
    
    # Logo analysis
    if features['logo_clarity'] < 0.6:
        reasons.append("Logo appears blurry or poorly printed")
    
    # Text analysis
    if features['text_alignment_score'] < 0.7:
        reasons.append("Text alignment is inconsistent with authentic products")
    
    # Color analysis
    if features['color_deviation'] > 0.3:
        reasons.append("Color scheme differs from authentic packaging")
    
    # Print quality
    if features['print_texture_score'] < 0.65:
        reasons.append("Print quality shows signs of low-resolution reproduction")
    
    # Edge sharpness
    if features['edge_sharpness'] < 0.5:
        reasons.append("Packaging edges lack the crispness of genuine products")
    
    return reasons[:3]  # Return top 3 most relevant reasons
```

**Interface:**
- Input: Original image, preprocessed tensor, model prediction, feature maps
- Output:
  - Grad-CAM heatmap overlay image (as base64 or URL)
  - List of 3-5 textual explanations
  - Feature comparison scores

### 4. Web Application Interface

**Frontend Components:**

```
App
├── UploadPage
│   ├── ImageUploader (drag-drop + camera)
│   ├── ImagePreview
│   └── UploadButton
├── ResultsPage
│   ├── ClassificationBadge (Original/Fake)
│   ├── ConfidenceScore (circular progress)
│   ├── ExplanationPanel
│   │   ├── HeatmapViewer
│   │   └── ReasonsList
│   └── FeedbackForm
└── HistoryPage (optional)
```

**Backend API Endpoints:**

```python
POST /api/v1/classify
    Request: multipart/form-data with image file
    Response: {
        "classification": "Fake",
        "confidence": 87.5,
        "explanations": {
            "heatmap_url": "https://...",
            "reasons": ["Logo appears blurry...", "Text alignment..."],
            "feature_scores": {
                "logo_clarity": 0.45,
                "text_alignment": 0.62,
                ...
            }
        },
        "processing_time_ms": 1234,
        "request_id": "uuid"
    }

POST /api/v1/feedback
    Request: {
        "request_id": "uuid",
        "user_feedback": "correct" | "incorrect",
        "comments": "optional text"
    }
    Response: {"status": "success"}

GET /api/v1/health
    Response: {"status": "healthy", "model_loaded": true}

GET /api/v1/stats (admin only)
    Response: {
        "total_classifications": 1234,
        "accuracy_estimate": 0.89,
        "avg_confidence": 0.82
    }
```

**Request Flow:**

1. User uploads image via frontend
2. Frontend sends POST to /api/v1/classify
3. API Gateway validates request (file size, format, rate limit)
4. Image bytes passed to Preprocessing Pipeline
5. Preprocessed tensor sent to CNN Model
6. Model returns prediction + feature maps
7. Explainability Module generates heatmap and reasons
8. Response formatted and returned to frontend
9. Frontend displays results with visualizations
10. Logging Service records classification event

## Data Models

### Image Metadata

```python
@dataclass
class ImageMetadata:
    original_width: int
    original_height: int
    file_format: str  # "JPEG", "PNG", "HEIC"
    file_size_bytes: int
    quality_score: float  # 0-1, based on blur/resolution detection
    has_glare: bool
    preprocessing_applied: List[str]  # ["glare_reduction", "lighting_norm"]
```

### Classification Result

```python
@dataclass
class ClassificationResult:
    request_id: str  # UUID
    timestamp: datetime
    classification: str  # "Original" or "Fake"
    confidence_score: float  # 0-100
    processing_time_ms: int
    model_version: str
    image_metadata: ImageMetadata
```

### Explanation Data

```python
@dataclass
class ExplanationData:
    heatmap_image: np.ndarray  # Grad-CAM overlay
    textual_reasons: List[str]  # Top 3-5 reasons
    feature_scores: Dict[str, float]  # Individual feature analysis
    reference_comparison: Optional[Dict[str, float]]  # If reference available
```

### Training Sample

```python
@dataclass
class TrainingSample:
    image_path: str
    label: int  # 0 = Original, 1 = Fake
    product_category: str  # "cosmetics", "electronics", "apparel"
    brand: Optional[str]
    source: str  # "web_scraping", "user_submission", "manual_collection"
    verified: bool  # Manual verification status
    metadata: Dict[str, Any]
```

### User Feedback

```python
@dataclass
class UserFeedback:
    request_id: str
    feedback_type: str  # "correct", "incorrect"
    user_comments: Optional[str]
    timestamp: datetime
    flagged_for_review: bool
```

### Database Schema

**classifications table:**
```sql
CREATE TABLE classifications (
    id SERIAL PRIMARY KEY,
    request_id UUID UNIQUE NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    classification VARCHAR(10) NOT NULL,
    confidence_score FLOAT NOT NULL,
    processing_time_ms INTEGER,
    model_version VARCHAR(50),
    image_quality_score FLOAT,
    product_category VARCHAR(100)
);
```

**feedback table:**
```sql
CREATE TABLE feedback (
    id SERIAL PRIMARY KEY,
    request_id UUID REFERENCES classifications(request_id),
    feedback_type VARCHAR(20) NOT NULL,
    user_comments TEXT,
    timestamp TIMESTAMP NOT NULL,
    flagged_for_review BOOLEAN DEFAULT FALSE
);
```

**metrics table:**
```sql
CREATE TABLE daily_metrics (
    date DATE PRIMARY KEY,
    total_classifications INTEGER,
    avg_confidence FLOAT,
    correct_feedback_count INTEGER,
    incorrect_feedback_count INTEGER,
    avg_processing_time_ms FLOAT
);
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

Before defining properties, we identify and eliminate redundancy:

**Redundancy Analysis:**
- Properties 1.1 and 1.4 both test input validation but from different angles (valid vs invalid). These are complementary and should both be kept.
- Properties 3.2 and 4.1 both relate to preprocessing but test different aspects (dimension consistency vs lighting normalization). Keep both.
- Properties 2.1 and 2.2 test different aspects of explainability (visual vs textual). Keep both.
- Property 7.1 and 7.3 both test logging but for different events. Keep both.

**Combined Properties:**
- Properties about feature extraction (5.1 and 5.3) can be combined into a single comprehensive property about feature completeness.

### Core Properties

**Property 1: Valid image format acceptance**
*For any* image file in JPEG, PNG, or HEIC format with size ≤ 10MB, the Detection System should accept the upload and proceed to classification.
**Validates: Requirements 1.1**

**Property 2: Invalid input rejection**
*For any* file that is not a valid image format or exceeds 10MB, the Detection System should reject the upload and return an error message.
**Validates: Requirements 1.4**

**Property 3: Classification output format**
*For any* successfully processed image, the Detection System should return exactly one classification label ("Original" or "Fake") and a confidence score in the range [0, 100].
**Validates: Requirements 1.3**

**Property 4: Low confidence warning**
*For any* classification result with confidence score < 60%, the response should include an uncertainty warning flag.
**Validates: Requirements 1.5**

**Property 5: Fake classification includes heatmap**
*For any* image classified as "Fake", the Explainability Module should generate a Grad-CAM heatmap highlighting suspicious regions.
**Validates: Requirements 2.1**

**Property 6: Explanation completeness**
*For any* classification result, the Detection System should provide at least 3 textual reasons explaining the decision.
**Validates: Requirements 2.2**

**Property 7: Detailed analysis includes feature comparison**
*For any* classification request with detailed_analysis flag set to true, the response should include feature comparison scores.
**Validates: Requirements 2.4**

**Property 8: Preprocessing dimension consistency**
*For any* input image, the Preprocessing Pipeline should output a tensor with consistent dimensions (224×224×3 or 299×299×3 depending on model architecture).
**Validates: Requirements 3.2**

**Property 9: Preprocessing normalization**
*For any* preprocessed image tensor, all pixel values should be in the range [0, 1] or standardized with mean ≈ 0 and std ≈ 1.
**Validates: Requirements 3.2**

**Property 10: Metrics calculation completeness**
*For any* set of predictions and ground truth labels, the evaluation function should compute and return precision, recall, and F1-score for both "Original" and "Fake" classes.
**Validates: Requirements 3.4**

**Property 11: Lighting normalization application**
*For any* image processed through the Preprocessing Pipeline, brightness and contrast normalization should be applied as indicated in preprocessing metadata.
**Validates: Requirements 4.1**

**Property 12: Glare reduction on detection**
*For any* image where glare is detected (glare_score > threshold), the Preprocessing Pipeline should apply glare reduction and record this in preprocessing metadata.
**Validates: Requirements 4.3**

**Property 13: Low quality warning**
*For any* image with quality_score < 0.5 (indicating low resolution or blur), the response should include a quality warning.
**Validates: Requirements 4.4**

**Property 14: Primary product detection**
*For any* image containing multiple distinct objects, the Preprocessing Pipeline should detect and crop to the primary product region.
**Validates: Requirements 4.5**

**Property 15: Feature extraction completeness**
*For any* product image, the feature extraction should produce values for logo_clarity, text_alignment, color_consistency, and print_texture without requiring QR codes or barcodes.
**Validates: Requirements 5.1, 5.3**

**Property 16: Progress indicator during processing**
*For any* classification request in progress, the User Interface should display a progress indicator.
**Validates: Requirements 6.2**

**Property 17: Classification logging completeness**
*For any* completed classification, the system should create a log entry containing timestamp, product_category, classification label, and confidence_score.
**Validates: Requirements 7.1**

**Property 18: Feedback storage with linkage**
*For any* user feedback submission, the system should store the feedback with a valid reference (request_id) to the original classification.
**Validates: Requirements 7.3**

**Property 19: Metrics report completeness**
*For any* metrics report generation request, the output should include classification distribution statistics, average confidence scores, and category-wise performance metrics.
**Validates: Requirements 7.4**

**Property 20: Daily accuracy calculation**
*For any* day with user feedback data, the metrics calculation should compute accuracy as (correct_feedback_count / total_feedback_count).
**Validates: Requirements 7.2**

**Property 21: Incorrect feedback flagging**
*For any* feedback submission marked as "incorrect", the corresponding classification record should be flagged for manual review.
**Validates: Requirements 8.1**

**Property 22: API backward compatibility**
*For any* API request format valid in version N, the same request should remain valid in version N+1 (maintaining backward compatibility).
**Validates: Requirements 8.4**

**Property 23: Log anonymization**
*For any* log entry, the data should not contain email addresses, IP addresses, or other personally identifiable information.
**Validates: Requirements 9.3**

**Property 24: API response format consistency**
*For any* API request, the response should be valid JSON containing standard fields (status, data/error, request_id).
**Validates: Requirements 10.2**

## Error Handling

### Input Validation Errors

**Invalid File Format:**
- Error Code: `INVALID_FORMAT`
- HTTP Status: 400 Bad Request
- Message: "Unsupported file format. Please upload JPEG, PNG, or HEIC images."
- Action: Reject request immediately, do not process

**File Size Exceeded:**
- Error Code: `FILE_TOO_LARGE`
- HTTP Status: 413 Payload Too Large
- Message: "Image file exceeds 10MB limit. Please upload a smaller image."
- Action: Reject request before loading full file into memory

**Corrupted Image:**
- Error Code: `CORRUPTED_IMAGE`
- HTTP Status: 400 Bad Request
- Message: "Unable to decode image file. The file may be corrupted."
- Action: Catch decoding exceptions in preprocessing

### Processing Errors

**Model Inference Failure:**
- Error Code: `INFERENCE_ERROR`
- HTTP Status: 500 Internal Server Error
- Message: "Classification failed due to internal error. Please try again."
- Action: Log full error details, return generic message to user, alert monitoring

**Preprocessing Failure:**
- Error Code: `PREPROCESSING_ERROR`
- HTTP Status: 500 Internal Server Error
- Message: "Unable to process image. Please try a different image."
- Action: Log error with image metadata, attempt graceful degradation if possible

**Timeout:**
- Error Code: `PROCESSING_TIMEOUT`
- HTTP Status: 504 Gateway Timeout
- Message: "Processing took too long. Please try again with a simpler image."
- Action: Cancel processing after 10 seconds, clean up resources

### System Errors

**Model Not Loaded:**
- Error Code: `MODEL_UNAVAILABLE`
- HTTP Status: 503 Service Unavailable
- Message: "Classification service is temporarily unavailable. Please try again later."
- Action: Return immediately, trigger alert for ops team

**Database Connection Error:**
- Error Code: `DATABASE_ERROR`
- HTTP Status: 500 Internal Server Error
- Message: "Unable to save results. Classification completed but not logged."
- Action: Complete classification but warn about logging failure

**Rate Limit Exceeded:**
- Error Code: `RATE_LIMIT_EXCEEDED`
- HTTP Status: 429 Too Many Requests
- Message: "Too many requests. Please try again in {retry_after} seconds."
- Headers: `Retry-After: {seconds}`
- Action: Reject request, return retry timing

### Error Recovery Strategies

1. **Graceful Degradation:** If explainability module fails, return classification without explanations
2. **Retry Logic:** Implement exponential backoff for transient database errors
3. **Circuit Breaker:** Temporarily disable failing components to prevent cascade failures
4. **Fallback Responses:** Return cached results or default responses when possible
5. **User Guidance:** Provide actionable error messages (e.g., "Try better lighting" for low quality images)

## Testing Strategy

The testing strategy employs a dual approach combining unit tests for specific scenarios and property-based tests for universal correctness guarantees.

### Unit Testing Approach

**Framework:** pytest (Python backend), Jest (React frontend)

**Unit Test Coverage:**

1. **Preprocessing Module:**
   - Test image format validation with specific JPEG, PNG, HEIC files
   - Test file size validation with 9MB (pass) and 11MB (fail) files
   - Test glare detection with synthetic glare-affected images
   - Test primary product detection with multi-object images
   - Edge case: Completely black or white images
   - Edge case: Images with extreme aspect ratios (1:10, 10:1)

2. **Model Inference:**
   - Test model loading and initialization
   - Test prediction output format with sample images
   - Test feature map extraction for explainability
   - Edge case: Batch size of 1 vs multiple images

3. **Explainability Module:**
   - Test Grad-CAM heatmap generation with known activations
   - Test textual reason generation with mock feature scores
   - Test heatmap overlay rendering
   - Edge case: Images where all regions have equal importance

4. **API Endpoints:**
   - Test /classify endpoint with valid image
   - Test /classify endpoint with invalid inputs
   - Test /feedback endpoint with valid feedback
   - Test rate limiting behavior
   - Edge case: Concurrent requests to same endpoint

5. **Database Operations:**
   - Test classification logging with complete data
   - Test feedback storage and retrieval
   - Test metrics calculation with sample data
   - Edge case: Database connection failures

**Unit Test Example:**

```python
def test_image_format_validation():
    """Test that valid formats are accepted and invalid are rejected"""
    # Valid formats
    assert validate_image("test.jpg") == (True, "")
    assert validate_image("test.png") == (True, "")
    assert validate_image("test.heic") == (True, "")
    
    # Invalid formats
    assert validate_image("test.txt")[0] == False
    assert validate_image("test.pdf")[0] == False
    assert "Unsupported" in validate_image("test.gif")[1]
```

### Property-Based Testing Approach

**Framework:** Hypothesis (Python)

**Configuration:** Each property test should run a minimum of 100 iterations to ensure robust validation across diverse inputs.

**Property Test Coverage:**

1. **Input Validation Properties:**
   - **Property 1 & 2:** Generate random valid/invalid image files and verify acceptance/rejection
   - Strategy: Use Hypothesis to generate byte arrays with valid/invalid image headers

2. **Output Format Properties:**
   - **Property 3:** Generate random images, verify output always contains one label and score in [0,100]
   - **Property 4:** Generate classifications with random confidence scores, verify warning appears when < 60%

3. **Preprocessing Properties:**
   - **Property 8 & 9:** Generate random images of various sizes, verify output dimensions and normalization
   - Strategy: Use PIL to generate random RGB images, check preprocessed tensor properties

4. **Explainability Properties:**
   - **Property 5:** Generate random "Fake" classifications, verify heatmap is always produced
   - **Property 6:** Generate random classifications, verify at least 3 reasons are returned

5. **Feature Extraction Properties:**
   - **Property 15:** Generate random product images, verify all required features are extracted
   - Strategy: Mock feature extractor, verify output dictionary contains all required keys

6. **Logging Properties:**
   - **Property 17:** Generate random classification events, verify all required fields are logged
   - **Property 18:** Generate random feedback, verify linkage to classification exists

**Property Test Example:**

```python
from hypothesis import given, strategies as st
import numpy as np

@given(st.integers(min_value=0, max_value=100))
def test_low_confidence_warning_property(confidence_score):
    """
    Feature: fake-product-detection, Property 4: Low confidence warning
    For any confidence score, warning should appear if and only if score < 60%
    """
    result = format_classification_result(
        classification="Fake",
        confidence=confidence_score
    )
    
    has_warning = result.get("warning") is not None
    should_have_warning = confidence_score < 60
    
    assert has_warning == should_have_warning, \
        f"Warning mismatch for confidence {confidence_score}"

@given(st.integers(min_value=1, max_value=5000))
def test_preprocessing_dimension_consistency(image_size):
    """
    Feature: fake-product-detection, Property 8: Preprocessing dimension consistency
    For any input image size, output should have consistent dimensions
    """
    # Generate random image
    img = np.random.randint(0, 255, (image_size, image_size, 3), dtype=np.uint8)
    
    # Preprocess
    preprocessed = preprocess_image(img)
    
    # Verify output dimensions
    assert preprocessed.shape == (224, 224, 3), \
        f"Expected (224,224,3), got {preprocessed.shape}"

@given(st.lists(st.text(), min_size=1, max_size=10))
def test_explanation_completeness_property(mock_features):
    """
    Feature: fake-product-detection, Property 6: Explanation completeness
    For any classification, at least 3 reasons should be provided
    """
    reasons = generate_explanations(
        classification="Fake",
        features={"logo_clarity": 0.5, "text_alignment": 0.6}
    )
    
    assert len(reasons) >= 3, \
        f"Expected at least 3 reasons, got {len(reasons)}"
```

### Integration Testing

**Scope:** Test end-to-end workflows combining multiple components

1. **Full Classification Pipeline:**
   - Upload image → Preprocess → Classify → Generate explanations → Return response
   - Verify complete flow with real model and database

2. **Feedback Loop:**
   - Submit classification → Receive result → Submit feedback → Verify storage and flagging

3. **API Contract Testing:**
   - Test all API endpoints with various payloads
   - Verify response schemas match OpenAPI specification

4. **Database Integration:**
   - Test classification logging with real database
   - Test metrics calculation with real data

### Performance Testing

**Load Testing:**
- Simulate 100 concurrent users uploading images
- Verify 95th percentile response time < 5 seconds
- Verify no memory leaks during sustained load

**Stress Testing:**
- Test with very large images (near 10MB limit)
- Test with unusual image dimensions (very wide/tall)
- Test with edge case images (all black, all white, random noise)

### Testing Workflow

1. **Development:** Run unit tests and property tests on every code change
2. **Pre-commit:** Run fast unit tests (<30 seconds total)
3. **CI Pipeline:** Run full test suite including property tests (100 iterations each)
4. **Pre-deployment:** Run integration tests and performance tests
5. **Post-deployment:** Run smoke tests to verify production deployment

### Test Data Management

**Training/Validation Data:**
- Collect 5000+ images across 5 product categories (cosmetics, electronics, apparel, pharmaceuticals, accessories)
- 50/50 split between authentic and counterfeit
- Sources: Web scraping, public datasets, manual collection
- Manual verification by domain experts

**Test Data:**
- Hold out 20% of collected data for final testing
- Create synthetic test cases for edge conditions
- Generate adversarial examples to test robustness

**Mock Data:**
- Create fixtures for unit tests (small set of representative images)
- Generate synthetic images for property tests
- Use faker library for generating test metadata

## Deployment Architecture

### Development Environment

```
Developer Machine
├── Python 3.9+ virtual environment
├── Local PostgreSQL database
├── Local Redis instance
├── Model files in ./models/
└── Frontend dev server (React)
```

### Production Environment

```
Load Balancer (NGINX)
    ↓
┌─────────────────────────────────────┐
│   Application Servers (3x)          │
│   - FastAPI + Uvicorn               │
│   - Model loaded in memory          │
│   - Gunicorn for process management │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Database Layer                    │
│   - PostgreSQL (primary + replica)  │
│   - Redis (caching + rate limiting) │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Storage Layer                     │
│   - S3 for temporary images         │
│   - S3 for model artifacts          │
└─────────────────────────────────────┘
```

### Containerization

**Docker Compose for Development:**

```yaml
services:
  backend:
    build: ./backend
    ports: ["8000:8000"]
    volumes: ["./models:/app/models"]
    environment:
      - DATABASE_URL=postgresql://postgres:123123@db:5432/fakedetect
      - REDIS_URL=redis://redis:6379
  
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    environment:
      - REACT_APP_API_URL=http://localhost:8000
  
  db:
    image: postgres:14
    volumes: ["postgres_data:/var/lib/postgresql/data"]
  
  redis:
    image: redis:7
```

**Production Dockerfile (Backend):**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY ./src /app/src
COPY ./models /app/models

# Run with gunicorn
CMD ["gunicorn", "src.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

### Scaling Considerations

1. **Horizontal Scaling:** Add more application server instances behind load balancer
2. **Model Serving:** Consider TensorFlow Serving or TorchServe for dedicated model inference
3. **Caching:** Cache preprocessing results for identical images (hash-based)
4. **Async Processing:** Use Celery + RabbitMQ for batch processing if needed
5. **CDN:** Serve frontend static assets through CDN

### Monitoring and Observability

**Metrics to Track:**
- Request rate and response times (p50, p95, p99)
- Model inference latency
- Classification distribution (Original vs Fake ratio)
- Confidence score distribution
- Error rates by error type
- Database query performance
- Memory and CPU usage

**Logging:**
- Structured JSON logs with request IDs
- Log levels: DEBUG (dev), INFO (prod), ERROR (always)
- Centralized logging with ELK stack or CloudWatch

**Alerting:**
- Alert if error rate > 5%
- Alert if p95 response time > 7 seconds
- Alert if model inference fails
- Alert if database connection fails

## Security Considerations

1. **Input Validation:** Strict file type and size validation to prevent malicious uploads
2. **Rate Limiting:** Prevent abuse with per-IP rate limits (100 requests/hour)
3. **HTTPS Only:** Enforce TLS 1.2+ for all connections
4. **API Authentication:** JWT tokens for API access (if needed for future integrations)
5. **SQL Injection Prevention:** Use parameterized queries with SQLAlchemy ORM
6. **XSS Prevention:** Sanitize all user inputs in frontend
7. **CORS Configuration:** Restrict allowed origins in production
8. **Secrets Management:** Use environment variables or secret management service for credentials
9. **Image Scanning:** Scan uploaded images for malware before processing
10. **Data Retention:** Automatically delete temporary images after 24 hours

## Future Enhancements

1. **Mobile Application:** Native iOS/Android apps with camera integration
2. **Real-time Detection:** Process video streams for live product verification
3. **AR Overlay:** Augmented reality highlighting of suspicious packaging elements
4. **Blockchain Integration:** Verify product authenticity against blockchain supply chain records
5. **Multi-language Support:** Support product text in multiple languages
6. **Batch Processing:** Allow users to upload multiple images at once
7. **Product Database:** Build reference database of authentic products for comparison
8. **Crowdsourced Verification:** Allow users to contribute verified authentic/fake samples
9. **Browser Extension:** Chrome/Firefox extension for e-commerce site integration
10. **API Marketplace:** Offer API access to e-commerce platforms and retailers
