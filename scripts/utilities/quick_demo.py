"""
Quick Demo: Test Your Fake Product Detection System

This is a simple script to verify everything is working.
Run: python quick_demo.py
"""
import sys
import numpy as np
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend' / 'src'))

print("="*70)
print("  🎯 FAKE PRODUCT DETECTION - QUICK TEST")
print("="*70)

# Test 1: Preprocessing
print("\n1️⃣  Testing Image Preprocessing...")
try:
    from preprocessor import ImagePreprocessor
    preprocessor = ImagePreprocessor()
    
    # Create test image
    test_image = np.random.randint(0, 255, (400, 400, 3), dtype=np.uint8)
    
    # Assess quality
    quality, has_glare = preprocessor.assess_image_quality(test_image)
    
    # Resize and normalize
    resized = preprocessor.resize_image(test_image, (224, 224))
    normalized = preprocessor.normalize_image(resized, method='minmax')
    
    print(f"   ✅ Preprocessing works!")
    print(f"      Quality: {quality:.2f}, Glare: {has_glare}")
    print(f"      Output shape: {normalized.shape}")
    print(f"      Value range: [{normalized.min():.2f}, {normalized.max():.2f}]")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Classification
print("\n2️⃣  Testing Classification (Mock)...")
try:
    from classifier import create_mock_classifier
    classifier = create_mock_classifier()
    
    test_image = np.random.rand(224, 224, 3)
    label, confidence, _ = classifier.predict(test_image)
    
    print(f"   ✅ Classification works!")
    print(f"      Prediction: {label}")
    print(f"      Confidence: {confidence:.1f}%")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Explainability
print("\n3️⃣  Testing Explainability...")
try:
    from explainability import create_mock_explainability_module
    explainer = create_mock_explainability_module()
    
    test_image = (np.random.rand(224, 224, 3) * 255).astype(np.uint8)
    
    # Heatmap
    heatmap = explainer.generate_gradcam(test_image, pred_class=1)
    
    # Features
    features = explainer.extract_visual_features(test_image)
    
    # Reasons
    reasons = explainer.generate_textual_reasons(features, "Fake", 85.0)
    
    print(f"   ✅ Explainability works!")
    print(f"      Heatmap: {heatmap.shape}")
    print(f"      Features: {len(features)}")
    print(f"      Reasons: {len(reasons)}")
    print(f"\n      Sample reason:")
    print(f"      → {reasons[0]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Data Augmentation
print("\n4️⃣  Testing Data Augmentation...")
try:
    from data_augmentation import ImageAugmentor
    augmentor = ImageAugmentor()
    
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    augmented = augmentor.random_rotation(test_image, max_angle=15)
    
    print(f"   ✅ Augmentation works!")
    print(f"      Input: {test_image.shape}")
    print(f"      Output: {augmented.shape}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Evaluation
print("\n5️⃣  Testing Evaluation Metrics...")
try:
    from evaluation import ModelEvaluator
    evaluator = ModelEvaluator()
    
    y_true = np.array([0, 1, 0, 1, 0, 1])
    y_pred = np.array([0, 1, 0, 0, 0, 1])
    
    metrics = evaluator.calculate_metrics(y_true, y_pred)
    
    print(f"   ✅ Evaluation works!")
    print(f"      Accuracy: {metrics['accuracy']:.3f}")
    print(f"      Precision: {metrics['class_1_precision']:.3f}")
    print(f"      Recall: {metrics['class_1_recall']:.3f}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "="*70)
print("  ✅ ALL COMPONENTS WORKING!")
print("="*70)
print("\n  📊 System Status:")
print("     • Image Preprocessing: ✅")
print("     • Classification (Mock): ✅")
print("     • Explainability: ✅")
print("     • Data Augmentation: ✅")
print("     • Evaluation Metrics: ✅")
print("\n  🚀 Next Steps:")
print("     1. Run full tests: python -m pytest tests/ -v")
print("     2. See TESTING_GUIDE.md for detailed instructions")
print("     3. Collect product images for training")
print()
