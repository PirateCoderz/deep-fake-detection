# Complete Testing Guide - Fake Product Detection System

## Overview

This guide covers all testing for the Fake Product Detection system, including setup, running tests, and interpreting results.

## Prerequisites

### 1. Install Dependencies

```bash
# Install all Python dependencies
pip install -r backend/requirements.txt
```

Required packages for testing:
- `pytest` - Test framework
- `pytest-asyncio` - Async test support
- `hypothesis` - Property-based testing
- `fastapi` - API framework
- `sqlalchemy` - Database ORM
- `redis` - Caching (optional for some tests)

### 2. Database Setup

Ensure PostgreSQL is running and database is created:

```bash
# Test database connection
python test_db_connection.py
```

If database doesn't exist, follow `DATABASE_SETUP_GUIDE.md` or `PGADMIN_VISUAL_GUIDE.md`.

### 3. Environment Configuration

Create `.env` file in project root:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/fakedetect
REDIS_URL=redis://localhost:6379/0
```

## Test Structure

### Test Categories

```
tests/
├── Preprocessing Tests (5 files)
│   ├── test_property_preprocessing.py
│   ├── test_property_dimension_consistency.py
│   ├── test_property_normalization.py
│   ├── test_property_lighting_normalization.py
│   └── test_property_low_quality_warning.py
│
├── Classification Tests (4 files)
│   ├── test_property_classification.py
│   ├── test_property_classification_output.py
│   ├── test_property_low_confidence.py
│   └── test_property_classification_logging.py
│
├── Explainability Tests (4 files)
│   ├── test_property_heatmap_generation.py
│   ├── test_property_feature_extraction.py
│   ├── test_property_explanation_completeness.py
│   └── test_property_feature_comparison.py
│
├── API Tests (5 files)
│   ├── test_property_api_response_format.py
│   ├── test_property_rate_limiting.py
│   ├── test_property_feedback_flagging.py
│   ├── test_property_metrics_report.py
│   └── test_property_daily_accuracy.py
│
└── Logging & Metrics Tests (2 files)
    ├── test_property_log_anonymization.py
    └── test_metrics_calculation.py
```

## Running Tests

### Method 1: Run All Tests (Recommended)

```bash
# Using the test runner script
python run_all_tests.py
```

This script:
- Checks dependencies
- Lists all test files
- Runs all tests with verbose output
- Provides summary

### Method 2: Using pytest Directly

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend/src --cov-report=html

# Run specific category
pytest tests/test_property_api_*.py -v

# Run single test file
pytest tests/test_property_log_anonymization.py -v

# Run with detailed output
pytest tests/ -vv --tb=long

# Stop on first failure
pytest tests/ -x

# Run only failed tests from last run
pytest tests/ --lf
```

### Method 3: Run by Category

**Preprocessing Tests:**
```bash
pytest tests/test_property_preprocessing.py \
       tests/test_property_dimension_consistency.py \
       tests/test_property_normalization.py \
       tests/test_property_lighting_normalization.py \
       tests/test_property_low_quality_warning.py -v
```

**Classification Tests:**
```bash
pytest tests/test_property_classification.py \
       tests/test_property_classification_output.py \
       tests/test_property_low_confidence.py \
       tests/test_property_classification_logging.py -v
```

**Explainability Tests:**
```bash
pytest tests/test_property_heatmap_generation.py \
       tests/test_property_feature_extraction.py \
       tests/test_property_explanation_completeness.py \
       tests/test_property_feature_comparison.py -v
```

**API Tests:**
```bash
pytest tests/test_property_api_response_format.py \
       tests/test_property_rate_limiting.py \
       tests/test_property_feedback_flagging.py \
       tests/test_property_metrics_report.py \
       tests/test_property_daily_accuracy.py -v
```

**Logging & Metrics Tests:**
```bash
pytest tests/test_property_log_anonymization.py \
       tests/test_metrics_calculation.py -v
```

## Test Coverage

### Current Test Count

| Category | Test Files | Approximate Tests |
|----------|-----------|-------------------|
| Preprocessing | 5 | ~50 tests |
| Classification | 4 | ~40 tests |
| Explainability | 4 | ~50 tests |
| API | 5 | ~50 tests |
| Logging & Metrics | 2 | ~37 tests |
| **Total** | **20** | **~227 tests** |

### Property-Based Tests

Many tests use Hypothesis for property-based testing:
- Generates random inputs
- Tests properties that should always hold
- More thorough than example-based tests
- Default: 100 examples per property test

Example:
```python
@given(
    email=st.emails(),
    text_before=st.text(min_size=0, max_size=20),
    text_after=st.text(min_size=0, max_size=20)
)
@settings(max_examples=50, deadline=None)
def test_email_anonymization_property(self, email, text_before, text_after):
    # Test runs 50 times with different random inputs
    ...
```

## Test Output Interpretation

### Successful Test Run

```
tests/test_property_log_anonymization.py::TestLogAnonymization::test_email_anonymization PASSED [ 10%]
tests/test_property_log_anonymization.py::TestLogAnonymization::test_phone_anonymization PASSED [ 20%]
...
========================= 25 passed in 5.23s =========================
```

### Failed Test

```
FAILED tests/test_property_log_anonymization.py::TestLogAnonymization::test_email_anonymization
AssertionError: assert 'user@example.com' not in 'Contact user@example.com'
```

### Skipped Test

```
SKIPPED [1] tests/test_property_api_response_format.py:45: Model not loaded
```

This is normal if model hasn't been trained yet.

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'pytest'
```

**Solution:**
```bash
pip install -r backend/requirements.txt
```

### Issue 2: Database Connection Error

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
1. Start PostgreSQL service
2. Verify database exists: `python test_db_connection.py`
3. Check DATABASE_URL in `.env`

### Issue 3: Redis Connection Error

```
redis.exceptions.ConnectionError: Error connecting to Redis
```

**Solution:**
- Some tests will skip if Redis unavailable
- To run all tests, start Redis:
  ```bash
  # Using Docker
  docker run -d -p 6379:6379 redis
  
  # Or install Redis for Windows
  ```

### Issue 4: Model Not Found

```
pytest.skip: Model not loaded
```

**Solution:**
- This is expected if model hasn't been trained
- Tests will skip gracefully
- To train model: `python train.py`

### Issue 5: Import Errors

```
ImportError: cannot import name 'LoggingService'
```

**Solution:**
```bash
# Ensure you're in project root
cd /path/to/deep-fake-detection

# Run tests from project root
pytest tests/ -v
```

## Test Configuration

### pytest.ini

Located in `backend/pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
```

### Hypothesis Settings

Property tests use these settings:
- `max_examples`: Number of random inputs (default: 100)
- `deadline`: Time limit per test (None = unlimited)
- `database`: Stores examples for regression testing

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: fakedetect
        ports:
          - 5432:5432
      
      redis:
        image: redis:7
        ports:
          - 6379:6379
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/fakedetect
          REDIS_URL: redis://localhost:6379/0
        run: pytest tests/ -v --cov=backend/src
```

## Test Maintenance

### Adding New Tests

1. Create test file in `tests/` directory
2. Follow naming convention: `test_*.py`
3. Use appropriate test class: `Test*`
4. Use descriptive test names: `test_*`

Example:
```python
"""
Property Test: Description

Validates Requirement X.Y: Description
"""
import pytest
from hypothesis import given, strategies as st

class TestNewFeature:
    """Test new feature functionality."""
    
    def test_basic_functionality(self):
        """Test basic case."""
        assert True
    
    @given(value=st.integers())
    def test_property(self, value):
        """Property: Description."""
        assert value == value
```

### Updating Tests

When code changes:
1. Run tests: `pytest tests/ -v`
2. Fix failing tests
3. Update test expectations if behavior changed intentionally
4. Add new tests for new functionality

## Performance Testing

### Timing Tests

```bash
# Show slowest tests
pytest tests/ --durations=10

# Set timeout for tests
pytest tests/ --timeout=30
```

### Load Testing

For API endpoints:
```bash
# Install locust
pip install locust

# Create locustfile.py
# Run load test
locust -f locustfile.py
```

## Test Reports

### HTML Coverage Report

```bash
pytest tests/ --cov=backend/src --cov-report=html
```

Open `htmlcov/index.html` in browser to view coverage.

### JUnit XML Report

```bash
pytest tests/ --junitxml=test-results.xml
```

Useful for CI/CD integration.

### JSON Report

```bash
pip install pytest-json-report
pytest tests/ --json-report --json-report-file=report.json
```

## Best Practices

### 1. Test Isolation
- Each test should be independent
- Use fixtures for setup/teardown
- Don't rely on test execution order

### 2. Clear Test Names
```python
# Good
def test_email_anonymization_replaces_with_placeholder():
    ...

# Bad
def test_1():
    ...
```

### 3. Arrange-Act-Assert Pattern
```python
def test_example():
    # Arrange
    data = create_test_data()
    
    # Act
    result = function_under_test(data)
    
    # Assert
    assert result == expected
```

### 4. Use Fixtures
```python
@pytest.fixture
def db_session():
    db = create_session()
    yield db
    db.close()

def test_with_db(db_session):
    # Use db_session
    ...
```

### 5. Property-Based Testing
Use Hypothesis for testing properties:
```python
@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a
```

## Quick Reference

### Common Commands

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=backend/src

# Run specific file
pytest tests/test_property_log_anonymization.py -v

# Run specific test
pytest tests/test_property_log_anonymization.py::TestLogAnonymization::test_email_anonymization -v

# Stop on first failure
pytest tests/ -x

# Show print statements
pytest tests/ -s

# Run in parallel (requires pytest-xdist)
pytest tests/ -n auto
```

### Useful Flags

- `-v` - Verbose output
- `-vv` - Very verbose output
- `-s` - Show print statements
- `-x` - Stop on first failure
- `-k EXPRESSION` - Run tests matching expression
- `--lf` - Run last failed tests
- `--ff` - Run failed tests first
- `--tb=short` - Short traceback
- `--tb=long` - Long traceback
- `--durations=N` - Show N slowest tests

## Summary

✅ **20 test files** covering all major components  
✅ **~227 tests** ensuring system correctness  
✅ **Property-based testing** for thorough coverage  
✅ **Integration tests** for API endpoints  
✅ **Unit tests** for individual components  
✅ **Comprehensive documentation** for maintenance  

All tests are ready to run. Follow this guide to execute and maintain the test suite.
