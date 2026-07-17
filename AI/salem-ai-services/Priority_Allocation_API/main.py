# =========================================================
# Priority & Resource Allocation API
# SALEM Graduation Project
# =========================================================

from fastapi import FastAPI
from pydantic import BaseModel

import pandas as pd
import joblib

# =========================================================
# Load Trained Model
# =========================================================
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

model = joblib.load(
    BASE_DIR / "priority_allocation_model.pkl"
)

label_encoders = joblib.load(
    BASE_DIR / "priority_label_encoders.pkl"
)

features = joblib.load(
    BASE_DIR / "priority_features.pkl"
)

# =========================================================
# Initialize FastAPI
# =========================================================

app = FastAPI(
    title="Priority & Resource Allocation API",
    version="1.0"
)

# =========================================================
# Request Schema
# =========================================================

class PriorityRequest(BaseModel):

    severity_label: str
    severity_score: float
    area_load: float
    available_teams: int
    team_skill_match: float
    historical_team_performance: float
    citizen_trust_score: float
    reports_nearby_1h: int

# =========================================================
# Root Endpoint
# =========================================================

@app.get("/")

def home():

    return {
        "message":
        "Priority & Resource Allocation API Running"
    }

# =========================================================
# Prediction Endpoint
# =========================================================

@app.post("/predict")

def predict_priority(data: PriorityRequest):

    # =====================================================
    # Encode Severity Label
    # =====================================================

    severity_encoded = label_encoders[
        "severity_label"
    ].transform([data.severity_label])[0]

    # =====================================================
    # Build Input DataFrame
    # =====================================================

    input_df = pd.DataFrame([{

        "severity_label":
            severity_encoded,

        "severity_score":
            data.severity_score,

        "area_load":
            data.area_load,

        "available_teams":
            data.available_teams,

        "team_skill_match":
            data.team_skill_match,

        "historical_team_performance":
            data.historical_team_performance,

        "citizen_trust_score":
            data.citizen_trust_score,

        "reports_nearby_1h":
            data.reports_nearby_1h
    }])

    # =====================================================
    # Reorder Features
    # =====================================================

    input_df = input_df[features]

    # =====================================================
    # Predict
    # =====================================================

    prediction = model.predict(input_df)[0]

    confidence = model.predict_proba(
        input_df
    ).max()

    # =====================================================
    # Decode Prediction
    # =====================================================

    decoded_prediction = label_encoders[
        "priority_level"
    ].inverse_transform([prediction])[0]

    # =====================================================
    # Resource Allocation Logic
    # =====================================================

    if decoded_prediction == "P1":

        recommended_resources = 5

        dispatch_type = "Critical Response"

    elif decoded_prediction == "P2":

        recommended_resources = 3

        dispatch_type = "Standard Response"

    else:

        recommended_resources = 1

        dispatch_type = "Low Priority Response"

    # =====================================================
    # Return Response
    # =====================================================

    return {

        "priority_prediction":
            decoded_prediction,

        "confidence_score":
            round(float(confidence), 4),

        "dispatch_type":
            dispatch_type,

        "recommended_resources":
            recommended_resources
    }