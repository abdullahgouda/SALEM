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

- **[Backend](./Backend)** — Django + DRF, handles everything: auth, incidents, departments, notifications, and calling the AI services
- **[Frontend](./Frontend)** — React.js dashboard for operators and admins to monitor and manage what's happening
- **[MobileApplication](./MobileApplication)** — Flutter app for citizens to submit reports and employees to handle them in the field
- **[AI](./AI)** — a set of FastAPI microservices that do the actual intelligent analysis

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
| **Duplicate Detection** | Finds if the same image was submitted before | Feature extraction + cosine similarity |
| **Object Detection** | Identifies road damage and scene context | YOLOv8 |
| **NLP Classification** | Reads the Arabic description and categorizes the incident | AraBERT |
| **Semantic Similarity** | Catches duplicate reports that are worded differently | Sentence Transformers |
| **ETA Prediction** | Estimates how long resolution will take | Gradient Boosting |

Each model runs as its own FastAPI service so we can update or scale them independently.

---

## Tech Stack

**Backend**
- Python 3.10+, Django 5.0, Django REST Framework
- Simple JWT for authentication
- SQLite for development, PostgreSQL-ready for production
- Brevo for transactional email and notifications

**AI Services**
- FastAPI + Uvicorn
- Scikit-learn, XGBoost, TensorFlow/Keras
- Ultralytics YOLOv8
- AraBERT, Hugging Face Transformers, Sentence Transformers

**Frontend & Mobile**
- React.js, Tailwind CSS, Recharts, React Leaflet
- Flutter + Google Maps

---

## Project Structure

```
SALEM/
├── AI/                   # AI models and FastAPI microservices
├── Backend/              # Django REST API
├── Frontend/             # React.js dashboard
└── MobileApplication/    # Flutter app (citizen + employee)
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
source venv/bin/activate
# Windows: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

**Frontend**
```bash
cd Frontend
npm install
npm start
```
> Check `Frontend/` for any additional setup steps or environment variables needed.

**Mobile App**
```bash
cd MobileApplication
flutter pub get
flutter run
```

**AI Services**

Each model inside `AI/` is a standalone FastAPI service. Navigate into the relevant subfolder and follow the setup instructions there.

---

## API

All routes live under `/api/`. A Postman collection is included in the `Backend/` folder for testing the full API.

**Auth**
```
POST  /api/citizin/signup/
POST  /api/citizin/login/
POST  /api/employee/login/
```

**Incidents**
```
POST  /api/incidence/citizin/create/
GET   /api/incidence/
```

**Management**
```
GET   /api/department/
GET   /api/employee/
```

> The full list of endpoints is in the Postman collection.

---

## Authentication

JWT-based with role-based access control. Three roles: `Citizen`, `Employee`, `Administrator` — each with its own permission class enforced at the view level.

> Before deploying to production, move `SECRET_KEY`, email credentials, and AI service tokens into environment variables.

---

## Tests

```bash
cd Backend
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