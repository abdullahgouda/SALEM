from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import joblib

# =========================
# Load Model
# =========================

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(
    BASE_DIR / "trust_model.pkl"
)
# =========================
# FastAPI App
# =========================

app = FastAPI()

# =========================
# Input Schema
# =========================

class CitizenData(BaseModel):

    valid_ratio: float
    duplicate_rate: float
    fake_image_ratio: float
    reports_last_30_days: int
    avg_severity_reported: float

# =========================
# Trust Prediction Endpoint
# =========================

@app.post("/predict")

def predict(data: CitizenData):

    input_data = pd.DataFrame([{
        "valid_ratio": data.valid_ratio,
        "duplicate_rate": data.duplicate_rate,
        "fake_image_ratio": data.fake_image_ratio,
        "reports_last_30_days": data.reports_last_30_days,
        "avg_severity_reported": data.avg_severity_reported
    }])

    prediction = model.predict(
        input_data
    )[0]

    probability = model.predict_proba(
        input_data
    )[0][1]

    if probability >= 0.8:
        trust_level = "High"

    elif probability >= 0.5:
        trust_level = "Medium"

    else:
        trust_level = "Low"

    return {
        "trust_prediction": int(prediction),
        "trust_score": round(float(probability), 3),
        "trust_level": trust_level
    }