"""
Test runner script for all backend tests.

This script runs all tests and provides a summary of results.
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 70)
print("🧪 FAKE PRODUCT DETECTION - TEST SUITE")
print("=" * 70)

# Check if pytest is installed
try:
    import pytest
    print("✅ pytest is installed")
except ImportError:
    print("❌ pytest is not installed")
    print("\n📦 Installing required packages...")
    print("Run: pip install -r backend/requirements.txt")
    sys.exit(1)

# Check if other dependencies are available
try:
    import hypothesis
    print("✅ hypothesis is installed")
except ImportError:
    print("⚠️  hypothesis is not installed (required for property tests)")

try:
    import fastapi
    print("✅ fastapi is installed")
except ImportError:
    print("⚠️  fastapi is not installed")

try:
    import sqlalchemy
    print("✅ sqlalchemy is installed")
except ImportError:
    print("⚠️  sqlalchemy is not installed")

print("\n" + "=" * 70)
print("📋 TEST CATEGORIES")
print("=" * 70)

test_categories = {
    "Preprocessing Tests": [
        "tests/test_property_preprocessing.py",
        "tests/test_property_dimension_consistency.py",
        "tests/test_property_normalization.py",
        "tests/test_property_lighting_normalization.py",
        "tests/test_property_low_quality_warning.py",
    ],
    "Classification Tests": [
        "tests/test_property_classification.py",
        "tests/test_property_classification_output.py",
        "tests/test_property_low_confidence.py",
        "tests/test_property_classification_logging.py",
    ],
    "Explainability Tests": [
        "tests/test_property_heatmap_generation.py",
        "tests/test_property_feature_extraction.py",
        "tests/test_property_explanation_completeness.py",
        "tests/test_property_feature_comparison.py",
    ],
    "API Tests": [
        "tests/test_property_api_response_format.py",
        "tests/test_property_rate_limiting.py",
        "tests/test_property_feedback_flagging.py",
        "tests/test_property_metrics_report.py",
        "tests/test_property_daily_accuracy.py",
    ],
    "Logging & Metrics Tests": [
        "tests/test_property_log_anonymization.py",
        "tests/test_metrics_calculation.py",
    ],
}

# Count existing test files
total_files = 0
existing_files = 0

for category, files in test_categories.items():
    print(f"\n{category}:")
    for test_file in files:
        total_files += 1
        if os.path.exists(test_file):
            print(f"  ✅ {os.path.basename(test_file)}")
            existing_files += 1
        else:
            print(f"  ⚠️  {os.path.basename(test_file)} (not found)")

print(f"\n📊 Test files: {existing_files}/{total_files} found")

print("\n" + "=" * 70)
print("🚀 RUNNING TESTS")
print("=" * 70)

# Run pytest
print("\nRunning all tests in tests/ directory...\n")

# Pytest arguments
args = [
    "tests/",
    "-v",                    # Verbose
    "--tb=short",            # Short traceback
    "--color=yes",           # Colored output
    "-x",                    # Stop on first failure
]

# Run tests
exit_code = pytest.main(args)

print("\n" + "=" * 70)
if exit_code == 0:
    print("✅ ALL TESTS PASSED")
else:
    print(f"❌ TESTS FAILED (exit code: {exit_code})")
print("=" * 70)

sys.exit(exit_code)
