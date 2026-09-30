"""
Baseline anomaly detection models:
- Isolation Forest
- One-Class SVM
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    roc_curve,
    precision_recall_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import time


class BaselineAnomalyDetector:
    """Baseline anomaly detection using Isolation Forest and One-Class SVM"""

    def __init__(self):
        self.models = {}
        self.results = {}

    def train_isolation_forest(self, X_train, contamination=0.1, random_state=42):
        """
        Train Isolation Forest model

        Args:
            X_train: Training data (normal traffic only)
            contamination: Expected proportion of outliers
            random_state: Random seed

        Returns:
            Trained model
        """
        print("\n" + "="*60)
        print("Training Isolation Forest")
        print("="*60)

        start_time = time.time()

        model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_estimators=100,
            max_samples='auto',
            n_jobs=-1,
            verbose=0
        )

        model.fit(X_train)
        training_time = time.time() - start_time

        self.models['isolation_forest'] = model

        print(f"[OK] Training completed in {training_time:.2f} seconds")
        print(f"  - Number of estimators: 100")
        print(f"  - Contamination: {contamination}")

        return model

    def train_one_class_svm(self, X_train, nu=0.1, kernel='rbf', gamma='scale'):
        """
        Train One-Class SVM model

        Args:
            X_train: Training data (normal traffic only)
            nu: Upper bound on fraction of training errors
            kernel: Kernel type
            gamma: Kernel coefficient

        Returns:
            Trained model
        """
        print("\n" + "="*60)
        print("Training One-Class SVM")
        print("="*60)

        start_time = time.time()

        # Limit training samples for SVM (computational efficiency)
        if len(X_train) > 10000:
            print(f"  ⚠ Large dataset detected ({len(X_train)} samples)")
            print(f"  → Using 10,000 samples for SVM training (computational efficiency)")
            indices = np.random.choice(len(X_train), 10000, replace=False)
            X_train_sample = X_train[indices]
        else:
            X_train_sample = X_train

        model = OneClassSVM(
            nu=nu,
            kernel=kernel,
            gamma=gamma
        )

        model.fit(X_train_sample)
        training_time = time.time() - start_time

        self.models['one_class_svm'] = model

        print(f"[OK] Training completed in {training_time:.2f} seconds")
        print(f"  - Kernel: {kernel}")
        print(f"  - Nu: {nu}")
        print(f"  - Training samples: {len(X_train_sample)}")

        return model

    def predict(self, model, X_test):
        """
        Make predictions

        Args:
            model: Trained model
            X_test: Test data

        Returns:
            Binary predictions (0=normal, 1=anomaly)
        """
        # Model returns: 1 for inliers, -1 for outliers
        predictions = model.predict(X_test)

        # Convert to binary: 0=normal, 1=anomaly
        y_pred = (predictions == -1).astype(int)

        return y_pred

    def predict_scores(self, model_name, X_test):
        """
        Get anomaly scores

        Args:
            model_name: Name of the model
            X_test: Test data

        Returns:
            Anomaly scores
        """
        model = self.models[model_name]

        if model_name == 'isolation_forest':
            # Negative of decision_function gives anomaly score
            scores = -model.decision_function(X_test)
        elif model_name == 'one_class_svm':
            # Negative of decision_function gives anomaly score
            scores = -model.decision_function(X_test)
        else:
            raise ValueError(f"Unknown model: {model_name}")

        return scores

    def evaluate(self, model_name, X_test, y_test):
        """
        Evaluate model performance

        Args:
            model_name: Name of the model
            X_test: Test features
            y_test: True labels (0=normal, 1=attack)

        Returns:
            Dictionary with evaluation metrics
        """
        print(f"\n{'='*60}")
        print(f"Evaluating {model_name.replace('_', ' ').title()}")
        print("="*60)

        model = self.models[model_name]

        # Predictions
        y_pred = self.predict(model, X_test)

        # Anomaly scores
        scores = self.predict_scores(model_name, X_test)

        # Metrics
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        try:
            roc_auc = roc_auc_score(y_test, scores)
        except:
            roc_auc = 0.0

        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)

        results = {
            'model_name': model_name,
            'predictions': y_pred,
            'scores': scores,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm
        }

        self.results[model_name] = results

        # Print results
        print(f"\nMetrics:")
        print(f"  • Precision: {precision:.4f}")
        print(f"  • Recall:    {recall:.4f}")
        print(f"  • F1-Score:  {f1:.4f}")
        print(f"  • ROC-AUC:   {roc_auc:.4f}")

        print(f"\nConfusion Matrix:")
        print(f"  TN: {cm[0, 0]:<6} FP: {cm[0, 1]}")
        print(f"  FN: {cm[1, 0]:<6} TP: {cm[1, 1]}")

        # Detection rate and false positive rate
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

    def plot_confusion_matrix(self, model_name, save_path=None):
        """Plot confusion matrix"""
        if model_name not in self.results:
            print(f"No results for {model_name}")
            return

        cm = self.results[model_name]['confusion_matrix']

        plt.figure(figsize=(8, 6))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            cmap='Blues',
            xticklabels=['Normal', 'Attack'],
            yticklabels=['Normal', 'Attack'],
            cbar_kws={'label': 'Count'}
        )
        plt.title(f'Confusion Matrix - {model_name.replace("_", " ").title()}')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"[OK] Confusion matrix saved to {save_path}")

        plt.show()

    def plot_roc_curve(self, model_names=None, save_path=None):
        """Plot ROC curves for models"""
        if model_names is None:
            model_names = list(self.results.keys())

        plt.figure(figsize=(10, 8))

        for model_name in model_names:
            if model_name not in self.results:
                continue

            results = self.results[model_name]
            y_test = results.get('y_test')
            scores = results['scores']

            # Get ROC curve data from stored results or compute
            if y_test is not None:
                fpr, tpr, _ = roc_curve(y_test, scores)
                roc_auc = results['roc_auc']

                plt.plot(
                    fpr, tpr,
                    label=f"{model_name.replace('_', ' ').title()} (AUC = {roc_auc:.3f})",
                    linewidth=2
                )

        plt.plot([0, 1], [0, 1], 'k--', linewidth=1, label='Random')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate', fontsize=12)
        plt.ylabel('True Positive Rate', fontsize=12)
        plt.title('ROC Curves - Anomaly Detection Models', fontsize=14)
        plt.legend(loc='lower right', fontsize=10)
        plt.grid(alpha=0.3)
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"[OK] ROC curve saved to {save_path}")

        plt.show()

    def compare_models(self):
        """Compare all trained models"""
        if not self.results:
            print("No models evaluated yet")
            return

        print("\n" + "="*60)
        print("Model Comparison")
        print("="*60)

        comparison_data = []
        for model_name, results in self.results.items():
            comparison_data.append({
                'Model': model_name.replace('_', ' ').title(),
                'Precision': results['precision'],
                'Recall': results['recall'],
                'F1-Score': results['f1_score'],
                'ROC-AUC': results['roc_auc']
            })

        df_comparison = pd.DataFrame(comparison_data)
        print("\n", df_comparison.to_string(index=False))

        return df_comparison

    def save_model(self, model_name, filepath):
        """Save trained model"""
        if model_name not in self.models:
            print(f"Model {model_name} not found")
            return

        with open(filepath, 'wb') as f:
            pickle.dump(self.models[model_name], f)

        print(f"[OK] Model saved to {filepath}")

    def load_model(self, model_name, filepath):
        """Load trained model"""
        with open(filepath, 'rb') as f:
            model = pickle.load(f)

        self.models[model_name] = model
        print(f"[OK] Model loaded from {filepath}")

        return model


if __name__ == "__main__":
    from data_preprocessing import generate_sample_data

    print("Baseline Anomaly Detection Models")
    print("="*60)

    # Generate sample data
    X_train, X_test, y_train, y_test = generate_sample_data(n_samples=5000)

    # Initialize detector
    detector = BaselineAnomalyDetector()

    # Train models
    detector.train_isolation_forest(X_train, contamination=0.1)
    detector.train_one_class_svm(X_train, nu=0.1)

    # Evaluate models
    detector.evaluate('isolation_forest', X_test, y_test)
    detector.evaluate('one_class_svm', X_test, y_test)

    # Compare models
    detector.compare_models()
