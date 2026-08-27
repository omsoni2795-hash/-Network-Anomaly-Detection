"""
Test script for baseline models (no TensorFlow required)
Run this to verify Isolation Forest and One-Class SVM work correctly
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from data_preprocessing import generate_sample_data
from baseline_models import BaselineAnomalyDetector

print("=" * 60)
print("Testing Baseline Anomaly Detection Models")
print("=" * 60)

# Generate sample data
print("\n[1/4] Generating sample data...")
X_train, X_test, y_train, y_test = generate_sample_data(
    n_samples=5000,
    n_features=20,
    contamination=0.1
)

# Initialize detector
detector = BaselineAnomalyDetector()

# Train Isolation Forest
print("\n[2/4] Training Isolation Forest...")
detector.train_isolation_forest(X_train, contamination=0.1)

# Train One-Class SVM
print("\n[3/4] Training One-Class SVM...")
detector.train_one_class_svm(X_train, nu=0.1)

# Evaluate both models
print("\n[4/4] Evaluating models...")
if_results = detector.evaluate('isolation_forest', X_test, y_test)
svm_results = detector.evaluate('one_class_svm', X_test, y_test)

# Compare
print("\n" + "=" * 60)
print("Model Comparison Summary")
print("=" * 60)
comparison = detector.compare_models()
print("\n" + comparison.to_string(index=False))

# Save models
print("\n" + "=" * 60)
print("Saving Models")
print("=" * 60)
import os
os.makedirs('../models', exist_ok=True)
detector.save_model('isolation_forest', '../models/isolation_forest.pkl')
detector.save_model('one_class_svm', '../models/one_class_svm.pkl')

print("\n[OK] Test complete! Baseline models are working correctly.")
print("\nNext steps:")
print("1. Install TensorFlow: pip install tensorflow")
print("2. Run full training: python train.py")
print("3. Launch dashboard: cd ../streamlit_app && streamlit run app.py")
