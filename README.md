# Network Anomaly Detection - ML-T2-002

## Project Overview
Detecting Previously Unseen Network Attacks using Machine Learning anomaly detection techniques.

## Goal
Train a model on normal network traffic only, then detect anomalies that represent unseen attacks.

## Dataset
- CICIDS2017 or UNSW-NB15 dataset (CSV format)
- Training: Normal traffic only
- Testing: Normal + attack traffic

## Project Structure
```
network_anomaly_detection/
├── data/                  # Dataset files
├── notebooks/             # Jupyter notebooks
├── models/                # Saved models
├── src/                   # Source code
│   ├── data_preprocessing.py
│   ├── baseline_models.py
│   └── autoencoder_model.py
├── streamlit_app/         # Dashboard
│   └── app.py
├── requirements.txt
└── README.md
```

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### 1. Data Preparation
Download UNSW-NB15 dataset and place CSV files in `data/` folder.

### 2. Run Jupyter Notebook
```bash
jupyter notebook notebooks/anomaly_detection.ipynb
```

### 3. Launch Streamlit Dashboard
```bash
cd streamlit_app
streamlit run app.py
```

## Models
1. **Isolation Forest** - Baseline anomaly detection
2. **One-Class SVM** - Baseline anomaly detection
3. **Autoencoder** - Advanced deep learning approach

## Metrics
- Precision, Recall, F1-score
- ROC-AUC
- Detection rate for unseen attacks
- False positive rate

## Deliverables
- Jupyter Notebook with code and results
- Streamlit app prototype
- Technical report

## Author
ML Training Project - T2-002
