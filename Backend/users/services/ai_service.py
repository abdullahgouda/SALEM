import requests

BASE_URL = "https://amerramerr-salem-ai-services.hf.space"


# ==========================
# Duplicate Detection
# ==========================

def check_duplicate(description):
    try:
        response = requests.post(
            f"{BASE_URL}/duplicate/check-duplicate",
            json={
                "description": description
            },
            timeout=30
        )

        print("Duplicate Status:", response.status_code)
        print("Duplicate Body:", response.text)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("Duplicate API Error:", e)
        return None


# ==========================
# Trust Model
# ==========================

def get_trust_score(
    valid_ratio,
    duplicate_rate,
    fake_image_ratio,
    reports_last_30_days,
    avg_severity_reported
):
    try:
        response = requests.post(
            f"{BASE_URL}/trust/predict",
            json={
                "valid_ratio": valid_ratio,
                "duplicate_rate": duplicate_rate,
                "fake_image_ratio": fake_image_ratio,
                "reports_last_30_days": reports_last_30_days,
                "avg_severity_reported": avg_severity_reported
            },
            timeout=30
        )

        print("Trust Status:", response.status_code)
        print("Trust Body:", response.text)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("Trust API Error:", e)
        return None


# ==========================
# Severity Model
# ==========================

def get_severity(
    citizen_trust_score,
    anomaly_score,
    image_authenticity_score,
    reports_nearby_1h,
    historical_severity_avg
):
    try:
        response = requests.post(
            f"{BASE_URL}/severity/predict",
            json={
                "citizen_trust_score": citizen_trust_score,
                "anomaly_score": anomaly_score,
                "image_authenticity_score": image_authenticity_score,
                "reports_nearby_1h": reports_nearby_1h,
                "historical_severity_avg": historical_severity_avg
            },
            timeout=30
        )

        print("Severity Status:", response.status_code)
        print("Severity Body:", response.text)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("Severity API Error:", e)
        return None


# ==========================
# Priority Model
# ==========================

def get_priority(
    severity_label,
    severity_score,
    area_load,
    available_teams,
    team_skill_match,
    historical_team_performance,
    citizen_trust_score,
    reports_nearby_1h
):
    try:
        response = requests.post(
            f"{BASE_URL}/priority/predict",
            json={
                "severity_label": severity_label,
                "severity_score": severity_score,
                "area_load": area_load,
                "available_teams": available_teams,
                "team_skill_match": team_skill_match,
                "historical_team_performance": historical_team_performance,
                "citizen_trust_score": citizen_trust_score,
                "reports_nearby_1h": reports_nearby_1h
            },
            timeout=30
        )

        print("Priority Status:", response.status_code)
        print("Priority Body:", response.text)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("Priority API Error:", e)
        return None


# ==========================
# Road Damage Detection
# ==========================

def detect_road_damage(image_file):
    try:
        image_file.seek(0)
        response = requests.post(
            f"{BASE_URL}/road/predict",
            files={
                "image": (
                    image_file.name,
                    image_file.read(),
                    image_file.content_type
    )
            },
            timeout=60
        )

        print("Road Status:", response.status_code)
        print("Road Body:", response.text)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("Road Damage API Error:", e)
        return None


# ==========================
# Image Authenticity
# ==========================

def check_image_authenticity(image_file):
    try:
        image_file.seek(0)
        response = requests.post(
            f"{BASE_URL}/image/predict",
            files={
               "file": (
                    image_file.name,
                    image_file.read(),
                    image_file.content_type
    )
            },
            timeout=60
        )

        print("Image Status:", response.status_code)
        print("Image Body:", response.text)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("Image Authenticity API Error:", e)
        return None