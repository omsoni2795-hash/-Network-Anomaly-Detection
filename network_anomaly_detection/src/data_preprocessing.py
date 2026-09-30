"""
Data preprocessing for network anomaly detection
Handles CICIDS2017 and UNSW-NB15 datasets
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')


class NetworkDataPreprocessor:
    """Preprocessor for network traffic datasets"""

    def __init__(self, dataset_type='UNSW-NB15'):
        """
        Initialize preprocessor

        Args:
            dataset_type: 'UNSW-NB15' or 'CICIDS2017'
        """
        self.dataset_type = dataset_type
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None

    def load_data(self, filepath):
        """
        Load dataset from CSV file

        Args:
            filepath: Path to CSV file

        Returns:
            DataFrame with loaded data
        """
        print(f"Loading data from {filepath}...")
        df = pd.read_csv(filepath)
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        return df

    def clean_data(self, df):
        """
        Clean dataset: handle missing values, remove duplicates

        Args:
            df: Input DataFrame

        Returns:
            Cleaned DataFrame
        """
        print("\nCleaning data...")
        initial_shape = df.shape

        # Remove duplicates
        df = df.drop_duplicates()

        # Handle missing values
        # For numerical columns, fill with median
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        for col in numerical_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].median(), inplace=True)

        # For categorical columns, fill with mode
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            if df[col].isnull().any():
                df[col].fillna(df[col].mode()[0], inplace=True)

        # Remove infinite values
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)

        print(f"Shape after cleaning: {df.shape} (removed {initial_shape[0] - df.shape[0]} rows)")
        return df

    def encode_features(self, df, label_column='label'):
        """
        Encode categorical features

        Args:
            df: Input DataFrame
            label_column: Name of the label column

        Returns:
            DataFrame with encoded features
        """
        print("\nEncoding categorical features...")
        df_encoded = df.copy()

        # Identify categorical columns (excluding label)
        categorical_cols = df_encoded.select_dtypes(include=['object']).columns.tolist()
        if label_column in categorical_cols:
            categorical_cols.remove(label_column)

        # Encode categorical features
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            self.label_encoders[col] = le

        print(f"Encoded {len(categorical_cols)} categorical columns")
        return df_encoded

    def normalize_features(self, X_train, X_test=None):
        """
        Normalize numerical features using StandardScaler

        Args:
            X_train: Training features
            X_test: Test features (optional)

        Returns:
            Normalized features
        """
        print("\nNormalizing features...")
        X_train_scaled = self.scaler.fit_transform(X_train)

        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            return X_train_scaled, X_test_scaled

        return X_train_scaled

    def prepare_anomaly_data(self, df, label_column='label', normal_label='Normal'):
        """
        Prepare data for anomaly detection:
        - Training set: normal traffic only
        - Test set: normal + attack traffic

        Args:
            df: Input DataFrame
            label_column: Name of the label column
            normal_label: Label value representing normal traffic

        Returns:
            X_train, X_test, y_train, y_test
        """
        print("\nPreparing data for anomaly detection...")

        # Separate features and labels
        if label_column not in df.columns:
            # Try to find label column
            possible_labels = ['label', 'Label', 'attack_cat', 'Attack']
            for col in possible_labels:
                if col in df.columns:
                    label_column = col
                    break

        # Create binary labels: 0 = normal, 1 = attack
        if label_column in df.columns:
            y = df[label_column].copy()
            # Handle different label formats
            if y.dtype == 'object':
                y_binary = (y.str.lower() != normal_label.lower()).astype(int)
            else:
                y_binary = (y != 0).astype(int)
        else:
            print(f"Warning: Label column '{label_column}' not found. Using last column as label.")
            y = df.iloc[:, -1]
            y_binary = (y != 0).astype(int)
            label_column = df.columns[-1]

        X = df.drop(columns=[label_column])
        self.feature_columns = X.columns.tolist()

        print(f"Total samples: {len(X)}")
        print(f"Normal samples: {(y_binary == 0).sum()}")
        print(f"Attack samples: {(y_binary == 1).sum()}")

        # Split data: 70% train, 30% test
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_binary, test_size=0.3, random_state=42, stratify=y_binary
        )

        # Filter training set to normal traffic only
        X_train_normal = X_train[y_train == 0]
        y_train_normal = y_train[y_train == 0]

        print(f"\nTraining set (normal only): {len(X_train_normal)} samples")
        print(f"Test set: {len(X_test)} samples ({(y_test == 0).sum()} normal, {(y_test == 1).sum()} attacks)")

        return X_train_normal, X_test, y_train_normal, y_test

    def preprocess_pipeline(self, filepath, label_column='label', normal_label='Normal'):
        """
        Complete preprocessing pipeline

        Args:
            filepath: Path to dataset CSV
            label_column: Name of the label column
            normal_label: Label value representing normal traffic

        Returns:
            X_train_scaled, X_test_scaled, y_train, y_test
        """
        # Load data
        df = self.load_data(filepath)

        # Clean data
        df = self.clean_data(df)

        # Encode categorical features
        df = self.encode_features(df, label_column)

        # Prepare anomaly detection data
        X_train, X_test, y_train, y_test = self.prepare_anomaly_data(
            df, label_column, normal_label
        )

        # Normalize features
        X_train_scaled, X_test_scaled = self.normalize_features(X_train, X_test)

        print("\n[OK] Preprocessing complete!")
        print(f"Training features shape: {X_train_scaled.shape}")
        print(f"Test features shape: {X_test_scaled.shape}")

        return X_train_scaled, X_test_scaled, y_train, y_test


def generate_sample_data(n_samples=10000, n_features=20, contamination=0.1):
    """
    Generate synthetic network traffic data for testing

    Args:
        n_samples: Number of samples
        n_features: Number of features
        contamination: Proportion of outliers

    Returns:
        X_train, X_test, y_train, y_test
    """
    from sklearn.datasets import make_classification

    print("Generating synthetic network traffic data...")

    # Generate data
    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=15,
        n_redundant=5,
        n_clusters_per_class=2,
        weights=[1-contamination, contamination],
        flip_y=0.01,
        random_state=42
    )

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    # Filter training to normal only
    X_train_normal = X_train[y_train == 0]
    y_train_normal = y_train[y_train == 0]

    # Normalize
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train_normal)
    X_test_scaled = scaler.transform(X_test)

    print(f"Generated {len(X_train_scaled)} training samples (normal only)")
    print(f"Generated {len(X_test_scaled)} test samples ({(y_test == 0).sum()} normal, {(y_test == 1).sum()} attacks)")

    return X_train_scaled, X_test_scaled, y_train_normal, y_test


if __name__ == "__main__":
    # Example usage
    print("Network Data Preprocessor")
    print("=" * 50)

    # Generate sample data for demonstration
    X_train, X_test, y_train, y_test = generate_sample_data()

    print("\n[OK] Sample data generated successfully!")
