"""
Generate realistic network traffic data with proper column names
Based on common features from CICIDS2017 and UNSW-NB15 datasets
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.data_preprocessing import generate_sample_data
import pandas as pd
import numpy as np

print("=" * 60)
print("Generating Realistic Network Traffic Data")
print("=" * 60)

# Real network traffic feature names (based on CICIDS2017 and UNSW-NB15)
NETWORK_FEATURE_NAMES = [
    'flow_duration',           # Duration of network flow in microseconds
    'total_fwd_packets',       # Total packets in forward direction
    'total_bwd_packets',       # Total packets in backward direction
    'total_length_fwd_packets', # Total size of forward packets
    'total_length_bwd_packets', # Total size of backward packets
    'fwd_packet_length_max',   # Maximum length of forward packets
    'fwd_packet_length_min',   # Minimum length of forward packets
    'fwd_packet_length_mean',  # Mean length of forward packets
    'bwd_packet_length_max',   # Maximum length of backward packets
    'bwd_packet_length_min',   # Minimum length of backward packets
    'flow_bytes_per_sec',      # Flow byte rate (bytes/sec)
    'flow_packets_per_sec',    # Flow packet rate (packets/sec)
    'flow_iat_mean',           # Mean inter-arrival time between packets
    'flow_iat_std',            # Standard deviation of inter-arrival time
    'fwd_iat_total',           # Total inter-arrival time in forward direction
    'bwd_iat_total',           # Total inter-arrival time in backward direction
    'fwd_psh_flags',           # Number of PSH flags in forward direction
    'bwd_psh_flags',           # Number of PSH flags in backward direction
    'fwd_urg_flags',           # Number of URG flags in forward direction
    'packet_length_variance'   # Variance of packet lengths
]

# Generate synthetic data
print("\nGenerating synthetic network traffic data...")
X_train, X_test, y_train, y_test = generate_sample_data(
    n_samples=10000,
    n_features=20,
    contamination=0.1
)

# Create DataFrames with realistic column names
print("Creating DataFrames with realistic network feature names...")

df_train = pd.DataFrame(X_train, columns=NETWORK_FEATURE_NAMES)
df_train['attack_type'] = 'Normal'  # More descriptive label

df_test = pd.DataFrame(X_test, columns=NETWORK_FEATURE_NAMES)
df_test['attack_type'] = df_test.apply(lambda row: 'Normal' if y_test[row.name] == 0 else 'Attack', axis=1)

# Add binary label for compatibility
df_train['label'] = 0
df_test['label'] = y_test

# Save to CSV
print("\nSaving to CSV files...")
df_train.to_csv('data/train_data.csv', index=False)
df_test.to_csv('data/test_data.csv', index=False)

# Also create a detailed version with attack categories
print("Creating detailed version with attack categories...")
attack_categories = ['Normal', 'DoS', 'DDoS', 'Port Scan', 'Brute Force', 'Web Attack']
df_test_detailed = df_test.copy()
df_test_detailed['attack_category'] = df_test_detailed['attack_type'].apply(
    lambda x: 'Normal' if x == 'Normal' else np.random.choice(['DoS', 'DDoS', 'Port Scan', 'Brute Force', 'Web Attack'])
)
df_test_detailed.to_csv('data/test_data_detailed.csv', index=False)

print(f"\n[OK] Files saved successfully!")
print(f"  - data/train_data.csv: {len(df_train)} rows (normal traffic only)")
print(f"  - data/test_data.csv: {len(df_test)} rows ({(df_test['label']==0).sum()} normal, {(df_test['label']==1).sum()} attacks)")
print(f"  - data/test_data_detailed.csv: {len(df_test_detailed)} rows (with attack categories)")

print("\n" + "=" * 60)
print("Data Preview with Realistic Column Names")
print("=" * 60)
print("\nTraining Data (first 5 rows):")
print(df_train.head())

print("\nTest Data (first 5 rows):")
print(df_test.head())

print("\n" + "=" * 60)
print("Network Feature Descriptions")
print("=" * 60)
print("""
Flow-based Features:
  • flow_duration: How long the connection lasted
  • flow_bytes_per_sec: Data transfer rate
  • flow_packets_per_sec: Packet transmission rate

Packet Statistics:
  • total_fwd_packets: Packets sent from source
  • total_bwd_packets: Packets received back
  • packet_length_variance: Variation in packet sizes

Timing Features:
  • flow_iat_mean: Average time between packets
  • flow_iat_std: Consistency of packet timing

TCP Flags:
  • fwd_psh_flags: Push flags (force data delivery)
  • fwd_urg_flags: Urgent flags (priority data)

Size Metrics:
  • fwd_packet_length_mean: Average packet size
  • total_length_fwd_packets: Total data sent
""")

print("\n" + "=" * 60)
print("Data Statistics")
print("=" * 60)
print(f"\nTraining set: {df_train.shape}")
print(f"  - Network Features: {len(NETWORK_FEATURE_NAMES)}")
print(f"  - Samples: {df_train.shape[0]}")
print(f"  - All Normal Traffic")

print(f"\nTest set: {df_test.shape}")
print(f"  - Network Features: {len(NETWORK_FEATURE_NAMES)}")
print(f"  - Samples: {df_test.shape[0]}")
print(f"  - Normal: {(df_test['label']==0).sum()} ({(df_test['label']==0).sum()/len(df_test)*100:.1f}%)")
print(f"  - Attacks: {(df_test['label']==1).sum()} ({(df_test['label']==1).sum()/len(df_test)*100:.1f}%)")

print(f"\nTest set (detailed) attack categories:")
print(df_test_detailed['attack_category'].value_counts())

print("\n" + "=" * 60)
print("✓ Complete! Open the CSV files in VS Code to see realistic network features!")
print("=" * 60)
