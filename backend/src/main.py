"""
Main FastAPI application entry point.
"""
import os
import time
import uuid
from datetime import datetime, timedelta
from typing import Optional
from io import BytesIO

from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import redis
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db, engine
from src.db_models import Base, Classification, Feedback
from src.preprocessor import ImagePreprocessor
from src.classifier import ProductClassifier
from src.explainability import ExplainabilityModule
from src.security import sanitize_filename, sanitize_text_input, validate_image_content, validate_request_id
from src.cleanup_service import CleanupService
from src.logging_config import setup_logging, RequestLogger
from src.metrics import metrics_collector

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Fake Product Detection API",
    description="""
## Machine Learning-Powered Product Authenticity Verification

This API uses deep learning to detect fake products from images.

### Features
* **Image Classification**: Classify products as Original or Fake
* **Confidence Scoring**: Get confidence levels for predictions
* **Visual Explanations**: Grad-CAM heatmaps showing decision areas
* **Textual Explanations**: Human-readable reasons for classifications
* **User Feedback**: Submit feedback to improve model accuracy
* **Rate Limiting**: 100 requests per hour per IP address

### Authentication
Currently no authentication required. Rate limiting applies per IP address.

### Rate Limits
* Classification endpoint: 100 requests/hour per IP
* Other endpoints: No limit

### Supported Image Formats
* JPEG (.jpg, .jpeg)
* PNG (.png)
* HEIC (.heic)

### Maximum File Size
10 MB per image

### Response Times
* Typical: 1-3 seconds
* Maximum: 120 seconds (timeout)
    """,
    version=settings.model_version,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "classification",
            "description": "Image classification operations",
        },
        {
            "name": "feedback",
            "description": "User feedback submission",
        },
        {
            "name": "monitoring",
            "description": "Health checks and statistics",
        },
        {
            "name": "maintenance",
            "description": "Administrative operations",
        },
    ]
)

# Configure CORS - Allow frontend to access API
# Use environment variable for production, fallback to localhost for development
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
print(f"Configuring CORS with origins: {allowed_origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Only allow necessary methods
    allow_headers=["Content-Type", "Authorization"],  # Restrict headers
    expose_headers=["Content-Type"]
)

# Initialize Redis for rate limiting
try:
    redis_client = redis.from_url(settings.redis_url, decode_responses=True)
    redis_available = True
except Exception:
    redis_client = None
    redis_available = False

# Initialize components (lazy loading)
preprocessor = None
classifier = None
explainability = None
cleanup_service = CleanupService(temp_dir="temp_uploads")

# Setup logging
try:
    logger = setup_logging(
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        log_format=os.getenv("LOG_FORMAT", "json"),
        log_file=os.getenv("LOG_FILE", "logs/app.log")
    )
except Exception as e:
    # Fallback to basic logging if setup fails
    import logging
    logger = logging.getLogger("fake_product_detection")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.error(f"Failed to setup structured logging: {e}")


# Startup event - cleanup old files (using lifespan context manager is preferred but on_event works)
@app.on_event("startup")
async def startup_event():
    """Run startup tasks."""
    try:
        logger.info("Application starting up")
        
        # Cleanup old temporary files
        deleted = cleanup_service.cleanup_old_images(max_age_hours=24)
        if deleted > 0:
            logger.info(f"Startup cleanup: Deleted {deleted} old temporary files", extra={"deleted_files": deleted})
    except Exception as e:
        logger.error(f"Error during startup: {e}")


def get_components():
    """Lazy load ML components."""
    global preprocessor, classifier, explainability
    
    if preprocessor is None:
        preprocessor = ImagePreprocessor()
    
    if classifier is None:
        classifier = ProductClassifier(num_classes=2)
        # Try to load trained model if exists
        if os.path.exists(settings.model_path):
            try:
                classifier.load_model(settings.model_path)
            except Exception as e:
                print(f"Warning: Could not load model: {e}")
    
    if explainability is None and classifier is not None and classifier.model is not None:
        explainability = ExplainabilityModule(classifier.model)
    
    return preprocessor, classifier, explainability


# Pydantic models for API
class FeedbackRequest(BaseModel):
    """Request model for user feedback."""
    request_id: str = Field(
        description="Classification request ID (UUID format)",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    is_correct: bool = Field(
        description="Whether the classification was correct",
        json_schema_extra={"example": True}
    )
    user_label: Optional[str] = Field(
        None, 
        description="User's label if classification was incorrect (Original or Fake)",
        json_schema_extra={"example": "Original"}
    )
    comments: Optional[str] = Field(
        None, 
        max_length=500, 
        description="Optional comments about the classification",
        json_schema_extra={"example": "The product looks authentic to me"}
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "is_correct": False,
                "user_label": "Original",
                "comments": "This is actually an original product"
            }
        }
    }


class ClassificationResponse(BaseModel):
    """Response model for classification."""
    request_id: str = Field(
        description="Unique request identifier for this classification",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    label: str = Field(
        description="Classification result: 'Original' or 'Fake'",
        json_schema_extra={"example": "Original"}
    )
    confidence: float = Field(
        description="Confidence score between 0 and 1",
        ge=0.0,
        le=1.0,
        json_schema_extra={"example": 0.87}
    )
    probabilities: dict = Field(
        description="Probability distribution for each class",
        json_schema_extra={"example": {"Original": 0.87, "Fake": 0.13}}
    )
    heatmap_available: bool = Field(
        description="Whether Grad-CAM heatmap was generated (only for Fake classifications)",
        json_schema_extra={"example": False}
    )
    explanations: list = Field(
        description="List of textual explanations for the classification",
        json_schema_extra={"example": [
            "Logo shows clear, high-quality printing",
            "Print quality indicates professional manufacturing",
            "Color consistency matches authentic products"
        ]}
    )
    low_confidence_warning: bool = Field(
        description="Warning flag if confidence is below threshold",
        json_schema_extra={"example": False}
    )
    processing_time_ms: float = Field(
        description="Processing time in milliseconds",
        json_schema_extra={"example": 1234.56}
    )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "label": "Original",
                "confidence": 0.87,
                "probabilities": {"Original": 0.87, "Fake": 0.13},
                "heatmap_available": False,
                "explanations": [
                    "Logo shows clear, high-quality printing",
                    "Print quality indicates professional manufacturing",
                    "Color consistency matches authentic products"
                ],
                "low_confidence_warning": False,
                "processing_time_ms": 1234.56
            }
        }
    }


# Middleware for security headers
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Add security headers to all responses."""
    response = await call_next(request)
    
    # Security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    
    return response


# Middleware for request logging and metrics
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing and collect metrics."""
    start_time = time.time()
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    
    # Create request logger
    req_logger = RequestLogger(logger, request_id)
    request.state.logger = req_logger
    
    # Log request start
    req_logger.info(
        f"Request started: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "client_ip": request.client.host if request.client else None
        }
    )
    
    response = await call_next(request)
    
    # Calculate processing time
    process_time = (time.time() - start_time) * 1000
    
    # Record metrics
    metrics_collector.record_request(
        duration_ms=process_time,
        endpoint=request.url.path,
        status_code=response.status_code
    )
    
    # Log request completion
    req_logger.info(
        f"Request completed: {request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "processing_time_ms": process_time
        }
    )
    
    return response


# Rate limiting dependency
async def check_rate_limit(request: Request):
    """Check rate limit for IP address."""
    if not redis_available:
        return  # Skip if Redis not available
    
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    try:
        current = redis_client.get(key)
        if current is None:
            redis_client.setex(key, 3600, 1)  # 1 hour expiry
        else:
            count = int(current)
            if count >= settings.rate_limit_per_hour:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded",
                    headers={"Retry-After": "3600"}
                )
            redis_client.incr(key)
    except redis.RedisError:
        pass  # Continue if Redis fails


@app.get(
    "/",
    tags=["monitoring"],
    summary="API Root",
    description="Get basic API information and links to documentation"
)
async def root():
    """
    Root endpoint providing API information.
    
    Returns basic information about the API including version and documentation links.
    """
    return {
        "message": "Fake Product Detection API",
        "version": settings.model_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/health"
    }


@app.get(
    "/api/v1/health",
    tags=["monitoring"],
    summary="Health Check",
    description="Check the health status of the API and its dependencies",
    responses={
        200: {
            "description": "Service is healthy or degraded",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "model_loaded": True,
                        "database_connected": True,
                        "redis_available": True,
                        "version": "1.0.0"
                    }
                }
            }
        }
    }
)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    
    Checks the status of:
    - Model loading
    - Database connectivity
    - Redis availability
    
    Returns 'healthy' if all systems operational, 'degraded' otherwise.
    """
    # Check model status
    model_loaded = False
    if os.path.exists(settings.model_path):
        try:
            _, clf, _ = get_components()
            model_loaded = clf is not None and clf.model is not None
        except Exception:
            pass
    
    # Check database connectivity
    db_connected = False
    try:
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_connected = True
    except Exception as e:
        print(f"Database connection error: {e}")
        pass
    
    status = "healthy" if (model_loaded and db_connected) else "degraded"
    
    return {
        "status": status,
        "model_loaded": model_loaded,
        "database_connected": db_connected,
        "redis_available": redis_available,
        "version": settings.model_version
    }


@app.post(
    "/api/v1/classify",
    response_model=ClassificationResponse,
    tags=["classification"],
    summary="Classify Product Image",
    description="Upload a product image to classify it as Original or Fake",
    dependencies=[Depends(check_rate_limit)],
    responses={
        200: {
            "description": "Successful classification",
            "model": ClassificationResponse,
        },
        400: {
            "description": "Invalid input (wrong format, too large, corrupted)",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid file format. Allowed: jpg, jpeg, png, heic"}
                }
            }
        },
        429: {
            "description": "Rate limit exceeded",
            "content": {
                "application/json": {
                    "example": {"detail": "Rate limit exceeded"}
                }
            },
            "headers": {
                "Retry-After": {
                    "description": "Seconds until rate limit resets",
                    "schema": {"type": "integer"}
                }
            }
        },
        503: {
            "description": "Service unavailable (model not loaded)",
            "content": {
                "application/json": {
                    "example": {"detail": "Model not loaded. Please train a model first."}
                }
            }
        }
    }
)
async def classify_image(
    request: Request,
    file: UploadFile = File(
        ...,
        description="Product image file (JPEG, PNG, or HEIC format, max 10MB)"
    ),
    db: Session = Depends(get_db)
):
    """
    Classify a product image as Original or Fake.
    
    This endpoint accepts an image file and returns:
    - Classification label (Original or Fake)
    - Confidence score (0-1)
    - Probability distribution
    - Visual explanations (Grad-CAM heatmap for Fake classifications)
    - Textual explanations (human-readable reasons)
    - Low confidence warning if applicable
    
    **Rate Limit**: 100 requests per hour per IP address
    
    **Supported Formats**: JPEG, PNG, HEIC
    
    **Maximum File Size**: 10 MB
    
    **Processing Time**: Typically 1-3 seconds
    """
    start_time = time.time()
    request_id = request.state.request_id
    
    # Sanitize filename
    safe_filename = sanitize_filename(file.filename)
    
    # Validate file format
    file_ext = safe_filename.split('.')[-1].lower() if '.' in safe_filename else ''
    if file_ext not in settings.allowed_formats:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file format. Allowed: {', '.join(settings.allowed_formats)}"
        )
    
    # Read file
    try:
        contents = await file.read()
        if len(contents) > settings.max_file_size_mb * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.max_file_size_mb}MB"
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    
    # Validate image content (check magic bytes)
    is_valid_image, error_msg = validate_image_content(contents)
    if not is_valid_image:
        raise HTTPException(status_code=400, detail=error_msg)
    
    # Get components
    try:
        prep, clf, expl = get_components()
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service initialization failed: {str(e)}")
    
    if clf is None or clf.model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train a model first."
        )
    
    # Preprocess image
    try:
        preprocessed, metadata, error = prep.preprocess(contents)
        if error:
            raise HTTPException(status_code=400, detail=error)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Preprocessing failed: {str(e)}")
    
    # Classify
    try:
        inference_start = time.time()
        label, confidence, probabilities = clf.predict(preprocessed, return_probabilities=True)
        inference_time = (time.time() - inference_start) * 1000
        
        # Convert probabilities array to dict format
        prob_dict = {}
        if probabilities is not None:
            prob_list = probabilities.tolist() if hasattr(probabilities, 'tolist') else probabilities
            # Assuming binary classification: index 0 = Original, index 1 = Fake
            prob_dict = {
                "Original": float(prob_list[0]) if len(prob_list) > 0 else 0.0,
                "Fake": float(prob_list[1]) if len(prob_list) > 1 else 0.0
            }
        
        # Store results in simple dict (not using full ClassificationResult dataclass)
        # Convert confidence from 0-100 to 0-1 for response model
        result = {
            "label": label,
            "confidence": confidence / 100.0,  # Convert to 0-1 range
            "probabilities": prob_dict
        }
        
        # Log classification event
        if hasattr(request.state, 'logger'):
            request.state.logger.info(
                f"Classification completed: {label}",
                extra={
                    "label": label,
                    "confidence": confidence,
                    "inference_time_ms": inference_time
                }
            )
    except Exception as e:
        if hasattr(request.state, 'logger'):
            request.state.logger.error(f"Classification failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Classification failed: {str(e)}")
    
    # Generate explanations
    explanations = []
    heatmap_available = False
    
    if expl is not None:
        try:
            # Generate heatmap for fake classifications
            if result["label"].lower() == "fake":
                heatmap = expl.generate_gradcam(preprocessed, class_index=0)
                heatmap_available = heatmap is not None
            
            # Extract features and generate explanations
            features = expl.extract_visual_features(preprocessed)
            explanations = expl.generate_textual_reasons(features, result["label"])
        except Exception as e:
            print(f"Warning: Explainability failed: {e}")
    
    # Check for low confidence
    low_confidence = result["confidence"] < (settings.confidence_threshold / 100.0)
    
    # Log classification to database
    try:
        classification = Classification(
            request_id=request_id,
            image_filename=safe_filename,  # Use sanitized filename
            predicted_label=result["label"],
            confidence=result["confidence"],
            probabilities=list(result["probabilities"].values()),  # Store as list in DB
            image_metadata=metadata.__dict__ if metadata else {},  # Renamed from metadata
            explanations=explanations,
            processing_time_ms=(time.time() - start_time) * 1000
        )
        db.add(classification)
        db.commit()
    except Exception as e:
        print(f"Warning: Failed to log classification: {e}")
        db.rollback()
    
    processing_time = (time.time() - start_time) * 1000
    
    # Record classification metrics (confidence is 0-1 in result)
    metrics_collector.record_classification(
        label=result["label"],
        confidence=result["confidence"],  # Already 0-1 range
        processing_time_ms=processing_time,
        inference_time_ms=inference_time if 'inference_time' in locals() else None
    )
    
    return ClassificationResponse(
        request_id=request_id,
        label=result["label"],
        confidence=result["confidence"],
        probabilities=result["probabilities"],
        heatmap_available=heatmap_available,
        explanations=explanations,
        low_confidence_warning=low_confidence,
        processing_time_ms=processing_time
    )


@app.post(
    "/api/v1/feedback",
    tags=["feedback"],
    summary="Submit Feedback",
    description="Submit user feedback on a classification result to help improve the model",
    responses={
        200: {
            "description": "Feedback received successfully",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Feedback received",
                        "feedback_id": 123,
                        "flagged_for_review": True
                    }
                }
            }
        },
        400: {
            "description": "Invalid request ID format",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid request ID format"}
                }
            }
        },
        404: {
            "description": "Classification request not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Classification request not found"}
                }
            }
        }
    }
)
async def submit_feedback(
    feedback_req: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """
    Submit user feedback on a classification result.
    
    Use this endpoint to provide feedback on whether a classification was correct.
    Incorrect classifications are automatically flagged for review to improve the model.
    
    **Parameters**:
    - **request_id**: The UUID from the classification response
    - **is_correct**: True if classification was correct, False otherwise
    - **user_label**: If incorrect, provide the correct label (Original or Fake)
    - **comments**: Optional additional comments
    
    **Note**: Incorrect classifications are automatically flagged for manual review.
    """
    # Validate request_id format
    if not validate_request_id(feedback_req.request_id):
        raise HTTPException(status_code=400, detail="Invalid request ID format")
    
    # Verify request_id exists
    classification = db.query(Classification).filter(
        Classification.request_id == feedback_req.request_id
    ).first()
    
    if not classification:
        raise HTTPException(status_code=404, detail="Classification request not found")
    
    # Sanitize text inputs
    sanitized_label = sanitize_text_input(feedback_req.user_label, max_length=50)
    sanitized_comments = sanitize_text_input(feedback_req.comments, max_length=500)
    
    # Create feedback record
    feedback = Feedback(
        classification_id=classification.id,
        is_correct=feedback_req.is_correct,
        user_label=sanitized_label,
        comments=sanitized_comments,
        flagged_for_review=not feedback_req.is_correct  # Flag incorrect classifications
    )
    
    try:
        db.add(feedback)
        db.commit()
        db.refresh(feedback)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to save feedback: {str(e)}")
    
    return {
        "message": "Feedback received",
        "feedback_id": feedback.id,
        "flagged_for_review": feedback.flagged_for_review
    }


@app.post(
    "/api/v1/cleanup",
    tags=["maintenance"],
    summary="Trigger Cleanup",
    description="Manually trigger cleanup of temporary files older than 24 hours",
    responses={
        200: {
            "description": "Cleanup completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "deleted_files": 15,
                        "remaining_files": 3,
                        "directory_size_bytes": 1048576,
                        "message": "Cleanup complete. Deleted 15 files."
                    }
                }
            }
        }
    }
)
async def trigger_cleanup():
    """
    Manually trigger cleanup of old temporary files.
    
    This endpoint removes temporary image files older than 24 hours.
    Cleanup also runs automatically on server startup.
    
    **Admin endpoint** - Use for maintenance purposes.
    
    Returns:
    - Number of files deleted
    - Number of remaining files
    - Total directory size in bytes
    """
    deleted = cleanup_service.cleanup_old_images(max_age_hours=24)
    file_count = cleanup_service.get_temp_file_count()
    dir_size = cleanup_service.get_temp_dir_size()
    
    return {
        "deleted_files": deleted,
        "remaining_files": file_count,
        "directory_size_bytes": dir_size,
        "message": f"Cleanup complete. Deleted {deleted} files."
    }


@app.get(
    "/api/v1/metrics",
    tags=["monitoring"],
    summary="Get Performance Metrics",
    description="Get real-time performance metrics and monitoring data",
    responses={
        200: {
            "description": "Metrics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "timestamp": "2024-01-01T12:00:00Z",
                        "requests": {
                            "total_requests": 1523,
                            "avg_response_time_ms": 1234.56,
                            "requests_per_minute": 25,
                            "error_rate": 0.02
                        },
                        "classifications": {
                            "total_classifications": 1200,
                            "avg_processing_time_ms": 1500.0,
                            "avg_confidence": 0.85,
                            "label_distribution": {"Original": 700, "Fake": 500}
                        }
                    }
                }
            }
        }
    }
)
async def get_metrics():
    """
    Get real-time performance metrics.
    
    Returns comprehensive metrics including:
    - Request statistics (count, response times, error rates)
    - Classification metrics (processing times, confidence scores, label distribution)
    - Model inference performance
    - Error tracking
    
    **Note**: Metrics are collected in-memory for recent requests (last 1000).
    """
    return metrics_collector.get_all_metrics()


@app.get(
    "/api/v1/stats",
    tags=["monitoring"],
    summary="Get Statistics",
    description="Get system statistics and performance metrics from database",
    responses={
        200: {
            "description": "Statistics retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "total_classifications": 1523,
                        "accuracy_estimate": 0.89,
                        "average_confidence": 0.82,
                        "category_distribution": {
                            "original": 892,
                            "fake": 631
                        },
                        "feedback_count": 234
                    }
                }
            }
        }
    }
)
async def get_statistics(db: Session = Depends(get_db)):
    """
    Get system statistics and performance metrics.
    
    Returns comprehensive statistics including:
    - **total_classifications**: Total number of classifications performed
    - **accuracy_estimate**: Estimated accuracy based on user feedback (null if no feedback)
    - **average_confidence**: Average confidence score across all classifications
    - **category_distribution**: Count of Original vs Fake classifications
    - **feedback_count**: Number of feedback submissions received
    
    **Note**: Accuracy estimate is only available when user feedback has been submitted.
    """
    # Total classifications
    total_classifications = db.query(Classification).count()
    
    # Get all classifications with feedback
    classifications_with_feedback = db.query(Classification).join(
        Feedback, Classification.id == Feedback.classification_id
    ).all()
    
    # Calculate accuracy from feedback
    if classifications_with_feedback:
        correct_count = sum(1 for c in classifications_with_feedback 
                          if db.query(Feedback).filter(
                              Feedback.classification_id == c.id,
                              Feedback.is_correct == True
                          ).first())
        accuracy = correct_count / len(classifications_with_feedback)
    else:
        accuracy = None
    
    # Average confidence
    all_classifications = db.query(Classification).all()
    if all_classifications:
        avg_confidence = sum(c.confidence for c in all_classifications) / len(all_classifications)
    else:
        avg_confidence = 0.0
    
    # Category-wise performance
    original_count = db.query(Classification).filter(
        Classification.predicted_label == "Original"
    ).count()
    fake_count = db.query(Classification).filter(
        Classification.predicted_label == "Fake"
    ).count()
    
    return {
        "total_classifications": total_classifications,
        "accuracy_estimate": accuracy,
        "average_confidence": avg_confidence,
        "category_distribution": {
            "original": original_count,
            "fake": fake_count
        },
        "feedback_count": len(classifications_with_feedback)
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
