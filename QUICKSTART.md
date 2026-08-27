# Quick Start Guide
## Network Anomaly Detection - ML-T2-002

### 🚀 Getting Started in 3 Steps

---

## Step 1: Install Dependencies

```bash
cd network_anomaly_detection
pip install -r requirements.txt
```

**Required Libraries:**
- pandas, numpy, scikit-learn
- tensorflow (for Autoencoder)
- matplotlib, seaborn, plotly
- streamlit (for dashboard)

---

## Step 2: Train Models

### Option A: Run Training Script (Fastest)
```bash
python src/train.py
```

This will:
- Generate synthetic training data
- Train all three models (Isolation Forest, One-Class SVM, Autoencoder)
- Save trained models to `models/` directory
- Display performance comparison

**Expected Output:**
```
[Step 1/5] Preparing data...
[Step 2/5] Training Isolation Forest...
[Step 3/5] Training One-Class SVM...
[Step 4/5] Training Autoencoder...
[Step 5/5] Evaluating and saving models...

Final Model Comparison
======================================================================
              Model  Precision    Recall  F1-Score   ROC-AUC
   Isolation Forest      0.XXX     0.XXX     0.XXX     0.XXX
   One-Class SVM         0.XXX     0.XXX     0.XXX     0.XXX
   Autoencoder           0.XXX     0.XXX     0.XXX     0.XXX
```

### Option B: Run Jupyter Notebook (Interactive)
```bash
jupyter notebook notebooks/anomaly_detection.ipynb
```

Execute all cells to:
- Explore data preprocessing
- Train models step-by-step
- Generate visualizations
- See detailed analysis

---

## Step 3: Launch Dashboard

```bash
cd streamlit_app
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Dashboard Features:
1. **Model Selection** - Choose between 3 trained models
2. **Data Generation** - Create synthetic test data
3. **Upload CSV** - Test on your own network traffic data
4. **Real-time Detection** - Classify traffic as normal or anomaly
5. **Visualizations** - View confusion matrices, ROC curves, and score distributions

---

## 📁 Project Structure

```
network_anomaly_detection/
│
├── src/
│   ├── data_preprocessing.py      # Data loading and preprocessing
│   ├── baseline_models.py         # Isolation Forest & One-Class SVM
│   ├── autoencoder_model.py       # Deep Learning Autoencoder
│   └── train.py                   # Complete training pipeline
│
├── notebooks/
│   └── anomaly_detection.ipynb    # Interactive analysis notebook
│
├── streamlit_app/
│   └── app.py                     # Web dashboard
│
├── models/                         # Trained models (generated after training)
│   ├── isolation_forest.pkl
│   ├── one_class_svm.pkl
│   ├── autoencoder_best.keras
│   └── autoencoder_best_threshold.txt
│
├── data/                          # Place your datasets here
│
├── requirements.txt               # Python dependencies
├── README.md                      # Project overview
├── TECHNICAL_REPORT.md           # Detailed technical report
└── QUICKSTART.md                 # This file
```

---

## 🔧 Using Your Own Dataset

### CSV Format Requirements:
- **Last column**: Label (0 = normal, 1 = attack)
- **Other columns**: Numerical network traffic features
- **Example**:
```csv
feature_1,feature_2,feature_3,...,label
0.5,1.2,0.3,...,0
0.1,0.8,0.5,...,0
5.2,9.1,8.3,...,1
```

### Loading Custom Data:

**In Python:**
```python
from data_preprocessing import NetworkDataPreprocessor

preprocessor = NetworkDataPreprocessor(dataset_type='UNSW-NB15')
X_train, X_test, y_train, y_test = preprocessor.preprocess_pipeline(
    filepath='data/your_dataset.csv',
    label_column='label',
    normal_label='Normal'  # or 0, depending on your data
)
```

**In Dashboard:**
1. Click "Upload CSV File"
2. Select your CSV file
3. Click "Load Data"
4. Click "Run Detection"

---

## 🎯 Common Use Cases

### Use Case 1: Quick Demo
```bash
# Install dependencies
pip install -r requirements.txt

# Train models (2-3 minutes)
python src/train.py

# Launch dashboard
cd streamlit_app && streamlit run app.py
```

### Use Case 2: Research & Development
```bash
# Launch Jupyter notebook
jupyter notebook notebooks/anomaly_detection.ipynb

# Experiment with:
# - Different hyperparameters
# - Model architectures
# - Evaluation metrics
# - Visualization techniques
```

### Use Case 3: Production Deployment
```python
# Load trained model
import pickle
with open('models/isolation_forest.pkl', 'rb') as f:
    model = pickle.load(f)

# Predict on new data
predictions = model.predict(new_network_traffic)
# -1 = anomaly, 1 = normal

# Convert to binary labels
anomalies = (predictions == -1).astype(int)
```

---

## 🐛 Troubleshooting

### Issue: TensorFlow not installed
**Solution:**
```bash
pip install tensorflow==2.13.0
```

### Issue: Module not found errors
**Solution:**
```bash
# Ensure you're in the project directory
cd network_anomaly_detection

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Streamlit app won't load models
**Solution:**
```bash
# Train models first
python src/train.py

# Then launch dashboard
cd streamlit_app && streamlit run app.py
```

### Issue: Jupyter kernel crashes during Autoencoder training
**Solution:**
- Reduce batch size: `batch_size=64` instead of 128
- Reduce epochs: `epochs=10` instead of 30
- Use CPU instead of GPU if memory limited

---

## 📊 Performance Benchmarks

### Training Time (on typical laptop):
- **Isolation Forest**: 1-2 seconds
- **One-Class SVM**: 5-10 seconds (limited to 10K samples)
- **Autoencoder**: 30-60 seconds (30 epochs)

### Inference Speed (per sample):
- **Isolation Forest**: <1ms
- **One-Class SVM**: ~2ms
- **Autoencoder**: ~1ms (with GPU), ~5ms (CPU)

### Memory Requirements:
- **Training**: 2-4 GB RAM
- **Inference**: <500 MB RAM
- **Models on disk**: ~5-10 MB total

---

## 🎓 Learning Resources

### Understanding the Models:

**Isolation Forest:**
- Based on random forests
- Isolates anomalies using path length
- Best for: High-dimensional data, real-time detection

**One-Class SVM:**
- Learns boundary around normal data
- Uses kernel methods (RBF)
- Best for: Small datasets, theoretical foundation

**Autoencoder:**
- Neural network learns to compress and reconstruct
- High reconstruction error = anomaly
- Best for: Complex patterns, highest accuracy

### Key Concepts:
1. **Unsupervised Learning**: No labeled attack data needed during training
2. **Anomaly Detection**: Identify deviations from normal behavior
3. **Reconstruction Error**: Measure how well model reconstructs input
4. **Threshold Tuning**: Balance between false positives and false negatives

---

## 💡 Tips for Best Results

1. **Data Quality**: Clean, preprocessed data improves performance
2. **Feature Selection**: Remove irrelevant or redundant features
3. **Threshold Tuning**: Adjust based on false positive tolerance
4. **Ensemble Methods**: Combine multiple models for robustness
5. **Continuous Learning**: Retrain periodically with new normal traffic

---

## 📞 Next Steps

1. ✅ **Install dependencies** → `pip install -r requirements.txt`
2. ✅ **Train models** → `python src/train.py`
3. ✅ **Explore notebook** → `jupyter notebook notebooks/anomaly_detection.ipynb`
4. ✅ **Launch dashboard** → `streamlit run streamlit_app/app.py`
5. ✅ **Test with real data** → Upload your own CSV files
6. ✅ **Read technical report** → See `TECHNICAL_REPORT.md` for details

---

## 🌟 Key Takeaways

- **3 Models Implemented**: Isolation Forest, One-Class SVM, Autoencoder
- **Unsupervised Approach**: Trained on normal traffic only
- **Interactive Dashboard**: Easy-to-use Streamlit web interface
- **Complete Pipeline**: Data preprocessing → Training → Evaluation → Deployment
- **Production Ready**: Can be integrated into real network monitoring systems

**Happy Detecting! 🛡️**
