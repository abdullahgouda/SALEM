from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import joblib

# =========================================
# Load Model
# =========================================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(
    BASE_DIR / "severity_model.pkl"
)

# =========================================
# FastAPI App
# =========================================

app = FastAPI()

# =========================================
# Input Schema
# =========================================

class IncidentData(BaseModel):

    citizen_trust_score: float

    anomaly_score: float

    image_authenticity_score: float

    reports_nearby_1h: int

    historical_severity_avg: float

# =========================================
# Severity Prediction Endpoint
# =========================================

@app.post("/predict")

def predict(data: IncidentData):

    # =========================
    # Convert Input to DataFrame
    # =========================

    input_data = pd.DataFrame([{
        "citizen_trust_score": data.citizen_trust_score,
        "anomaly_score": data.anomaly_score,
        "image_authenticity_score": data.image_authenticity_score,
        "reports_nearby_1h": data.reports_nearby_1h,
        "historical_severity_avg": data.historical_severity_avg
    }])

    # =========================
    # Prediction
    # =========================

    prediction = model.predict(
        input_data
    )[0]

    probabilities = model.predict_proba(
        input_data
    )[0]

    confidence = probabilities.max()

    # =========================
    # Return Response
    # =========================

    return {
        "severity_prediction": str(prediction),
        "severity_score": round(float(confidence), 3),
        "severity_level": str(prediction)
    }