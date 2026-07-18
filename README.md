<div align="center">

# SALEM
**Smart AI-Powered Local Emergency Management**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-092E20?style=flat-square&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/Django%20REST%20Framework-red?style=flat-square&logo=django&logoColor=white)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=flat-square&logo=jsonwebtokens&logoColor=white)](https://jwt.io)
[![Flutter](https://img.shields.io/badge/Flutter-Mobile-02569B?style=flat-square&logo=flutter&logoColor=white)](https://flutter.dev)
[![React](https://img.shields.io/badge/React-Dashboard-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-AI%20Services-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)

</div>

---

SALEM is a graduation project we built to solve a real problem: when citizens report public incidents, there's usually no reliable, trackable process to make sure anything actually gets done about it. We wanted to change that.

The system connects citizens, field employees, and government operators in one platform. A citizen reports an issue from their phone. The backend runs it through several AI models. The right department gets notified. An employee is assigned. The citizen gets updates. That's the loop we built — and we tried to make every part of it work properly, not just look good in a demo.

---

## What's inside

The project is split into four parts that all talk to each other:

- **Backend API** — Django + DRF, handles everything: auth, incidents, departments, notifications, and calling the AI services
- **Dashboard** — React.js interface for operators and admins to monitor and manage what's happening
- **Mobile App** — Flutter app for citizens to submit reports and employees to handle them in the field
- **AI Services** — a set of FastAPI microservices that do the actual intelligent analysis

---

## How it works

```
Citizen submits a report (image + location + description)
        │
        ▼
Backend validates and triggers AI pipeline
  ├─ Is the image real?
  ├─ Has this been reported before?
  ├─ What category does this fall under?
  ├─ How severe is it?
  └─ How trustworthy is this reporter?
        │
        ▼
Incident is created and appears on the dashboard
        │
        ▼
Operator assigns it to the right department + employee
        │
        ▼
Employee works on it, updates status from the field
        │
        ▼
Citizen gets notified when it's resolved
```

Incident statuses: `new` → `assigned` → `in_progress` → `review` → `completed` (or `forwarded`)

---

## AI Models

This is the part we're most proud of. Every report goes through a pipeline of models before it even reaches an operator.

| Model | What it does | Tech |
|-------|-------------|------|
| **Trust Score** | Scores how reliable this citizen's reports tend to be | XGBoost / Logistic Regression — 85.98% accuracy |
| **Severity Prediction** | Low / Medium / High / Critical classification | Random Forest — 78.07% on 6,000 samples |
| **Image Authenticity** | Catches fake or manipulated images | CNN (TensorFlow + Keras) |
| **Duplicate Detection** | Finds if the same image was submitted before | ResNet-50 + cosine similarity |
| **Object Detection** | Identifies road damage and scene context | YOLOv8 |
| **NLP Classification** | Reads the Arabic description and categorizes the incident | AraBERT |
| **Semantic Similarity** | Catches duplicate reports that are worded differently | Sentence Transformers |
| **ETA Prediction** | Estimates how long resolution will take | Gradient Boosting |

Each model runs as its own FastAPI service so we can update or scale them independently.

---

## Tech Stack

**Backend**
- Python 3.10+, Django 5.0, Django REST Framework
- Simple JWT — access tokens (15 min) + refresh tokens (7 days)
- SQLite for development, PostgreSQL-ready for production
- Brevo for transactional email and notifications

**AI Services**
- FastAPI + Uvicorn
- Scikit-learn, XGBoost, TensorFlow/Keras
- Ultralytics YOLOv8
- AraBERT, Hugging Face Transformers, Sentence Transformers

**Frontend & Mobile**
- React.js, Tailwind CSS, Recharts, React Leaflet, Framer Motion
- Flutter, Dio, Firebase Cloud Messaging, Google Maps

---

## Project Structure

```
SALEM/
├── AI/                       # AI models and microservices (FastAPI)
│   ├── trust_score/
│   ├── severity/
│   ├── duplicate_detection/
│   ├── image_authenticity/
│   └── nlp/
├── Backend/                  # Django REST API
│   ├── backend/              # Django settings and URL routing
│   ├── users/                # Auth, incidents, departments, notifications
│   │   └── services/         # AI service integration layer
│   ├── media/                # Uploaded incident images
│   └── postman/              # Postman collection for API testing
├── Frontend/                 # React.js dashboard
└── MobileApplication/        # Flutter app (citizen + employee)
```

---

## Getting Started

```bash
git clone https://github.com/abdullahgouda/SALEM.git
cd SALEM
```

**Backend**
```bash
cd Backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend (Dashboard)**
```bash
cd Frontend
npm install
npm start
```

**Mobile App**
```bash
cd MobileApplication
flutter pub get
flutter run
```

**AI Services** — each model inside `AI/` is a standalone FastAPI service. Navigate into the relevant folder and run:
```bash
uvicorn main:app --reload
```

---

## API

All routes live under `/api/`. A Postman collection is in the [`Backend/postman/`](Backend/postman) folder.

**Auth**
```
POST  /api/citizin/signup/
POST  /api/citizin/login/
POST  /api/employee/login/
POST  /api/auth/refresh/
```

**Incidents**
```
POST  /api/incidence/citizin/create/
GET   /api/incidence/
PUT   /api/incidence/{id}/status/
```

**Management**
```
GET   /api/department/
GET   /api/employee/
GET   /api/statistics/heatmap/
```

**AI Endpoints**
```
POST  /api/ai/trust-score/predict/
POST  /api/ai/severity/predict/
POST  /api/ai/image-authenticity/predict/
POST  /api/ai/duplicate-detection/check/
POST  /api/ai/nlp/classify/
```

---

## Authentication

JWT with role-based access. Three roles: `Citizen`, `Employee`, `Administrator` — each with its own permission class enforced at the view level.

> Before deploying to production, move `SECRET_KEY`, email credentials, and AI service tokens into environment variables.

---

## Tests

```bash
python manage.py test
```

---

## What's next

Things we'd like to add if we keep working on this:

- Docker setup and a proper CI/CD pipeline
- SMS notifications
- IoT sensor integration for automated reporting
- PDF report exports from the dashboard
- Live camera feed with YOLOv8 for automated detection

---

## Team

- Abdallah Farag
- Amer Mohamed
- Esraa Magdy
- Hassan Tarek
- Micheal Salama

---

## License

No license yet. If you're making this public, [MIT](https://choosealicense.com/licenses/mit/) is a good starting point.