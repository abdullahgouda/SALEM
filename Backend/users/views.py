import json
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps

from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone as django_timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods

from .brevo_api import BrevoEmailError, send_transactional_email
from .models import Department, Incidence, OperatorNotification, PasswordResetOTP, User

from .services.ai_service import (
    check_duplicate,
    check_image_authenticity,
    detect_road_damage,
    get_trust_score,
    get_severity,
    get_priority
)


INCIDENCE_STATUS_FILTER_MAP = {
    "new": Incidence.Status.NEW,
    "assigned": Incidence.Status.ASSIGNED,
    "in_progress": Incidence.Status.IN_PROGRESS,
    "in progress": Incidence.Status.IN_PROGRESS,
    "review": Incidence.Status.REVIEW,
    "in_review": Incidence.Status.REVIEW,
    "forworded": Incidence.Status.FORWORDED,
    "forwarded": Incidence.Status.FORWORDED,
    "finished": Incidence.Status.FINISHED,
    "completed": Incidence.Status.FINISHED,
}
COMPLETED_INCIDENCE_STATUSES = (
    Incidence.Status.FINISHED,
    "Completed",
)
FORWORDED_INCIDENCE_STATUSES = (
    Incidence.Status.FORWORDED,
    "Forwarded",
)


def _extract_credentials(request):
    national_id = None
    password = None

    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, None, "Invalid JSON body."

        national_id = payload.get("National_id") or payload.get("national_id")
        password = payload.get("Password") or payload.get("password")
    else:
        national_id = request.POST.get("National_id") or request.POST.get("national_id")
        password = request.POST.get("Password") or request.POST.get("password")

    if not national_id or not password:
        return None, None, "National_id and Password are required."

    return str(national_id).strip(), str(password), None


def _extract_citizin_credentials(request):
    email = None
    phone_number = None
    password = None

    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, None, None, "Invalid JSON body."

        email = payload.get("Email") or payload.get("email")
        phone_number = payload.get("Phone_Number") or payload.get("phone_number")
        identifier = payload.get("Email_or_Phone_Number") or payload.get("email_or_phone_number")
        password = payload.get("Password") or payload.get("password")
    else:
        email = request.POST.get("Email") or request.POST.get("email")
        phone_number = request.POST.get("Phone_Number") or request.POST.get("phone_number")
        identifier = request.POST.get("Email_or_Phone_Number") or request.POST.get("email_or_phone_number")
        password = request.POST.get("Password") or request.POST.get("password")

    if not email and not phone_number and identifier:
        identifier = str(identifier).strip()
        if "@" in identifier:
            email = identifier
        else:
            phone_number = identifier

    if not password:
        return None, None, None, "Password is required."

    if not email and not phone_number:
        return None, None, None, "Email or Phone_Number is required."

    email = str(email).strip() if email else None
    phone_number = str(phone_number).strip() if phone_number else None
    return email, phone_number, str(password), None


def _extract_citizin_signup_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, "Invalid JSON body."
    else:
        payload = request.POST

    data = {
        "name": payload.get("Name") or payload.get("name"),
        "phone_number": payload.get("Phone_Number") or payload.get("phone_number"),
        "email": payload.get("Email") or payload.get("email"),
        "national_id": payload.get("National_Id") or payload.get("national_id"),
        "password": payload.get("Password") or payload.get("password"),
        "user_type": payload.get("User_Type") or payload.get("user_type"),
        "birthdate": payload.get("Birthdate") or payload.get("birthdate"),
        "username": payload.get("Username") or payload.get("username"),
    }

    required_fields = [
        "name",
        "phone_number",
        "email",
        "national_id",
        "password",
        "user_type",
        "birthdate",
        "username",
    ]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return None, f"Missing required fields: {', '.join(missing)}."

    data["name"] = str(data["name"]).strip()
    data["phone_number"] = str(data["phone_number"]).strip()
    data["email"] = str(data["email"]).strip()
    data["national_id"] = str(data["national_id"]).strip()
    data["password"] = str(data["password"])
    data["user_type"] = str(data["user_type"]).strip().lower()
    data["birthdate"] = str(data["birthdate"]).strip()
    data["username"] = str(data["username"]).strip()
    return data, None


def _parse_account_status(account_status_value):
    if account_status_value is None:
        return True, None

    if isinstance(account_status_value, bool):
        return account_status_value, None

    normalized_value = str(account_status_value).strip().lower()
    if normalized_value in {"نشط", "active", "enabled", "true", "1"}:
        return True, None
    if normalized_value in {"معطل", "inactive", "disabled", "false", "0"}:
        return False, None

    return None, "Account_Status must be either 'نشط' or 'معطل'."


def _extract_employee_signup_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, "Invalid JSON body."
    else:
        payload = request.POST

    account_status_value = payload.get("Account_Status")
    if account_status_value is None:
        account_status_value = payload.get("account_status")

    is_active, account_status_error = _parse_account_status(account_status_value)
    if account_status_error:
        return None, account_status_error

    data = {
        "name": payload.get("Name") or payload.get("name"),
        "national_id": payload.get("National_Id") or payload.get("national_id"),
        "phone_number": payload.get("Phone_Number") or payload.get("phone_number"),
        "email": payload.get("Email") or payload.get("email"),
        "password": payload.get("Password") or payload.get("password"),
        "user_type": payload.get("User_Type") or payload.get("user_type"),
        "role": payload.get("Role") or payload.get("role"),
        "region": payload.get("Region") or payload.get("region"),
        "department": (
            payload.get("Department")
            or payload.get("department")
            or payload.get("Department_Id")
            or payload.get("department_id")
        ),
        "is_active": is_active,
    }

    required_fields = [
        "name",
        "national_id",
        "phone_number",
        "email",
        "password",
        "user_type",
        "role",
        "region",
        "department",
    ]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return None, f"Missing required fields: {', '.join(missing)}."

    data["name"] = str(data["name"]).strip()
    data["national_id"] = str(data["national_id"]).strip()
    data["phone_number"] = str(data["phone_number"]).strip()
    data["email"] = str(data["email"]).strip()
    data["password"] = str(data["password"])
    data["user_type"] = str(data["user_type"]).strip().lower()
    data["role"] = str(data["role"]).strip().lower()
    data["region"] = str(data["region"]).strip()
    return data, None


def _resolve_department(department_value):
    if isinstance(department_value, int):
        return Department.objects.filter(id=department_value).first()

    value = str(department_value).strip()
    if not value:
        return None

    if value.isdigit():
        return Department.objects.filter(id=int(value)).first()

    return Department.objects.filter(name__iexact=value).first()

@api_view(["POST"])
def approve_report(request, report_id):

    incidence = get_object_or_404(
    Incidence,
    id=report_id
)

    incidence.status = Incidence.Status.NEW
    incidence.save()

    return Response({
        "message": "Report approved successfully"
    })

@api_view(["POST"])
def reject_report(request, report_id):

    incidence = get_object_or_404(
    Incidence,
    id=report_id
)

    incidence.status = Incidence.Status.REJECTED
    incidence.save()


    return Response({
        "message": "Report rejected successfully"
    })
def _extract_department_form_data(request):
    name = request.POST.get("Name") or request.POST.get("name")
    logo = request.FILES.get("Logo") or request.FILES.get("logo")

    if not name:
        return None, None, "Name is required."
    if not logo:
        return None, None, "Logo file is required. Use form-data."

    return str(name).strip(), logo, None


def _department_to_dict(request, department):
    logo_url = request.build_absolute_uri(department.logo.url) if department.logo else None
    return {
        "id": department.id,
        "Name": department.name,
        "Logo": logo_url,
    }


def _employee_to_dict(employee):
    return {
        "id": employee.id,
        "Name": employee.name,
        "Email": employee.email,
        "Role": employee.role,
        "Account_Status": "نشط" if employee.is_active else "معطل",
    }


def _employee_details_to_dict(employee):
    return {
        "id": employee.id,
        "Name": employee.name,
        "National_Id": employee.national_id,
        "Phone_Number": employee.phone_number,
        "Email": employee.email,
        "User_Type": employee.user_type,
        "Role": employee.role,
        "Account_Status": "نشط" if employee.is_active else "معطل",
        "Region": employee.region,
        "Department": (
            {"id": employee.department_id, "name": employee.department.name}
            if employee.department
            else None
        ),
    }


def _extract_department_update_form_data(request):
    name = request.POST.get("Name") or request.POST.get("name")
    logo = request.FILES.get("Logo") or request.FILES.get("logo")

    if name is not None:
        name = str(name).strip()
        if not name:
            return None, None, "Name cannot be empty."

    if name is None and logo is None:
        return None, None, "Provide at least one field to update: Name or Logo."

    return name, logo, None


def _extract_employee_update_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, "Invalid JSON body."
    else:
        payload = request.POST

    updates = {}

    name = payload.get("Name") if "Name" in payload else payload.get("name")
    if name is not None:
        name = str(name).strip()
        if not name:
            return None, "Name cannot be empty."
        updates["name"] = name

    national_id = payload.get("National_Id") if "National_Id" in payload else payload.get("national_id")
    if national_id is not None:
        national_id = str(national_id).strip()
        if not national_id:
            return None, "National_Id cannot be empty."
        updates["national_id"] = national_id

    phone_number = payload.get("Phone_Number") if "Phone_Number" in payload else payload.get("phone_number")
    if phone_number is not None:
        phone_number = str(phone_number).strip()
        if not phone_number:
            return None, "Phone_Number cannot be empty."
        updates["phone_number"] = phone_number

    email = payload.get("Email") if "Email" in payload else payload.get("email")
    if email is not None:
        email = str(email).strip()
        if not email:
            return None, "Email cannot be empty."
        updates["email"] = email

    role = payload.get("Role") if "Role" in payload else payload.get("role")
    if role is not None:
        role = str(role).strip().lower()
        if not role:
            return None, "Role cannot be empty."
        updates["role"] = role

    region = payload.get("Region") if "Region" in payload else payload.get("region")
    if region is not None:
        region = str(region).strip()
        if not region:
            return None, "Region cannot be empty."
        updates["region"] = region

    department_provided = any(
        key in payload for key in ("Department", "department", "Department_Id", "department_id")
    )
    if department_provided:
        department_value = (
            payload.get("Department")
            or payload.get("department")
            or payload.get("Department_Id")
            or payload.get("department_id")
        )
        if department_value in [None, ""]:
            return None, "Department cannot be empty."

        department = _resolve_department(department_value)
        if not department:
            return None, "Department not found."
        updates["department"] = department

    account_status_provided = "Account_Status" in payload or "account_status" in payload
    if account_status_provided:
        account_status_value = payload.get("Account_Status")
        if account_status_value is None:
            account_status_value = payload.get("account_status")

        is_active, account_status_error = _parse_account_status(account_status_value)
        if account_status_error:
            return None, account_status_error
        updates["is_active"] = is_active

    if not updates:
        return None, "Provide at least one field to update."

    return updates, None


def _extract_citizin_incidence_form_data(request):
    description = request.POST.get("Description") or request.POST.get("description")
    latlatitude = (
        request.POST.get("Latlatitude")
        or request.POST.get("latlatitude")
        or request.POST.get("Latitude")
        or request.POST.get("latitude")
    )
    longitude = request.POST.get("Longitude") or request.POST.get("longitude")
    location_name = request.POST.get("Location_Name") or request.POST.get("location_name")
    department_value = (
        request.POST.get("Department")
        or request.POST.get("department")
        or request.POST.get("Department_Id")
        or request.POST.get("department_id")
    )
    image_before_analysis = (
        request.FILES.get("Image_Before_Analysis")
        or request.FILES.get("image_before_analysis")
    )

    missing = []
    if not description:
        missing.append("Description")
    if not latlatitude:
        missing.append("Latlatitude")
    if not longitude:
        missing.append("Longitude")
    if not location_name:
        missing.append("Location_Name")
    if not department_value:
        missing.append("Department")
    if not image_before_analysis:
        missing.append("Image_Before_Analysis")

    if missing:
        return None, f"Missing required fields: {', '.join(missing)}. Use form-data."

    return (
        {
            "description": str(description).strip(),
            "latlatitude": str(latlatitude).strip(),
            "longitude": str(longitude).strip(),
            "location_name": str(location_name).strip(),
            "department_value": department_value,
            "image_before_analysis": image_before_analysis,
        },
        None,
    )


def _extract_incidence_assignment_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, "Invalid JSON body."
    else:
        payload = request.POST

    incidence_id = payload.get("Incidence_id") or payload.get("incidence_id")

    if not incidence_id:
        return None, "Incidence_id is required."

    try:
        incidence_id = int(str(incidence_id).strip())
    except (TypeError, ValueError):
        return None, "Incidence_id must be a valid integer."

    return {"incidence_id": incidence_id}, None


def _extract_incidence_in_progress_update_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, "Invalid JSON body."
    else:
        payload = request.POST

    lat_value = (
        payload.get("Lat")
        or payload.get("lat")
        or payload.get("Latlatitude")
        or payload.get("latlatitude")
        or payload.get("Latitude")
        or payload.get("latitude")
    )
    long_value = (
        payload.get("Long")
        or payload.get("long")
        or payload.get("Longitude")
        or payload.get("longitude")
    )
    location_name = payload.get("Location_Name") or payload.get("location_name")

    missing = []
    if lat_value in [None, ""]:
        missing.append("Lat")
    if long_value in [None, ""]:
        missing.append("Long")
    if location_name in [None, ""]:
        missing.append("Location_Name")

    if missing:
        return None, f"Missing required fields: {', '.join(missing)}."

    return {
        "latlatitude": str(lat_value).strip(),
        "longitude": str(long_value).strip(),
        "location_name": str(location_name).strip(),
    }, None


def _extract_incidence_review_form_data(request):
    what_was_done = (
        request.POST.get("What_Was_Done")
        or request.POST.get("what_was_done")
        or request.POST.get("What_was_done")
    )
    image_after_analysis = (
        request.FILES.get("Image_After_Analysis")
        or request.FILES.get("image_after_analysis")
    )

    missing = []
    if not image_after_analysis:
        missing.append("Image_After_Analysis")
    if not what_was_done:
        missing.append("What_Was_Done")

    if missing:
        return None, f"Missing required fields: {', '.join(missing)}. Use form-data."

    return {
        "image_after_analysis": image_after_analysis,
        "what_was_done": str(what_was_done).strip(),
    }, None


def _extract_incidence_list_filters(request):
    params = request.GET

    department_value = (
        params.get("Department")
        or params.get("department")
        or params.get("Department_Id")
        or params.get("department_id")
    )
    date_value = (
        params.get("Date")
        or params.get("date")
        or params.get("Created_At")
        or params.get("created_at")
    )
    status_value = params.get("Status") or params.get("status")
    search_value = (
        params.get("Search")
        or params.get("search")
        or params.get("Incidence_id")
        or params.get("incidence_id")
        or params.get("Id")
        or params.get("id")
    )

    filters = {}

    if department_value not in [None, ""]:
        department = _resolve_department(department_value)
        if not department:
            return None, "Department not found."
        filters["department_id"] = department.id

    if date_value not in [None, ""]:
        try:
            filters["created_at_date"] = datetime.strptime(str(date_value).strip(), "%Y-%m-%d").date()
        except ValueError:
            return None, "Date must be in YYYY-MM-DD format."

    if status_value not in [None, ""]:
        normalized_status = INCIDENCE_STATUS_FILTER_MAP.get(str(status_value).strip().lower())
        if not normalized_status:
            return None, "Invalid status filter."
        filters["status"] = normalized_status

    if search_value not in [None, ""]:
        search_value = str(search_value).strip()
        if not search_value.isdigit():
            return None, "Search by id must be a valid integer."
        filters["id"] = int(search_value)

    return filters, None


def _incidence_to_dict(request, incidence):
    image_before_url = (
        request.build_absolute_uri(incidence.image_before_analysis.url)
        if incidence.image_before_analysis
        else None
    )
    image_after_url = (
        request.build_absolute_uri(incidence.image_after_analysis.url)
        if incidence.image_after_analysis
        else None
    )

    assigned_employee_data = None
    if incidence.assigned_employee:
        assigned_employee_data = {
            "id": incidence.assigned_employee.id,
            "Name": incidence.assigned_employee.name,
            "Role": incidence.assigned_employee.role,
        }

    return {
        "id": incidence.id,
        "Created_At": incidence.created_at.isoformat() if incidence.created_at else None,
        "Description": incidence.description,
        "Latlatitude": str(incidence.latlatitude),
        "Longitude": str(incidence.longitude),
        "Location_Name": incidence.location_name,
        "Status": incidence.status,
        "Location_Confirmation": incidence.location_confirmation,
        "Priority": incidence.priority,
        "Image_Before_Analysis": image_before_url,
        "Image_After_Analysis": image_after_url,
        "Ai_Analysis_Label_Before": incidence.ai_analysis_label_before,
        "Ai_Analysis_Label_After": incidence.ai_analysis_label_after,
        "What_was_done": incidence.what_was_done,
        "Department": (
            {"id": incidence.department_id, "name": incidence.department.name}
            if incidence.department
            else None
        ),
        "Citizin": {
            "id": incidence.citizin_id,
            "Name": incidence.citizin.name,
            "Phone_Number": incidence.citizin.phone_number,
        },
        "Assigned_Employee": assigned_employee_data,
    }


def _extract_forgot_password_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, "Invalid JSON body."
    else:
        payload = request.POST

    email = payload.get("Email") or payload.get("email")
    if not email:
        return None, "Email is required."

    return str(email).strip(), None


def _extract_verify_otp_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, None, "Invalid JSON body."
    else:
        payload = request.POST

    email = payload.get("Email") or payload.get("email")
    otp = payload.get("OTP") or payload.get("otp")
    if not email or not otp:
        return None, None, "Email and OTP are required."

    otp = str(otp).strip()
    if len(otp) != 6 or not otp.isdigit():
        return None, None, "OTP must be a 6-digit number."

    return str(email).strip(), otp, None


def _extract_reset_password_payload(request):
    if request.content_type and "application/json" in request.content_type:
        try:
            payload = json.loads(request.body.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return None, None, "Invalid JSON body."
    else:
        payload = request.POST

    email = payload.get("Email") or payload.get("email")
    new_password = (
        payload.get("New_Password")
        or payload.get("new_password")
        or payload.get("Password")
        or payload.get("password")
    )
    if not email or not new_password:
        return None, None, "Email and New_Password are required."

    return str(email).strip(), str(new_password), None


def _generate_otp():
    return f"{secrets.randbelow(1000000):06d}"


def _verify_password(raw_password, stored_password):
    try:
        if check_password(raw_password, stored_password):
            return True
    except ValueError:
        pass

    return raw_password == stored_password


def _build_token(user, token_type, expires_delta):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "national_id": user.national_id,
        "user_type": user.user_type,
        "role": user.role,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def _can_complete_incidence(employee):
    if not employee:
        return False

    return employee.role in {
        User.EmployeeRole.ADMIN,
        User.EmployeeRole.SUPERVISIOR,
    }


def _extract_bearer_token(request):
    auth_header = request.headers.get("Authorization") or request.META.get("HTTP_AUTHORIZATION", "")
    parts = auth_header.strip().split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


def employee_access_token_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        token = _extract_bearer_token(request)
        if not token:
            return JsonResponse({"message": "Authorization Bearer token is required."}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token has expired."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid token."}, status=401)

        if payload.get("type") != "access":
            return JsonResponse({"message": "Access token is required."}, status=401)

        if payload.get("user_type") != User.UserType.EMPLOYEE:
            return JsonResponse({"message": "Employee token is required for this action."}, status=403)

        user_id = payload.get("sub")
        employee = User.objects.filter(id=user_id, user_type=User.UserType.EMPLOYEE).first()
        if not employee:
            return JsonResponse({"message": "Invalid token user."}, status=401)

        request.employee_user = employee
        return view_func(request, *args, **kwargs)

    return _wrapped


def citizin_access_token_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        token = _extract_bearer_token(request)
        if not token:
            return JsonResponse({"message": "Authorization Bearer token is required."}, status=401)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token has expired."}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid token."}, status=401)

        if payload.get("type") != "access":
            return JsonResponse({"message": "Access token is required."}, status=401)

        if payload.get("user_type") != User.UserType.CITIZIN:
            return JsonResponse({"message": "Citizin token is required for this action."}, status=403)

        user_id = payload.get("sub")
        citizin = User.objects.filter(id=user_id, user_type=User.UserType.CITIZIN).first()
        if not citizin:
            return JsonResponse({"message": "Invalid token user."}, status=401)

        request.citizin_user = citizin
        return view_func(request, *args, **kwargs)

    return _wrapped


@csrf_exempt
@require_POST
def employee_login(request):
    national_id, password, error = _extract_credentials(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    try:
        user = User.objects.get(national_id=national_id)
    except User.DoesNotExist:
        return JsonResponse({"message": "Invalid National_id or Password."}, status=401)

    if user.user_type != User.UserType.EMPLOYEE:
        return JsonResponse({"message": "This login is only for employee users."}, status=403)

    if not _verify_password(password, user.password):
        return JsonResponse({"message": "Invalid National_id or Password."}, status=401)

    access_token = _build_token(user, "access", timedelta(minutes=15))
    refresh_token = _build_token(user, "refresh", timedelta(days=7))

    return JsonResponse(
        {
            "id": user.id,
            "Name": user.name,
            "Role": user.role,
            "User_type": user.user_type,

            "Department": (
                {
                "id": user.department.id,
                "name": user.department.name,
                }
                if user.department
                else None
            ),

            "Asscess_Token": access_token,
            "Refresh_Token": refresh_token,
        },
        status=200,
    )


@csrf_exempt
@require_POST
def citizin_login(request):
    email, phone_number, password, error = _extract_citizin_credentials(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    query = Q(user_type=User.UserType.CITIZIN)
    if email and phone_number:
        query &= (Q(email=email) | Q(phone_number=phone_number))
    elif email:
        query &= Q(email=email)
    else:
        query &= Q(phone_number=phone_number)

    user = User.objects.filter(query).first()
    if not user:
        return JsonResponse({"message": "Invalid Email/Phone_Number or Password."}, status=401)

    if not _verify_password(password, user.password):
        return JsonResponse({"message": "Invalid Email/Phone_Number or Password."}, status=401)

    access_token = _build_token(user, "access", timedelta(minutes=15))
    refresh_token = _build_token(user, "refresh", timedelta(days=7))

    return JsonResponse(
        {
            "Name": user.name,
            "User_Type": user.user_type,
            "Access_Token": access_token,
            "Refresh_Token": refresh_token,
        },
        status=200,
    )


@csrf_exempt
@require_POST
def citizin_signup(request):
    data, error = _extract_citizin_signup_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    if data["user_type"] != User.UserType.CITIZIN:
        return JsonResponse({"message": "User_Type must be 'citizin' for this endpoint."}, status=400)

    try:
        user = User.objects.create(
            name=data["name"],
            phone_number=data["phone_number"],
            email=data["email"],
            national_id=data["national_id"],
            password=make_password(data["password"]),
            user_type=data["user_type"],
            birthdate=data["birthdate"],
            username=data["username"],
        )
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)
    except IntegrityError:
        return JsonResponse(
            {"message": "National_Id, Phone_Number, Email or Username already exists."},
            status=400,
        )

    return JsonResponse(
        {
            "message": "Citizin account created successfully.",
            "user": {
                "Name": user.name,
                "Phone_Number": user.phone_number,
                "Email": user.email,
                "National_Id": user.national_id,
                "User_Type": user.user_type,
                "Birthdate": str(user.birthdate),
                "Username": user.username,
            },
        },
        status=201,
    )


@csrf_exempt
@require_POST
def employee_signup(request):
    data, error = _extract_employee_signup_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    if data["user_type"] != User.UserType.EMPLOYEE:
        return JsonResponse({"message": "User_Type must be 'employee' for this endpoint."}, status=400)

    department = _resolve_department(data["department"])
    if not department:
        return JsonResponse({"message": "Department not found."}, status=400)

    try:
        user = User.objects.create(
            name=data["name"],
            national_id=data["national_id"],
            phone_number=data["phone_number"],
            email=data["email"],
            password=make_password(data["password"]),
            user_type=data["user_type"],
            role=data["role"],
            region=data["region"],
            department=department,
            is_active=data["is_active"],
        )
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)
    except IntegrityError:
        return JsonResponse(
            {"message": "National_Id, Phone_Number or Email already exists."},
            status=400,
        )

    return JsonResponse(
        {
            "message": "Employee account created successfully.",
            "user": {
                "Name": user.name,
                "National_Id": user.national_id,
                "Phone_Number": user.phone_number,
                "Email": user.email,
                "User_Type": user.user_type,
                "Role": user.role,
                "Account_Status": "نشط" if user.is_active else "معطل",
                "Region": user.region,
                "Department": {"id": user.department_id, "name": user.department.name},
            },
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_all_employees(request):
    employees = User.objects.filter(user_type=User.UserType.EMPLOYEE).order_by("-id")
    data = [_employee_to_dict(employee) for employee in employees]
    return JsonResponse(
        {
            "Total_Employees": len(data),
            "employees": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["POST", "PUT", "PATCH"])
@employee_access_token_required
def update_employee(request, employee_id):
    employee = User.objects.filter(id=employee_id, user_type=User.UserType.EMPLOYEE).first()
    if not employee:
        return JsonResponse({"message": "Employee not found."}, status=404)

    updates, error = _extract_employee_update_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    if "name" in updates:
        employee.name = updates["name"]
    if "national_id" in updates:
        employee.national_id = updates["national_id"]
    if "phone_number" in updates:
        employee.phone_number = updates["phone_number"]
    if "email" in updates:
        employee.email = updates["email"]
    if "role" in updates:
        employee.role = updates["role"]
    if "region" in updates:
        employee.region = updates["region"]
    if "department" in updates:
        employee.department = updates["department"]
    if "is_active" in updates:
        employee.is_active = updates["is_active"]

    try:
        employee.save()
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)
    except IntegrityError:
        return JsonResponse(
            {"message": "National_Id, Phone_Number or Email already exists."},
            status=400,
        )

    return JsonResponse(
        {
            "message": "Employee updated successfully.",
            "employee": _employee_details_to_dict(employee),
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
@employee_access_token_required
def delete_employee(request, employee_id):
    employee = User.objects.filter(id=employee_id, user_type=User.UserType.EMPLOYEE).first()
    if not employee:
        return JsonResponse({"message": "Employee not found."}, status=404)

    if request.employee_user.id == employee.id:
        return JsonResponse({"message": "You cannot delete your own account."}, status=400)

    employee.delete()
    return JsonResponse({"message": "Employee deleted successfully."}, status=200)


@csrf_exempt
@require_POST
def forgot_password(request):
    email, error = _extract_forgot_password_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    user = User.objects.filter(email__iexact=email).first()
    if not user:
        return JsonResponse({"message": "No account found with this email."}, status=404)

    PasswordResetOTP.objects.filter(email__iexact=user.email, is_used=False).update(is_used=True)

    otp_code = _generate_otp()
    expires_at = django_timezone.now() + timedelta(minutes=10)

    PasswordResetOTP.objects.create(
        user=user,
        email=user.email,
        otp_code=otp_code,
        expires_at=expires_at,
    )

    try:
        send_transactional_email(
            to_email=user.email,
            to_name=user.name,
            subject="Password Reset OTP",
            text_content=f"Your OTP is {otp_code}. It will expire in 10 minutes.",
        )
    except BrevoEmailError as exc:
        if settings.DEBUG:
            return JsonResponse({"message": "Failed to send OTP email.", "error": str(exc)}, status=500)
        return JsonResponse({"message": "Failed to send OTP email."}, status=500)
    except Exception as exc:
        if settings.DEBUG:
            return JsonResponse({"message": "Failed to send OTP email.", "error": str(exc)}, status=500)
        return JsonResponse({"message": "Failed to send OTP email."}, status=500)

    return JsonResponse({"message": "OTP sent to email successfully."}, status=200)


@csrf_exempt
@require_POST
def verify_password_otp(request):
    email, otp_code, error = _extract_verify_otp_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    otp_record = (
        PasswordResetOTP.objects.filter(email__iexact=email, otp_code=otp_code, is_used=False)
        .order_by("-created_at")
        .first()
    )
    if not otp_record:
        return JsonResponse({"message": "Invalid OTP or Email."}, status=400)

    now = django_timezone.now()
    if otp_record.expires_at <= now:
        otp_record.is_used = True
        otp_record.save(update_fields=["is_used"])
        return JsonResponse({"message": "OTP expired. Please request a new OTP."}, status=400)

    otp_record.is_verified = True
    otp_record.save(update_fields=["is_verified"])

    return JsonResponse({"message": "OTP verified successfully."}, status=200)


@csrf_exempt
@require_POST
def reset_password(request):
    email, new_password, error = _extract_reset_password_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    otp_record = (
        PasswordResetOTP.objects.filter(email__iexact=email, is_verified=True, is_used=False)
        .order_by("-created_at")
        .first()
    )
    if not otp_record:
        return JsonResponse({"message": "OTP verification is required before resetting password."}, status=400)

    now = django_timezone.now()
    if otp_record.expires_at <= now:
        otp_record.is_used = True
        otp_record.save(update_fields=["is_used"])
        return JsonResponse({"message": "Verified OTP expired. Please request a new OTP."}, status=400)

    user = otp_record.user
    user.password = make_password(new_password)
    user.save(update_fields=["password"])

    otp_record.is_used = True
    otp_record.save(update_fields=["is_used"])
    PasswordResetOTP.objects.filter(email__iexact=email, is_used=False).update(is_used=True)

    return JsonResponse({"message": "Password reset successfully."}, status=200)


@csrf_exempt
@require_POST
@employee_access_token_required
def create_department(request):
    name, logo, error = _extract_department_form_data(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    if Department.objects.filter(name__iexact=name).exists():
        return JsonResponse({"message": "Department with this name already exists."}, status=400)

    try:
        department = Department.objects.create(name=name, logo=logo)
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)
    except IntegrityError:
        return JsonResponse({"message": "Department with this name already exists."}, status=400)

    return JsonResponse(
        {
            "message": "Department created successfully.",
            "department": _department_to_dict(request, department),
        },
        status=201,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_departments(request):
    departments = Department.objects.all().order_by("id")
    data = [_department_to_dict(request, dep) for dep in departments]
    return JsonResponse({"departments": data}, status=200)


@csrf_exempt
@require_http_methods(["POST", "PUT", "PATCH"])
@employee_access_token_required
def update_department(request, department_id):
    department = Department.objects.filter(id=department_id).first()
    if not department:
        return JsonResponse({"message": "Department not found."}, status=404)

    name, logo, error = _extract_department_update_form_data(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    if name and Department.objects.filter(name__iexact=name).exclude(id=department.id).exists():
        return JsonResponse({"message": "Department with this name already exists."}, status=400)

    if name:
        department.name = name

    if logo:
        if department.logo:
            department.logo.delete(save=False)
        department.logo = logo

    try:
        department.save()
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)
    except IntegrityError:
        return JsonResponse({"message": "Department with this name already exists."}, status=400)

    return JsonResponse(
        {"message": "Department updated successfully.", "department": _department_to_dict(request, department)},
        status=200,
    )


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
@employee_access_token_required
def delete_department(request, department_id):

    department = Department.objects.filter(
        id=department_id
    ).first()

    if not department:
        return JsonResponse(
            {
                "message":
                "Department not found."
            },
            status=404,
        )

    # CHECK EMPLOYEES
    employees_count = User.objects.filter(
        user_type=User.UserType.EMPLOYEE,
        department=department,
    ).count()

    if employees_count > 0:

        return JsonResponse(
            {
                "message":
                "Cannot delete this department because employees are assigned to it.",

                "employees_count":
                employees_count,
            },
            status=409,
        )

    # CHECK REPORTS / INCIDENTS
    incidences_count = Incidence.objects.filter(
        department=department
    ).count()

    if incidences_count > 0:

        return JsonResponse(
            {
                "message":
                "Cannot delete this department because reports are linked to it.",

                "reports_count":
                incidences_count,
            },
            status=409,
        )

    # DELETE LOGO
    if department.logo:
        department.logo.delete(save=False)

    department.delete()

    return JsonResponse(
        {
            "message":
            "Department deleted successfully."
        },
        status=200,
    )
def calculate_user_trust_metrics(user):

    reports = Incidence.objects.filter(
        citizin=user
    )

    total_reports = reports.count()

    if total_reports == 0:
        return {
            "valid_ratio": 1,
            "duplicate_rate": 0,
            "fake_image_ratio": 0,
            "reports_last_30_days": 0,
            "avg_severity_reported": 0
        }

    duplicate_reports = reports.filter(
        duplicate=True
    ).count()

    fake_reports = reports.filter(
        image_authenticity__iexact="fake"
    ).count()

    reports_last_30_days = reports.filter(
        created_at__gte=django_timezone.now() - timedelta(days=30)
    ).count()

    valid_reports = (
        total_reports
        - duplicate_reports
        - fake_reports
    )

    valid_ratio = valid_reports / total_reports

    duplicate_rate = duplicate_reports / total_reports

    fake_image_ratio = fake_reports / total_reports

    return {
        "valid_ratio": round(valid_ratio, 4),
        "duplicate_rate": round(duplicate_rate, 4),
        "fake_image_ratio": round(fake_image_ratio, 4),
        "reports_last_30_days": reports_last_30_days,
        "avg_severity_reported": 0
    }
@csrf_exempt
@require_POST
@citizin_access_token_required
def create_citizin_incidence(request):

    data, error = _extract_citizin_incidence_form_data(request)

    if error:
        return JsonResponse({"message": error}, status=400)

    department = _resolve_department(data["department_value"])

    if not department:
        return JsonResponse({"message": "Department not found."}, status=400)

    # ==========================
    # Duplicate Detection AI
    # ==========================

    duplicate = False
    similarity = 0

    try:

        duplicate_result = check_duplicate(
            data["description"]
        )

        if duplicate_result:

            duplicate = duplicate_result.get(
                "duplicate",
                False
            )

            similarity = duplicate_result.get(
                "similarity",
                0
            )

    except Exception as e:

        print(
            "Duplicate Detection Error:",
            e
        )

    # ==========================
    # Image Authenticity AI
    # ==========================

    image_authenticity = None
    image_confidence = None

    try:

        image_result = check_image_authenticity(
            data["image_before_analysis"]
        )
        print("IMAGE RESULT =", image_result)

        if image_result:

            image_authenticity = image_result.get(
                "prediction"
            )

            image_confidence = image_result.get(
                "confidence"
            )

    except Exception as e:

        print(
            "Image Authenticity Error:",
            e
        )

    # ==========================
    # Road Damage Detection AI
    # ==========================

    road_prediction = None
    road_confidence = None

    try:
        data["image_before_analysis"].seek(0)
        road_result = detect_road_damage(
            data["image_before_analysis"]
        )
        print("ROAD RESULT =", road_result)

        if road_result:

            road_prediction = road_result.get(
                "prediction"
            )

            road_confidence = road_result.get(
                "confidence"
            )

    except Exception as e:

        print(
            "Road Detection Error:",
            e
        )

    # ==========================
    # Trust Model AI
    # ==========================

    trust_score = None
    trust_level = None

    try:

        trust_metrics = calculate_user_trust_metrics(
            request.citizin_user
        )

        trust_result = get_trust_score(
            trust_metrics["valid_ratio"],
            trust_metrics["duplicate_rate"],
            trust_metrics["fake_image_ratio"],
            trust_metrics["reports_last_30_days"],
            trust_metrics["avg_severity_reported"]
        )
        print("TRUST RESULT =", trust_result)

        if trust_result:

            trust_score = trust_result.get(
                "trust_score"
            )

            trust_level = trust_result.get(
                "trust_level"
            )

    except Exception as e:

        print(
            "Trust Model Error:",
            e
        )
         # ==========================
    # Severity Model AI
    # ==========================

    severity_prediction = None
    severity_score = None

    try:

        image_authenticity_score = (
            image_confidence
            if image_authenticity == "authentic"
            else 0
        )

        reports_nearby_1h = Incidence.objects.filter(
            location_name=data["location_name"],
            created_at__gte=django_timezone.now() - timedelta(hours=1)
        ).count()

        severity_result = get_severity(
            trust_score if trust_score else 0,
            0,
            image_authenticity_score,
            reports_nearby_1h,
            0
        )

        if severity_result:

            severity_prediction = severity_result.get(
                "severity_prediction"
            )

            severity_score = severity_result.get(
                "severity_score"
            )

    except Exception as e:

        print(
            "Severity Model Error:",
            e
        )
            # ==========================
    # Priority Model AI
    # ==========================

    priority_prediction = None
    priority_score = None

    try:

        area_load = Incidence.objects.filter(
            location_name=data["location_name"],
            status__in=[
                Incidence.Status.NEW,
                Incidence.Status.ASSIGNED,
                Incidence.Status.IN_PROGRESS
            ]
        ).count()

        priority_result = get_priority(
            severity_prediction if severity_prediction else "Medium",
            severity_score if severity_score else 0,
            area_load,
            1,      # available_teams
            1,      # team_skill_match
            1,      # historical_team_performance
            trust_score if trust_score else 0,
            reports_nearby_1h
        )

        if priority_result:

            priority_prediction = priority_result.get(
                "priority_prediction"
            )

            priority_score = priority_result.get(
                "confidence_score"
            )

    except Exception as e:

        print(
            "Priority Model Error:",
            e
        )

    DEPARTMENT_MAPPING = {
    "Road": [
        "Road_Damage",
        "Garbage",
        "Fallen_Tree"
    ],

    "Electricity": [
        "Electrical_Pole"
    ],

    "Gas": [
        "Fire"
    ]
}    
    # ==========================
    # AI Decision Layer
    # ==========================

    status = Incidence.Status.NEW
    forward_reason = None

    if image_authenticity == "spam":    

        status = Incidence.Status.FORWORDED
        forward_reason = "Spam Image"

    else:

        allowed_predictions = DEPARTMENT_MAPPING.get(
        department.name,
        []
    )

        if (
            road_prediction
            and
            allowed_predictions
            and
            road_prediction not in allowed_predictions
    ):
            status = Incidence.Status.FORWORDED
            forward_reason = "Department Mismatch"


    try:
        print("IMAGE =", image_authenticity)
        print("FINAL STATUS =", status)
        print("FORWARD REASON =", forward_reason)

        incidence = Incidence.objects.create(
            forward_reason=forward_reason,
            description=data["description"],
            latlatitude=data["latlatitude"],
            longitude=data["longitude"],
            location_name=data["location_name"],
            status=status,
            department=department,
            image_before_analysis=data["image_before_analysis"],
            citizin=request.citizin_user,

            duplicate=duplicate,
            duplicate_similarity=similarity,

            image_authenticity=image_authenticity,
            image_confidence=image_confidence,

            road_prediction=road_prediction,
            road_confidence=road_confidence,

            trust_score=trust_score,
            trust_level=trust_level,

            severity_prediction=severity_prediction,
            severity_score=severity_score,
            priority_prediction=priority_prediction,
            priority_score=priority_score,
        )
        print("SAVED STATUS =", incidence.status)
        print("SAVED REASON =", incidence.forward_reason)
        if trust_score is not None:

            request.citizin_user.trust_score = trust_score

        if trust_level is not None:

            request.citizin_user.trust_level = trust_level

        request.citizin_user.save(
            update_fields=[
                "trust_score",
                "trust_level"
            ]
        )

    except ValidationError as exc:

        if hasattr(exc, "message_dict"):
            return JsonResponse(
                {"errors": exc.message_dict},
                status=400
            )

        return JsonResponse(
            {"errors": exc.messages},
            status=400
        )

    except IntegrityError:

        return JsonResponse(
            {
                "message":
                "Failed to create incidence due to data conflict."
            },
            status=400
        )

    return JsonResponse(
        {
            "message": "Incidence created successfully.",

            "AI_Result": {

                "duplicate": duplicate,
                "similarity": similarity,

                "image_authenticity":
                    image_authenticity,

                "image_confidence":
                    image_confidence,

                "road_prediction":
                    road_prediction,

                "forward_reason":
                  forward_reason,    

                "road_confidence":
                    road_confidence,

                "trust_score":
                    trust_score,

                "trust_level":
                    trust_level,
                "severity_prediction":
                    severity_prediction,

                "severity_score":
                    severity_score,
                
                "priority_prediction":
                    priority_prediction,

                "priority_score":
                    priority_score
            },

            "incidence": _incidence_to_dict(
                request,
                incidence
            ),
        },
        status=201,
    )

@csrf_exempt
@require_POST
@employee_access_token_required
def assign_incidence_to_employee(request):
    data, error = _extract_incidence_assignment_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    employee = getattr(request, "employee_user", None)
    if not employee:
        return JsonResponse({"message": "Employee from token not found."}, status=401)

    # CHECK ACTIVE INCIDENCE
    active_incidence = Incidence.objects.filter(
        assigned_employee=employee,
        status__in=[
            Incidence.Status.ASSIGNED,
            Incidence.Status.IN_PROGRESS,
        ]
    ).exists()

    if active_incidence:
        return JsonResponse(
            {
                "message": "You already have an active incidence assigned."
            },
            status=400,
        )


    incidence = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(id=data["incidence_id"])
        .first()
    )
    if not incidence:
        return JsonResponse({"message": "Incidence not found."}, status=404)

    incidence.status = Incidence.Status.ASSIGNED
    incidence.assigned_employee = employee

    try:
        incidence.save(update_fields=["status", "assigned_employee"])
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)

    incidence.refresh_from_db()
    return JsonResponse(
        {
            "message": "Incidence assigned successfully.",
            "incidence": _incidence_to_dict(request, incidence),
        },
        status=200,
    )


@csrf_exempt
@require_POST
@employee_access_token_required
def move_incidence_to_completed(request):
    data, error = _extract_incidence_assignment_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    employee = getattr(request, "employee_user", None)
    if not employee:
        return JsonResponse({"message": "Employee from token not found."}, status=401)

    if not _can_complete_incidence(employee):
        return JsonResponse(
            {"message": "Only admin or supervisior can move incidence to Completed."},
            status=403,
        )

    incidence = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(id=data["incidence_id"])
        .first()
    )
    if not incidence:
        return JsonResponse({"message": "Incidence not found."}, status=404)

    incidence.status = Incidence.Status.FINISHED

    try:
        incidence.save(update_fields=["status", "completed_at"])
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)

    incidence.refresh_from_db()
    return JsonResponse(
        {
            "message": "Incidence moved to Completed successfully.",
            "incidence": _incidence_to_dict(request, incidence),
        },
        status=200,
    )


@csrf_exempt
@require_POST
@employee_access_token_required
def notify_department_region_operators(request):
    data, error = _extract_incidence_assignment_payload(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    employee = getattr(request, "employee_user", None)
    if not employee:
        return JsonResponse({"message": "Employee from token not found."}, status=401)

    if not employee.department_id:
        return JsonResponse({"message": "Employee has no department assigned."}, status=400)

    if not employee.region or not str(employee.region).strip():
        return JsonResponse({"message": "Employee has no region assigned."}, status=400)

    incidence = Incidence.objects.select_related("department").filter(id=data["incidence_id"]).first()
    if not incidence:
        return JsonResponse({"message": "Incidence not found."}, status=404)

    if incidence.department_id and incidence.department_id != employee.department_id:
        return JsonResponse(
            {"message": "Incidence belongs to a different department than the logged-in employee."},
            status=403,
        )

    region_value = str(employee.region).strip()
    operators = list(
        User.objects.filter(
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department_id=employee.department_id,
            region__iexact=region_value,
        )
        .exclude(id=employee.id)
        .order_by("id")
    )

    notification_data = {
        "Location": incidence.location_name,
        "Lat": str(incidence.latlatitude),
        "Long": str(incidence.longitude),
        "Employee_Name": employee.name,
        "Priority": incidence.priority,
        "Incidence_id": incidence.id,
        "Department": employee.department.name,
        "Employee_Email": employee.email,
    }

    notifications = [
        OperatorNotification(
            operator=operator,
            sender_employee=employee,
            incidence=incidence,
            location_name=incidence.location_name,
            latlatitude=incidence.latlatitude,
            longitude=incidence.longitude,
            priority=incidence.priority,
            department_name=employee.department.name,
            employee_name=employee.name,
            employee_email=employee.email,
        )
        for operator in operators
    ]
    if notifications:
        OperatorNotification.objects.bulk_create(notifications)

    return JsonResponse(
        {
            "message": "Notifications sent successfully.",
            "Incidence_id": incidence.id,
            "Department": {"id": employee.department_id, "name": employee.department.name},
            "Region": region_value,
            "Recipients_Count": len(operators),
            "Recipients": [
                {"id": operator.id, "Name": operator.name, "Email": operator.email}
                for operator in operators
            ],
            "Notification_Data": notification_data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["PATCH", "PUT", "POST"])
@employee_access_token_required
def move_incidence_to_in_progress(request, incidence_id):
    update_location_data = None
    if request.method in ["PATCH", "PUT"]:
        update_location_data, error = _extract_incidence_in_progress_update_payload(request)
        if error:
            return JsonResponse({"message": error}, status=400)

    employee = getattr(request, "employee_user", None)
    if not employee:
        return JsonResponse({"message": "Employee from token not found."}, status=401)

    incidence = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(id=incidence_id)
        .first()
    )
    if not incidence:
        return JsonResponse({"message": "Incidence not found."}, status=404)

    if incidence.status != Incidence.Status.ASSIGNED:
        return JsonResponse(
            {"message": "Incidence status must be 'Assigned' to move it to 'In_Progress'."},
            status=400,
        )

    if not incidence.assigned_employee_id:
        return JsonResponse({"message": "Incidence is not assigned to any employee."}, status=400)

    if incidence.assigned_employee_id != employee.id:
        return JsonResponse(
            {"message": "You can only move incidences assigned to your account."},
            status=403,
        )

    update_fields = ["status"]
    if update_location_data:
        incidence.latlatitude = update_location_data["latlatitude"]
        incidence.longitude = update_location_data["longitude"]
        incidence.location_name = update_location_data["location_name"]
        update_fields.extend(["latlatitude", "longitude", "location_name"])

    incidence.status = Incidence.Status.IN_PROGRESS

    try:
        incidence.save(update_fields=update_fields)
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)

    incidence.refresh_from_db()
    message = "Incidence moved to In_Progress successfully."
    if update_location_data:
        message = "Incidence updated and moved to In_Progress successfully."

    return JsonResponse(
        {
            "message": message,
            "incidence": _incidence_to_dict(request, incidence),
        },
        status=200,
    )

@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_operator_notifications(request):

    employee = getattr(request, "employee_user", None)

    if not employee:
        return JsonResponse(
            {"message": "Employee from token not found."},
            status=401,
        )

    notifications = (
        OperatorNotification.objects
        .filter(operator=employee)
        .select_related("incidence")
        .order_by("-created_at")
    )

    data = []

    for notification in notifications:
        data.append({
            "id": notification.id,

            "name": notification.employee_name,

            "email": notification.employee_email,

            "subject": (
                f"{notification.department_name} Incident"
            ),

            "message": (
                f"{notification.location_name} | "
                f"Priority: {notification.priority}"
            ),

            "priority": (
                notification.priority.lower()
                if notification.priority
                else "low"
            ),

            "report_id": notification.incidence_id,

            "read": notification.is_read,

            "created_at": (
                notification.created_at.isoformat()
                if notification.created_at
                else None
            ),
        })

    return JsonResponse(data, safe=False, status=200)


@csrf_exempt
@require_http_methods(["PATCH"])
@employee_access_token_required
def mark_notification_as_read(request, notification_id):

    employee = getattr(request, "employee_user", None)

    if not employee:
        return JsonResponse(
            {"message": "Employee from token not found."},
            status=401,
        )

    notification = (
        OperatorNotification.objects
        .filter(
            id=notification_id,
            operator=employee,
        )
        .first()
    )

    if not notification:
        return JsonResponse(
            {"message": "Notification not found."},
            status=404,
        )

    notification.is_read = True
    notification.save(update_fields=["is_read"])

    return JsonResponse(
        {
            "message": "Notification marked as read successfully.",
            "Notification_Id": notification.id,
            "Is_Read": notification.is_read,
        },
        status=200,
    )


@csrf_exempt
@require_POST
@employee_access_token_required
def move_incidence_to_review(request, incidence_id):
    data, error = _extract_incidence_review_form_data(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    employee = getattr(request, "employee_user", None)
    if not employee:
        return JsonResponse({"message": "Employee from token not found."}, status=401)

    incidence = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(id=incidence_id)
        .first()
    )
    if not incidence:
        return JsonResponse({"message": "Incidence not found."}, status=404)

    if incidence.status != Incidence.Status.IN_PROGRESS:
        return JsonResponse(
            {"message": "Incidence status must be 'In_Progress' to move it to 'Review'."},
            status=400,
        )

    if not incidence.assigned_employee_id:
        return JsonResponse({"message": "Incidence is not assigned to any employee."}, status=400)

    if incidence.assigned_employee_id != employee.id:
        return JsonResponse(
            {"message": "You can only update incidences assigned to your account."},
            status=403,
        )

    incidence.image_after_analysis = data["image_after_analysis"]
    incidence.what_was_done = data["what_was_done"]
    incidence.status = Incidence.Status.REVIEW

    try:
        incidence.save(update_fields=["image_after_analysis", "what_was_done", "status"])
    except ValidationError as exc:
        if hasattr(exc, "message_dict"):
            return JsonResponse({"errors": exc.message_dict}, status=400)
        return JsonResponse({"errors": exc.messages}, status=400)

    incidence.refresh_from_db()
    return JsonResponse(
        {
            "message": "Incidence moved to Review successfully.",
            "incidence": _incidence_to_dict(request, incidence),
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_incidences(request):
    filters, error = _extract_incidence_list_filters(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .all()
        .order_by("-id")
    )
    if "department_id" in filters:
        incidences = incidences.filter(department_id=filters["department_id"])
    if "created_at_date" in filters:
        incidences = incidences.filter(created_at__date=filters["created_at_date"])
    if "status" in filters:
        incidences = incidences.filter(status=filters["status"])
    if "id" in filters:
        incidences = incidences.filter(id=filters["id"])

    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse({"incidences": data}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def get_new_incidences(request):
    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(status=Incidence.Status.NEW)
        .order_by("-id")
    )
    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse(
        {
            "Status": Incidence.Status.NEW,
            "Total_New_Incidences": len(data),
            "incidences": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_assigned_incidences(request):
    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(status=Incidence.Status.ASSIGNED)
        .order_by("-id")
    )
    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse(
        {
            "Status": Incidence.Status.ASSIGNED,
            "Total_Assigned_Incidences": len(data),
            "incidences": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_review_incidences(request):
    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(status=Incidence.Status.REVIEW)
        .order_by("-id")
    )
    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse(
        {
            "Status": Incidence.Status.REVIEW,
            "Total_Review_Incidences": len(data),
            "incidences": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_in_progress_incidences(request):
    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(status=Incidence.Status.IN_PROGRESS)
        .order_by("-id")
    )
    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse(
        {
            "Status": Incidence.Status.IN_PROGRESS,
            "Total_In_Progress_Incidences": len(data),
            "incidences": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_forworded_incidences(request):
    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(status__in=FORWORDED_INCIDENCE_STATUSES)
        .order_by("-id")
    )
    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse(
        {
            "Status": Incidence.Status.FORWORDED,
            "Total_Forworded_Incidences": len(data),
            "incidences": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_completed_incidences(request):
    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(status__in=COMPLETED_INCIDENCE_STATUSES)
        .order_by("-id")
    )
    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse(
        {
            "Status": "Completed",
            "Total_Completed_Incidences": len(data),
            "incidences": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@citizin_access_token_required
def get_citizin_incidences(request):
    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(citizin_id=request.citizin_user.id)
        .order_by("-id")
    )
    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse(
        {
            "Citizin": {"id": request.citizin_user.id, "Name": request.citizin_user.name},
            "Total_Incidences": len(data),
            "incidences": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@citizin_access_token_required
def get_citizin_incidence_by_id(request, incidence_id):
    incidence = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(id=incidence_id, citizin_id=request.citizin_user.id)
        .first()
    )
    if not incidence:
        return JsonResponse({"message": "Incidence not found for this citizin."}, status=404)

    return JsonResponse({"incidence": _incidence_to_dict(request, incidence)}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def get_incidence_status_by_id(request, incidence_id):
    incidence = Incidence.objects.filter(id=incidence_id).first()
    if not incidence:
        return JsonResponse({"message": "Incidence not found."}, status=404)

    return JsonResponse(
        {
            "Incidence_id": incidence.id,
            "Created_At": incidence.created_at.isoformat() if incidence.created_at else None,
            "Status": incidence.status,
            "Lat": str(incidence.latlatitude),
            "Long": str(incidence.longitude),
            "Location_Name": incidence.location_name,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
def get_incidence_by_id(request, incidence_id):
    incidence = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(id=incidence_id)
        .first()
    )
    if not incidence:
        return JsonResponse({"message": "Incidence not found."}, status=404)

    return JsonResponse({"incidence": _incidence_to_dict(request, incidence)}, status=200)