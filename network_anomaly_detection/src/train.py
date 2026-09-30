"""
Training script for all anomaly detection models
Generates synthetic data, trains Isolation Forest, One-Class SVM, and Autoencoder models,
and saves the trained models to the models/ directory.
"""

import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent))

from data_preprocessing import generate_sample_data
from baseline_models import BaselineAnomalyDetector
from autoencoder_model import AutoencoderAnomalyDetector


def main():
    print("=" * 60)
    print("Network Anomaly Detection Model Training Pipeline")
    print("=" * 60)

    # 1. Prepare Data
    print("\n[Step 1/5] Preparing data...")
    X_train, X_test, y_train, y_test = generate_sample_data(
        n_samples=10000,
        n_features=20,
        contamination=0.1
    )

    # 2. Train Isolation Forest
    print("\n[Step 2/5] Training Isolation Forest...")
    detector = BaselineAnomalyDetector()
    detector.train_isolation_forest(X_train, contamination=0.1)

    # 3. Train One-Class SVM
    print("\n[Step 3/5] Training One-Class SVM...")
    detector.train_one_class_svm(X_train, nu=0.1)

    # 4. Train Autoencoder
    print("\n[Step 4/5] Training Autoencoder...")
    ae_detector = AutoencoderAnomalyDetector(input_dim=X_train.shape[1])
    ae_detector.build_model(
        layers=[32, 16, 8, 16, 32],
        dropout_rate=0.1,
        learning_rate=0.001
    )
    # Train for a small number of epochs for fast demonstration
    history = ae_detector.train(
        X_train,
        validation_split=0.2,
        epochs=30,
        batch_size=128,
        patience=5,
        model_dir=str(Path(__file__).parent.parent / 'models')
    )

    # 5. Evaluate and Compare Models
    print("\n[Step 5/5] Evaluating and saving models...")
    os.makedirs(str(Path(__file__).parent.parent / 'models'), exist_ok=True)

    # Save baseline models
    detector.save_model('isolation_forest', str(Path(__file__).parent.parent / 'models' / 'isolation_forest.pkl'))
    detector.save_model('one_class_svm', str(Path(__file__).parent.parent / 'models' / 'one_class_svm.pkl'))

    # Save autoencoder
    ae_detector.save_model(str(Path(__file__).parent.parent / 'models' / 'autoencoder_best.keras'))

    # Run evaluations
    if_results = detector.evaluate('isolation_forest', X_test, y_test)
    svm_results = detector.evaluate('one_class_svm', X_test, y_test)
    ae_results = ae_detector.evaluate(X_test, y_test)

    # Compare
    all_results = pd.DataFrame([
        {
            'Model': 'Isolation Forest',
            'Precision': if_results['precision'],
            'Recall': if_results['recall'],
            'F1-Score': if_results['f1_score'],
            'ROC-AUC': if_results['roc_auc']
        },
        {
            'Model': 'One-Class SVM',
            'Precision': svm_results['precision'],
            'Recall': svm_results['recall'],
            'F1-Score': svm_results['f1_score'],
            'ROC-AUC': svm_results['roc_auc']
        },
        {
            'Model': 'Autoencoder',
            'Precision': ae_results['precision'],
            'Recall': ae_results['recall'],
            'F1-Score': ae_results['f1_score'],
            'ROC-AUC': ae_results['roc_auc']
        }
    ])

    print("\n" + "=" * 70)
    print("Final Model Comparison")
    print("=" * 70)
    print(all_results.to_string(index=False))
    print("\n[OK] Training and evaluation complete! All models saved.")


if __name__ == "__main__":
    main()
