
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Literal
import pandas as pd
import joblib
from pathlib import Path

# Create FastAPI application
app = FastAPI(
    title="Predictive Maintenance API",
    description="Machine Failure Prediction System",
    version="1.0"
)

# Load trained ML model
MODEL_PATH = Path(__file__).resolve().parent / "predictive_maintenance_model.pkl"
model = joblib.load(MODEL_PATH)


# Input data format with validation
class MachineData(BaseModel):
    Type: Literal["L", "M", "H"]
    air_temperature: float = Field(ge=250, le=350)
    process_temperature: float = Field(ge=250, le=400)
    rotational_speed: float = Field(ge=0, le=5000)
    torque: float = Field(ge=0, le=100)
    tool_wear: float = Field(ge=0, le=300)

# Home route
@app.get("/")
def home():
    return {
        "message": "Predictive Maintenance API is running!"
    }


# Prediction route
@app.post("/predict")
def predict(data: MachineData):

    input_data = pd.DataFrame([{
        "Type": data.Type,
        "Air temperature [K]": data.air_temperature,
        "Process temperature [K]": data.process_temperature,
        "Rotational speed [rpm]": data.rotational_speed,
        "Torque [Nm]": data.torque,
        "Tool wear [min]": data.tool_wear
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    result = "Machine Failure" if prediction == 1 else "No Machine Failure"

    return {
        "prediction": result,
        "failure_probability": round(float(probability) * 100, 2)
    }
