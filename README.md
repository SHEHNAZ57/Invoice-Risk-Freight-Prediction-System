# Invoice Risk & Freight Prediction System  
**Machine Learning System for Invoice Risk Detection & Freight Cost Estimation**

---

## 📌 Table of Contents
- Project Overview  
- Business Objectives  
- Data Sources  
- Exploratory Data Analysis  
- Models Used  
- Evaluation Metrics  
- Application  
- Project Structure  
- How to Run This Project  
- Author & Contact  

---

## 📌 Project Overview

This project implements an **end-to-end machine learning system** designed to support finance and procurement teams by:

1. Predicting expected freight cost for vendor invoices  
2. Identifying high-risk invoices that require manual review based on abnormal patterns  

The system combines **regression and classification models** to improve operational efficiency and reduce manual invoice validation efforts.

---

## 🎯 Business Objectives

### 1. Freight Cost Prediction (Regression)
Predict expected freight cost using invoice and operational features.

✔ Helps in cost estimation  
✔ Improves procurement planning  
✔ Supports vendor negotiation  

---

### 2. Invoice Risk Detection (Classification)
Identify invoices that should be flagged for manual approval.

✔ Reduces manual review workload  
✔ Detects anomalies early  
✔ Improves financial control and audit efficiency  

---

## 📂 Data Sources

Data is stored in a SQLite database (`inventory.db`) containing:

- `vendor_invoice` – invoice-level financial data  
- `purchases` – item-level purchase records  
- `purchase_prices` – reference pricing  
- `begin_inventory`, `end_inventory` – inventory snapshots  

Feature engineering is performed using SQL aggregation and preprocessing pipelines.

---

## 📊 Exploratory Data Analysis (EDA)

EDA focuses on business-driven insights such as:

- Relationship between invoice value and freight cost  
- Differences between normal and flagged invoices  
- Distribution of invoice quantities and costs  

Statistical testing (t-tests) is used to validate significant differences between groups.

---

## 🤖 Models Used

### Freight Cost Prediction (Regression)
- Linear Regression (baseline)  
- Decision Tree Regressor  
- Random Forest Regressor (final model)  

### Invoice Risk Detection (Classification)
- Logistic Regression (baseline)  
- Decision Tree Classifier  
- Random Forest Classifier (final model)  

Hyperparameter tuning is performed using GridSearchCV with F1-score optimization.

---

## 📈 Evaluation Metrics

### Freight Prediction
- MAE  
- RMSE  
- R² Score  

### Invoice Risk Detection
- Accuracy  
- Precision  
- Recall  
- F1-score  
- Feature importance analysis  

---

## 🖥 Application

A Streamlit-based web application demonstrates the full pipeline:

- Invoice input interface  
- Freight cost prediction in real time  
- Risk detection (Approved / Manual Review)  
- Instant prediction output  

---

## 📁 Project Structure

```bash
invoice-risk-detection-system/
│
├── data/
│   └── inventory.db
│
├── freight_cost_prediction/
│   ├── train.py
│   ├── data_preprocessing.py
│   └── model_evaluation.py
│
├── invoice_flagging/
│   ├── train.py
│   ├── data_preprocessing.py
│   └── model_evaluation.py
│
├── inference/
│   ├── predict_freight.py
│   └── predict_invoice_flag.py
│
├── models/
│   ├── predict_freight_model.pkl
│   ├── predict_flag_invoice.pkl
│   └── scaler.pkl
│
├── notebooks/
│   ├── freight_analysis.ipynb
│   └── invoice_flagging.ipynb
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run This Project

```bash
# 1. Clone the repository
git clone https://github.com/your-username/invoice-risk-detection-system.git

# 2. Move into project directory
cd invoice-risk-detection-system

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Train models if not already available
python freight_cost_prediction/train.py
python invoice_flagging/train.py

# 5. Run inference scripts
python inference/predict_freight.py
python inference/predict_invoice_flag.py

# 6. Launch Streamlit app
streamlit run app.py
```

---

## 👤 Author & Contact

- Author: Shainaz  
- Project: Invoice Risk & Freight Prediction System  
- Purpose: Machine Learning Internship / Portfolio Project  
- GitHub: https://github.com/SHEHNAZ57