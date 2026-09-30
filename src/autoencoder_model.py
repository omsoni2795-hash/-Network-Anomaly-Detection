"""
Autoencoder anomaly detection model using TensorFlow/Keras
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.models import load_model as tf_load_model
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)
import time
import os


class AutoencoderAnomalyDetector:
    """Autoencoder model for reconstructing normal network traffic and detecting anomalies"""

    def __init__(self, input_dim=None):
        """
        Initialize autoencoder

        Args:
            input_dim: Number of input features
        """
        self.input_dim = input_dim
        self.model = None
        self.threshold = None
        self.results = {}

    def build_model(self, layers=[32, 16, 8, 16, 32], dropout_rate=0.1, learning_rate=0.001):
        """
        Build the Autoencoder architecture

        Args:
            layers: List of node counts for hidden layers. The middle element represents the bottleneck.
                    Example: [32, 16, 8, 16, 32] (encodes to 8, decodes back to input)
            dropout_rate: Dropout rate for regularization
            learning_rate: Optimizer learning rate
        """
        if self.input_dim is None:
            raise ValueError("Input dimension must be specified to build the model")

        print(f"\nBuilding Autoencoder model with layers: {self.input_dim} -> {layers} -> {self.input_dim}")

        model = Sequential()

        # Input layer
        model.add(Input(shape=(self.input_dim,)))

        # Encoder
        bottleneck_idx = len(layers) // 2
        encoder_layers = layers[:bottleneck_idx + 1]
        for units in encoder_layers:
            model.add(Dense(units, activation='relu'))
            if dropout_rate > 0:
                model.add(Dropout(dropout_rate))

        # Decoder
        decoder_layers = layers[bottleneck_idx + 1:]
        for units in decoder_layers:
            model.add(Dense(units, activation='relu'))
            if dropout_rate > 0:
                model.add(Dropout(dropout_rate))

        # Output layer (reconstructs input)
        model.add(Dense(self.input_dim, activation='linear'))

        # Compile model
        optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
        model.compile(optimizer=optimizer, loss='mse')

        self.model = model
        print("[OK] Architecture defined successfully:")
        self.model.summary()

        return model

    def train(self, X_train, validation_split=0.1, epochs=50, batch_size=256, verbose=1, patience=5, model_dir='models'):
        """
        Train the autoencoder on normal traffic only

        Args:
            X_train: Training features (normal traffic only)
            validation_split: Portion of data for validation
            epochs: Max training epochs
            batch_size: Batch size
            verbose: Keras verbosity level
            patience: Early stopping patience
            model_dir: Directory to save model checkpoint

        Returns:
            Training history
        """
        if self.model is None:
            self.input_dim = X_train.shape[1]
            self.build_model()

        print("\n" + "="*60)
        print("Training Autoencoder")
        print("="*60)

        # Callbacks
        os.makedirs(model_dir, exist_ok=True)
        checkpoint_path = os.path.join(model_dir, 'autoencoder_best.keras')

        callbacks = [
            EarlyStopping(
                monitor='val_loss',
                patience=patience,
                mode='min',
                restore_best_weights=True,
                verbose=1
            ),
            ModelCheckpoint(
                filepath=checkpoint_path,
                monitor='val_loss',
                save_best_only=True,
                mode='min',
                verbose=0
            )
        ]

        start_time = time.time()

        # For autoencoder, input and output are the same
        history = self.model.fit(
            X_train, X_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=validation_split,
            callbacks=callbacks,
            shuffle=True,
            verbose=verbose
        )

        training_time = time.time() - start_time
        print(f"[OK] Training completed in {training_time:.2f} seconds")

        # Determine anomaly threshold from training data
        self.determine_threshold(X_train)

        return history

    def calculate_reconstruction_error(self, X):
        """
        Calculate Mean Squared Error reconstruction error for each sample

        Args:
            X: Input features

        Returns:
            Array of reconstruction errors
        """
        # Predict reconstructions
        X_pred = self.model.predict(X, verbose=0)

        # Compute MSE per sample
        mse = np.mean(np.power(X - X_pred, 2), axis=1)

        return mse

    def determine_threshold(self, X_train_normal):
        """
        Set threshold for anomaly detection based on training reconstruction error.

        Args:
            X_train_normal: Training data (normal only)
        """
        print("\nCalculating anomaly threshold from training data...")
        errors = self.calculate_reconstruction_error(X_train_normal)

        # Standard heuristics
        mean_err = np.mean(errors)
        std_err = np.std(errors)

        # Try multiple options
        thresh_95 = np.percentile(errors, 95)
        thresh_99 = np.percentile(errors, 99)
        thresh_std_3 = mean_err + 3 * std_err

        # Choose the 97.5th percentile as default for balanced detection
        self.threshold = np.percentile(errors, 97.5)

        print(f"  - Training Reconstruction Error Stats:")
        print(f"    • Mean: {mean_err:.6f}")
        print(f"    • Std:  {std_err:.6f}")
        print(f"  - Candidate Thresholds:")
        print(f"    • 95th Percentile:      {thresh_95:.6f}")
        print(f"    • 99th Percentile:      {thresh_99:.6f}")
        print(f"    • Mean + 3*Std:         {thresh_std_3:.6f}")
        print(f"  → Threshold chosen (97.5th percentile): {self.threshold:.6f}")

    def predict(self, X_test):
        """
        Classify samples as normal (0) or anomaly (1) based on threshold

        Args:
            X_test: Test features

        Returns:
            Binary predictions
        """
        if self.threshold is None:
            raise ValueError("Threshold has not been set. Call train or set_threshold first.")

        # Compute errors
        errors = self.calculate_reconstruction_error(X_test)

        # Classify: error > threshold is anomaly (1)
        y_pred = (errors > self.threshold).astype(int)

        return y_pred

    def evaluate(self, X_test, y_test):
        """
        Evaluate model performance on test set

        Args:
            X_test: Test features
            y_test: True labels (0=normal, 1=attack)

        Returns:
            Dictionary with metrics
        """
        print(f"\n{'='*60}")
        print("Evaluating Autoencoder")
        print("="*60)

        # Anomaly scores (MSE reconstruction errors)
        errors = self.calculate_reconstruction_error(X_test)

        # Binary predictions
        y_pred = (errors > self.threshold).astype(int)

        # Metrics
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        try:
            roc_auc = roc_auc_score(y_test, errors)
        except:
            roc_auc = 0.0

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        results = {
            'model_name': 'autoencoder',
            'predictions': y_pred,
            'scores': errors,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm,
            'threshold': self.threshold
        }

        self.results['autoencoder'] = results

        # Print results
        print(f"\nMetrics:")
        print(f"  • Chosen Threshold: {self.threshold:.6f}")
        print(f"  • Precision:        {precision:.4f}")
        print(f"  • Recall:           {recall:.4f}")
        print(f"  • F1-Score:         {f1:.4f}")
        print(f"  • ROC-AUC:          {roc_auc:.4f}")

        print(f"\nConfusion Matrix:")
        print(f"  TN: {cm[0, 0]:<6} FP: {cm[0, 1]}")
        print(f"  FN: {cm[1, 0]:<6} TP: {cm[1, 1]}")

        if cm[1, 0] + cm[1, 1] > 0:
            detection_rate = cm[1, 1] / (cm[1, 0] + cm[1, 1])
        else:
            detection_rate = 0.0

        if cm[0, 0] + cm[0, 1] > 0:
            false_positive_rate = cm[0, 1] / (cm[0, 0] + cm[0, 1])
        else:
            false_positive_rate = 0.0

        print(f"\n  • Detection Rate: {detection_rate:.4f} ({cm[1, 1]}/{cm[1, 0] + cm[1, 1]} attacks detected)")
        print(f"  • False Positive Rate: {false_positive_rate:.4f}")

        return results

    def plot_reconstruction_distribution(self, X_test, y_test, save_path=None):
        """Plot reconstruction error distribution for normal vs attack traffic"""
        errors = self.calculate_reconstruction_error(X_test)
        df_err = pd.DataFrame({'reconstruction_error': errors, 'label': y_test})
        df_err['class'] = df_err['label'].map({0: 'Normal', 1: 'Attack'})

        plt.figure(figsize=(12, 6))

        # Histogram KDE plots
        sns.kdeplot(
            data=df_err,
            x='reconstruction_error',
            hue='class',
            common_norm=False,
            fill=True,
            palette={'Normal': '#1f77b4', 'Attack': '#d62728'},
            alpha=0.5,
            linewidth=2
        )

        # Draw threshold line
        plt.axvline(
            self.threshold,
            color='black',
            linestyle='--',
            linewidth=2,
            label=f'Threshold ({self.threshold:.4f})'
        )

        plt.title('Reconstruction Error Distribution (Normal vs Attack)', fontsize=14)
        plt.xlabel('Mean Squared Error (MSE) Reconstruction Error', fontsize=12)
        plt.ylabel('Density', fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"[OK] Error distribution plot saved to {save_path}")

        plt.show()

    def save_model(self, filepath):
        """Save model and threshold"""
        if self.model is None:
            print("No model to save")
            return

        # Save model architecture & weights (keras format)
        self.model.save(filepath)

        # Save threshold
        threshold_file = filepath.replace('.keras', '_threshold.txt')
        with open(threshold_file, 'w') as f:
            f.write(str(self.threshold))

        print(f"[OK] Model saved to {filepath}")
        print(f"[OK] Threshold ({self.threshold:.6f}) saved to {threshold_file}")

    def load_model(self, filepath):
        """Load model and threshold"""
        self.model = tf_load_model(filepath)

        # Load threshold
        threshold_file = filepath.replace('.keras', '_threshold.txt')
        if os.path.exists(threshold_file):
            with open(threshold_file, 'r') as f:
                self.threshold = float(f.read().strip())
            print(f"[OK] Model loaded with threshold = {self.threshold:.6f}")
        else:
            print(f"⚠ Model loaded but threshold file {threshold_file} not found. Must set manually.")

        # Update input dim
        self.input_dim = self.model.input_shape[1]

        return self.model


if __name__ == "__main__":
    from data_preprocessing import generate_sample_data

    print("Autoencoder Anomaly Detection")
    print("="*60)

    # Generate sample data
    X_train, X_test, y_train, y_test = generate_sample_data(n_samples=5000)

    # Initialize and train
    detector = AutoencoderAnomalyDetector(input_dim=X_train.shape[1])
    detector.train(X_train, epochs=10, batch_size=64, validation_split=0.2)

    # Evaluate
    detector.evaluate(X_test, y_test)
