"""
Optional script to save generated data as CSV files
Run this if you want to see the training/testing data as CSV files in VS Code
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data_preprocessing import generate_sample_data
import pandas as pd
import numpy as np

print("=" * 60)
print("Generating and Saving Sample Network Traffic Data")
print("=" * 60)

# Generate data
print("\nGenerating synthetic data...")
X_train, X_test, y_train, y_test = generate_sample_data(
    n_samples=10000,
    n_features=20,
    contamination=0.1
)

# Create DataFrames
print("Creating DataFrames...")

# Training data (normal traffic only)
feature_names = [f'feature_{i}' for i in range(X_train.shape[1])]
df_train = pd.DataFrame(X_train, columns=feature_names)
df_train['label'] = y_train

# Test data (mixed normal + attacks)
df_test = pd.DataFrame(X_test, columns=feature_names)
df_test['label'] = y_test

# Save to CSV
print("\nSaving to CSV files...")
df_train.to_csv('data/train_data.csv', index=False)
df_test.to_csv('data/test_data.csv', index=False)

print(f"\n[OK] Files saved successfully!")
print(f"  - data/train_data.csv: {len(df_train)} rows (normal traffic only)")
print(f"  - data/test_data.csv:  {len(df_test)} rows ({(df_test['label']==0).sum()} normal, {(df_test['label']==1).sum()} attacks)")

print("\nYou can now see these files in VS Code!")
print("\nData Preview:")
print("\nTraining Data (first 5 rows):")
print(df_train.head())
print("\nTest Data (first 5 rows):")
print(df_test.head())

print("\n" + "=" * 60)
print("Data Statistics")
print("=" * 60)
print(f"\nTraining set: {df_train.shape}")
print(f"  - Features: {df_train.shape[1] - 1}")
print(f"  - Samples: {df_train.shape[0]}")
print(f"  - All Normal: {(df_train['label']==0).sum()} samples")

print(f"\nTest set: {df_test.shape}")
print(f"  - Features: {df_test.shape[1] - 1}")
print(f"  - Samples: {df_test.shape[0]}")
print(f"  - Normal: {(df_test['label']==0).sum()} ({(df_test['label']==0).sum()/len(df_test)*100:.1f}%)")
print(f"  - Attacks: {(df_test['label']==1).sum()} ({(df_test['label']==1).sum()/len(df_test)*100:.1f}%)")
