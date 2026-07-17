# SALEM AI Services API Documentation

## 1. Duplicate Incident Detection API

Port: 8001

Endpoint:
POST /check-duplicate

Input:

```json
{
  "description": "يوجد حفرة كبيرة في شارع عباس العقاد"
}
```

Output:

```json
{
  "duplicate": true,
  "similarity": 0.93,
  "matched_report": "يوجد حفرة في شارع عباس العقاد",
  "threshold": 0.85
}
```

---

## 2. Citizen Trust Score API

Port: 8002

Endpoint:
POST /predict

Input:

```json
{
  "valid_ratio": 0.9,
  "duplicate_rate": 0.1,
  "fake_image_ratio": 0.05,
  "reports_last_30_days": 5,
  "avg_severity_reported": 3.2
}
```

Output:

```json
{
  "trust_prediction": 1,
  "trust_score": 0.91,
  "trust_level": "High"
}
```

---

## 3. ETA Prediction API

Port: 8003

Endpoint:
POST /predict

Output:

```json
{
  "estimated_resolution_time": 7.5,
  "eta_category": "Fast Response"
}
```

---

## 4. Image Authenticity API

Port: 8004

Endpoint:
POST /predict

Input:
Image File

Output:

```json
{
  "prediction": "authentic",
  "confidence": 98.2
}
```

---

## 5. Incident Severity API

Port: 8005

Endpoint:
POST /predict

Output:

```json
{
  "severity_prediction": "High",
  "severity_score": 0.92,
  "severity_level": "High"
}
```

---

## 6. Priority Allocation API

Port: 8006

Endpoint:
POST /predict

Output:

```json
{
  "priority_prediction": "P1",
  "confidence_score": 0.94,
  "dispatch_type": "Critical Response",
  "recommended_resources": 5
}
```

---

## 7. Road Damage Classification API

Port: 8007

Endpoint:
POST /predict

Input:
Image File

Output:

```json
{
  "prediction": "Road_Damage",
  "confidence": 97.8
}
```

---

# Recommended Workflow

Citizen Report

↓

Duplicate Detection

↓

Image Authenticity Verification

↓

Road Damage Classification

↓

Citizen Trust Score

↓

Incident Severity Prediction

↓

Priority Allocation

↓

ETA Prediction

↓

Save To Database

↓

Display On Dashboard
