
# Project Documentation

## 1. Problem Statement
Traditional maintenance methods may fail to identify machine problems before breakdowns occur. This project uses machine learning to predict possible machine failures from operating conditions.

## 2. Objective
To develop a machine learning-based predictive maintenance system that estimates the possibility of machine failure.

## 3. Input Features
- Machine Type
- Air Temperature
- Process Temperature
- Rotational Speed
- Torque
- Tool Wear

## 4. Selected Algorithm
Gradient Boosting Classifier was selected after comparing six machine learning algorithms and performing hyperparameter tuning.

## 5. Backend
FastAPI receives machine details, validates the input and returns the prediction and failure probability.

## 6. Frontend
Streamlit provides an interactive dashboard for entering machine details and viewing predictions.

## 7. Database
SQLite stores prediction history, including machine details, predicted status, probability and timestamp.

## 8. Model Evaluation
- Accuracy: 98.70%
- Precision: 87.50%
- Recall: 72.06%
- F1 Score: 79.03%
- ROC-AUC: 96.86%

## 9. Limitations
The model is trained on the AI4I 2020 dataset. Its predictions depend on the quality and characteristics of the training data. It is a decision-support prototype, not a guarantee that machine failures will be prevented.
