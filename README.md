
# Machine Learning-Based Predictive Maintenance and Machine Failure Prediction System

## Project Overview
This project uses Machine Learning to predict potential machine failures based on machine operating conditions. It helps identify possible failures in advance and supports predictive maintenance.

## Dataset
- AI4I 2020 Predictive Maintenance Dataset
- Source: UCI Machine Learning Repository
- 10,000 records

## Machine Learning Algorithms
The following algorithms were compared:
1. Logistic Regression
2. Decision Tree
3. Random Forest
4. Support Vector Machine (SVM)
5. K-Nearest Neighbors (KNN)
6. Gradient Boosting Classifier

**Final selected model:** Gradient Boosting Classifier

## Model Performance
- Accuracy: 98.70%
- Precision: 87.50%
- Recall: 72.06%
- F1 Score: 79.03%
- ROC-AUC: 96.86%

## Technologies Used
- Python
- Scikit-learn
- Pandas
- FastAPI
- Streamlit
- SQLite
- Joblib

## Project Structure
- `Backend/` – FastAPI backend and trained ML model
- `frontend.py` – Streamlit dashboard
- `requirements.txt` – Required Python libraries
- `Notebooks/` – Model development notebook
- `Reports/` – Project report and poster
- `Documentation/` – Supporting documentation

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the backend
```bash
python -m uvicorn Backend.main:app --reload
```

### 3. Start the frontend in another terminal
```bash
streamlit run frontend.py
```

Open the dashboard at:
`http://localhost:8501`

## Note
This is a local machine learning prototype. Predictions are intended to support maintenance decisions and are not a guarantee against machine failure.
