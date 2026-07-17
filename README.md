# SALEM

Smart AI-Powered Location & Excavation Management Ecosystem

SALEM is a full-scale digital ecosystem for managing location- and excavation-related incidents through a connected architecture that includes a backend API, a dashboard, a mobile application, and AI-powered intelligence. I designed this project as a practical solution for turning citizen reports into actionable operational workflows with speed, structure, and real-time visibility.

## Why I Built This

This system was created to solve a real operational problem: when incidents are reported by citizens, they often lack a consistent, intelligent, and trackable process for follow-up. SALEM brings together multiple layers of the solution into one connected platform:

- a backend API to handle authentication, business logic, and incident management
- a dashboard for monitoring, reviewing, and coordinating reports
- a mobile application for citizens and field users to interact with the system
- AI models to support duplicate detection, trust evaluation, severity prediction, priority recommendation, and image analysis

## What This Project Includes

### Core Features

- Citizen and employee authentication
- Role-based access for different user types
- Department and employee management
- Incident creation, assignment, review, and completion flows
- Notifications for operators and assigned teams
- Media upload support for before/after incident evidence
- AI-driven analysis for duplicate detection, trust scoring, severity classification, road damage detection, and image authenticity checks
- Password reset and OTP verification flow
- End-to-end workflow support across backend, dashboard, and mobile interfaces

### Technical Highlights

- Built with Django 5 and Django REST Framework
- JWT-based authentication for secure API access
- Custom validation and model constraints for role-specific business rules
- REST API endpoints for the full incident lifecycle
- Integration with external AI services through HTTP API calls
- Media handling for evidence-based reporting
- Email delivery and transactional messaging support through Brevo

## System Overview

SALEM is not just a backend project. It is a complete intelligent platform composed of several connected components that work together as one ecosystem:

- Backend API: manages data, business rules, authentication, and integrations
- Dashboard: gives operators and departments a way to review and manage incidents
- Mobile App: enables citizens and field users to report issues and interact with the system
- AI Models: provide automated insights that improve incident prioritization and decision-making

## Architecture Overview

The repository is organized around a clean backend structure that supports the broader system:

```text
backend/         # Django project settings and routing
Home/             # Additional app for project-level endpoints
media/            # Uploaded incident images and media files
postman/          # API collection for testing and development
staticfiles/     # Collected static assets
users/            # Main app containing models, views, services, and API logic
```

## Main Functional Flow

1. A citizen submits a report with location, description, and image evidence.
2. The backend validates the report and performs AI-based analysis.
3. The system detects duplicates, estimates trustworthiness, and evaluates severity.
4. The incident progresses through statuses such as new, assigned, in progress, review, forwarded, or completed.
5. Operators, departments, and connected interfaces receive updates and can act on the report.

## Tech Stack

- Python 3.10+
- Django 5.0
- Django REST Framework
- Simple JWT
- SQLite (default development database)
- Pillow
- Requests
- CORS headers
- PostgreSQL-ready structure for future production deployment

## Project Structure

```text
users/                # Authentication, accounts, incidents, departments, notifications
users/services/      # AI integration services for duplicate detection, trust scoring, severity, priority, and image analysis
backend/              # Core Django project configuration
media/                # Files uploaded by users
postman/              # API testing collection
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd SALEM
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the development server

```bash
python manage.py runserver
```

The application will be available at:

```text
http://127.0.0.1:8000/
```

## API Overview

The backend exposes REST endpoints under the following base route:

```text
/api/
```

Some of the main routes include:

- `/api/citizin/signup/`
- `/api/citizin/login/`
- `/api/employee/login/`
- `/api/incidence/citizin/create/`
- `/api/incidence/`
- `/api/department/`
- `/api/employee/`

A Postman collection is included in the [postman](postman) folder for quick testing.

## Authentication & Security

The API uses JWT-based authentication and includes structured request handling for citizen and employee workflows. For production deployment, I strongly recommend moving sensitive values such as secret keys, email credentials, and API tokens into environment variables.

## AI Integration

One of the strongest parts of this system is the AI layer. The backend connects to external AI services to support:

- duplicate report detection
- trust score prediction
- severity estimation
- priority recommendation
- road damage detection from images
- image authenticity analysis

This makes the platform more than a simple CRUD backend; it becomes an intelligent incident management system.

## What I Focused On While Building It

I paid special attention to the parts that make a real-world system reliable and scalable:

- clean API design for frontend and mobile integration
- role-based logic for different user types
- reliable incident status transitions
- media handling for evidence-based reporting
- extensibility for future dashboards, analytics, and automation
- a strong foundation for production-level expansion and maintenance

## Testing

Run the test suite with:

```bash
python manage.py test
```

## Future Improvements

Possible next steps for this project include:

- deeper dashboard analytics and reporting
- broader mobile experience optimization
- stronger workflow automation
- SMS and push notification support
- Docker and CI/CD deployment setup

## Contributing

If you want to contribute, feel free to fork the repository, create a feature branch, and submit a pull request.

## License

No license has been specified for this repository yet. If you plan to publish it publicly, consider adding an open-source license such as MIT or Apache 2.0.

## Contact

If you want to discuss this project, improve it, or collaborate further, feel free to reach out through the repository owner.
