from datetime import datetime, timedelta

from django.db.models import Count, OuterRef, Subquery
from django.db.models.functions import TruncDate, TruncMonth, TruncWeek
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from users.models import Incidence
from users.views import _incidence_to_dict, employee_access_token_required

COMPLETED_STATUSES = (Incidence.Status.FINISHED, "Completed")
IN_WORK_STATUSES = (
    Incidence.Status.REVIEW,
    Incidence.Status.IN_PROGRESS,
    Incidence.Status.ASSIGNED,
    Incidence.Status.FORWORDED,
    "Forwarded",
)
ASSIGNED_IN_PROGRESS_STATUSES = (
    Incidence.Status.ASSIGNED,
    Incidence.Status.IN_PROGRESS,
)
IN_REVIEW_STATUSES = (
    Incidence.Status.REVIEW,
    "In_Review",
)
FORWARDED_STATUSES = (
    Incidence.Status.FORWORDED,
    "Forwarded",
)


def _extract_status_date_range(request):
    start_date_value = request.GET.get("Start_Date") or request.GET.get("start_date")
    end_date_value = request.GET.get("End_Date") or request.GET.get("end_date")

    if not start_date_value or not end_date_value:
        return None, None, "Start_Date and End_Date are required in YYYY-MM-DD format."

    try:
        start_date = datetime.strptime(str(start_date_value).strip(), "%Y-%m-%d").date()
    except ValueError:
        return None, None, "Start_Date must be in YYYY-MM-DD format."

    try:
        end_date = datetime.strptime(str(end_date_value).strip(), "%Y-%m-%d").date()
    except ValueError:
        return None, None, "End_Date must be in YYYY-MM-DD format."

    if start_date > end_date:
        return None, None, "Start_Date cannot be after End_Date."

    return start_date, end_date, None


def _coerce_period_to_date(period_value):
    if hasattr(period_value, "date"):
        return period_value.date()
    return period_value


def _format_duration_from_seconds(total_seconds):
    if total_seconds is None:
        return None

    total_seconds = max(int(total_seconds), 0)
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{days}d {hours}h {minutes}m {seconds}s"


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_home_dashboard(request):
    today = timezone.localdate()

    carryover_qs = (
        Incidence.objects.exclude(status__in=COMPLETED_STATUSES).filter(dashboard_date__lt=today)
    )
    carried_from_previous_days = carryover_qs.count()
    if carried_from_previous_days:
        carryover_qs.update(dashboard_date=today)

    today_incidences = Incidence.objects.filter(dashboard_date=today)

    total_incidences = today_incidences.count()
    new_incidences = today_incidences.filter(status=Incidence.Status.NEW).count()
    in_work_incidences = today_incidences.filter(status__in=IN_WORK_STATUSES).count()
    completed_incidences = today_incidences.filter(status__in=COMPLETED_STATUSES).count()

    return JsonResponse(
        {
            "Employee_Name": request.employee_user.name,
            "Date": str(today),
            "Total_Incidences": total_incidences,
            "New_Incidences": new_incidences,
            "In_Work_Incidences": in_work_incidences,
            "Completed_Incidences": completed_incidences,
            "Carried_From_Previous_Days": carried_from_previous_days,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_department_new_incidences(request):
    employee = request.employee_user
    if not employee.department_id:
        return JsonResponse({"message": "Employee has no department assigned."}, status=400)

    incidences = (
        Incidence.objects.select_related("citizin", "department", "assigned_employee")
        .filter(
            department_id=employee.department_id,
            status=Incidence.Status.NEW,
        )
        .order_by("-id")
    )

    data = [_incidence_to_dict(request, incidence) for incidence in incidences]
    return JsonResponse(
        {
            "Department": {"id": employee.department_id, "name": employee.department.name},
            "Total_New_Incidences": len(data),
            "incidences": data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_employee_completed_and_current_incidences(request):
    employee = request.employee_user

    employee_incidences = Incidence.objects.select_related("citizin", "department", "assigned_employee").filter(
        assigned_employee_id=employee.id
    )
    completed_qs = employee_incidences.filter(status__in=COMPLETED_STATUSES).order_by("-id")
    current_qs = employee_incidences.exclude(status__in=COMPLETED_STATUSES).order_by("-id")

    completed_data = [_incidence_to_dict(request, incidence) for incidence in completed_qs]
    current_data = [_incidence_to_dict(request, incidence) for incidence in current_qs]

    return JsonResponse(
        {
            "Employee": {"id": employee.id, "Name": employee.name},
            "Total_Completed_Incidences": len(completed_data),
            "Total_Current_Incidences": len(current_data),
            "Completed_Incidences": completed_data,
            "Current_Incidences": current_data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_incidences_status_overview(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1, day=1)
    else:
        next_month_start = month_start.replace(month=month_start.month + 1, day=1)

    monthly_incidences = Incidence.objects.filter(
        dashboard_date__gte=month_start,
        dashboard_date__lt=next_month_start,
    )

    total_incidences = monthly_incidences.count()
    assigned_in_progress_count = monthly_incidences.filter(
        status__in=ASSIGNED_IN_PROGRESS_STATUSES
    ).count()
    in_review_count = monthly_incidences.filter(status__in=IN_REVIEW_STATUSES).count()
    forwarded_count = monthly_incidences.filter(status__in=FORWARDED_STATUSES).count()
    completed_this_month_count = monthly_incidences.filter(
        status__in=COMPLETED_STATUSES,
    ).count()

    return JsonResponse(
        {
            "Date": str(today),
            "Month_Start": str(month_start),
            "Month_End": str(next_month_start - timedelta(days=1)),
            "Total_Incidences": total_incidences,
            "Assigned_And_In_Progress_Incidences": assigned_in_progress_count,
            "In_Review_Incidences": in_review_count,
            "Forwarded_Incidences": forwarded_count,
            "Completed_This_Month_Incidences": completed_this_month_count,
            "Completed_Today_Incidences": completed_this_month_count,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_incidences_status_summary_by_date_range(request):
    start_date, end_date, error = _extract_status_date_range(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    filtered_incidences = Incidence.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
    )

    total_incidences = filtered_incidences.count()
    assigned_and_in_progress_count = filtered_incidences.filter(
        status__in=ASSIGNED_IN_PROGRESS_STATUSES
    ).count()
    review_count = filtered_incidences.filter(status__in=IN_REVIEW_STATUSES).count()
    forworded_count = filtered_incidences.filter(status__in=FORWARDED_STATUSES).count()
    completed_count = filtered_incidences.filter(status__in=COMPLETED_STATUSES).count()

    return JsonResponse(
        {
            "Start_Date": str(start_date),
            "End_Date": str(end_date),
            "Total_Incidences": total_incidences,
            "Assigned_And_In_Progress_Incidences": assigned_and_in_progress_count,
            "Review_Incidences": review_count,
            "Forworded_Incidences": forworded_count,
            "Completed_Incidences": completed_count,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_department_incidences_summary_by_date_range(request):
    start_date, end_date, error = _extract_status_date_range(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    filtered_incidences = Incidence.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
    )
    total_incidences = filtered_incidences.count()

    department_counts_qs = (
        filtered_incidences.values("department_id", "department__name")
        .annotate(total=Count("id"))
        .order_by("-total", "department__name")
    )

    departments_data = [
        {
            "Department_Id": row["department_id"],
            "Department_Name": row["department__name"] or "No Department",
            "Incidences_Count": row["total"],
        }
        for row in department_counts_qs
    ]

    return JsonResponse(
        {
            "Start_Date": str(start_date),
            "End_Date": str(end_date),
            "Total_Incidences": total_incidences,
            "Departments_Count": len(departments_data),
            "Departments": departments_data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_incidences_heatmap_data(request):
    total_incidences = Incidence.objects.count()
    heatmap_points_qs = (
        Incidence.objects.values("location_name", "latlatitude", "longitude")
        .annotate(total=Count("id"))
        .order_by("-total", "location_name")
    )

    heatmap_data = [
        {
            "Location_Name": row["location_name"],
            "Latlatitude": float(row["latlatitude"]),
            "Longitude": float(row["longitude"]),
            "Incidences_Count": row["total"],
        }
        for row in heatmap_points_qs
    ]

    return JsonResponse(
        {
            "Total_Incidences": total_incidences,
            "Total_Locations": len(heatmap_data),
            "Heatmap_Data": heatmap_data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def search_location_incidences_analysis(request):
    location_name_value = request.GET.get("Location_Name") or request.GET.get("location_name")
    if location_name_value in [None, ""]:
        return JsonResponse({"message": "Location_Name is required."}, status=400)

    location_name = str(location_name_value).strip()
    if not location_name:
        return JsonResponse({"message": "Location_Name is required."}, status=400)

    incidences = (
        Incidence.objects.select_related("department")
        .filter(location_name__iexact=location_name)
        .order_by("-created_at", "-id")
    )

    incidences_data = []
    solved_durations_seconds = []
    for incidence in incidences:
        solve_duration_seconds = None
        solve_duration_human = None

        if (
            incidence.status == Incidence.Status.FINISHED
            and incidence.created_at
            and incidence.completed_at
            and incidence.completed_at >= incidence.created_at
        ):
            solve_duration_seconds = int((incidence.completed_at - incidence.created_at).total_seconds())
            solve_duration_human = _format_duration_from_seconds(solve_duration_seconds)
            solved_durations_seconds.append(solve_duration_seconds)

        incidences_data.append(
            {
                "Incidence_Number": incidence.id,
                "Date": incidence.created_at.isoformat() if incidence.created_at else None,
                "Status": incidence.status,
                "Lat": str(incidence.latlatitude),
                "Long": str(incidence.longitude),
                "Department": (
                    {"id": incidence.department_id, "name": incidence.department.name}
                    if incidence.department
                    else None
                ),
                "Solve_Duration_Seconds": solve_duration_seconds,
                "Solve_Duration": solve_duration_human,
            }
        )

    average_solve_seconds = None
    average_solve_duration = None
    if solved_durations_seconds:
        average_solve_seconds = int(sum(solved_durations_seconds) / len(solved_durations_seconds))
        average_solve_duration = _format_duration_from_seconds(average_solve_seconds)

    department_mode_row = (
        incidences.exclude(department__isnull=True)
        .values("department_id", "department__name")
        .annotate(total=Count("id"))
        .order_by("-total", "department__name")
        .first()
    )
    most_frequent_department = None
    if department_mode_row:
        most_frequent_department = {
            "id": department_mode_row["department_id"],
            "name": department_mode_row["department__name"],
            "Incidences_Count": department_mode_row["total"],
        }

    return JsonResponse(
        {
            "Location_Name": location_name,
            "Total_Incidences_On_Street": len(incidences_data),
            "Solved_Incidences_Count": len(solved_durations_seconds),
            "Average_Solve_Duration_Seconds": average_solve_seconds,
            "Average_Solve_Duration": average_solve_duration,
            "Most_Frequent_Department": most_frequent_department,
            "incidences": incidences_data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_incidences_time_counts_by_date_range(request):
    start_date, end_date, error = _extract_status_date_range(request)
    if error:
        return JsonResponse({"message": error}, status=400)

    filtered_incidences = Incidence.objects.filter(
        created_at__date__gte=start_date,
        created_at__date__lte=end_date,
    )
    total_incidences = filtered_incidences.count()

    daily_counts_qs = (
        filtered_incidences.annotate(period=TruncDate("created_at"))
        .values("period")
        .annotate(total=Count("id"))
    )
    daily_counts_map = {row["period"]: row["total"] for row in daily_counts_qs}

    daily_data = []
    current_day = start_date
    while current_day <= end_date:
        daily_data.append(
            {
                "Date": str(current_day),
                "Incidences_Count": daily_counts_map.get(current_day, 0),
            }
        )
        current_day += timedelta(days=1)

    weekly_counts_qs = (
        filtered_incidences.annotate(period=TruncWeek("created_at"))
        .values("period")
        .annotate(total=Count("id"))
    )
    weekly_counts_map = {
        _coerce_period_to_date(row["period"]): row["total"] for row in weekly_counts_qs
    }

    weekly_data = []
    current_week_start = start_date - timedelta(days=start_date.weekday())
    while current_week_start <= end_date:
        week_end = min(current_week_start + timedelta(days=6), end_date)
        weekly_data.append(
            {
                "Week_Start": str(current_week_start),
                "Week_End": str(week_end),
                "Incidences_Count": weekly_counts_map.get(current_week_start, 0),
            }
        )
        current_week_start += timedelta(days=7)

    monthly_counts_qs = (
        filtered_incidences.annotate(period=TruncMonth("created_at"))
        .values("period")
        .annotate(total=Count("id"))
    )
    monthly_counts_map = {
        _coerce_period_to_date(row["period"]): row["total"] for row in monthly_counts_qs
    }

    monthly_data = []
    current_month_start = start_date.replace(day=1)
    while current_month_start <= end_date:
        if current_month_start.month == 12:
            next_month_start = current_month_start.replace(year=current_month_start.year + 1, month=1, day=1)
        else:
            next_month_start = current_month_start.replace(month=current_month_start.month + 1, day=1)
        month_end = min(next_month_start - timedelta(days=1), end_date)
        monthly_data.append(
            {
                "Month_Start": str(current_month_start),
                "Month_End": str(month_end),
                "Month": current_month_start.strftime("%B"),
                "Year": current_month_start.year,
                "Incidences_Count": monthly_counts_map.get(current_month_start, 0),
            }
        )
        current_month_start = next_month_start

    return JsonResponse(
        {
            "Start_Date": str(start_date),
            "End_Date": str(end_date),
            "Total_Incidences": total_incidences,
            "Daily_Counts": daily_data,
            "Weekly_Counts": weekly_data,
            "Monthly_Counts": monthly_data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_weekly_incidences_chart_data(request):
    today = timezone.localdate()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    weekly_counts_qs = (
        Incidence.objects.filter(created_at__date__gte=week_start, created_at__date__lte=week_end)
        .values("created_at__date")
        .annotate(total=Count("id"))
    )
    counts_by_day = {row["created_at__date"]: row["total"] for row in weekly_counts_qs}

    chart_data = []
    for offset in range(7):
        day = week_start + timedelta(days=offset)
        chart_data.append(
            {
                "Date": str(day),
                "Day": day.strftime("%A"),
                "Month": day.strftime("%B"),
                "Incidences_Count": counts_by_day.get(day, 0),
            }
        )

    return JsonResponse(
        {
            "Date": str(today),
            "Week_Start": str(week_start),
            "Week_End": str(week_end),
            "Total_Incidences_This_Week": sum(item["Incidences_Count"] for item in chart_data),
            "Chart_Data": chart_data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_monthly_department_incidences_chart_data(request):
    today = timezone.localdate()
    month_start = today.replace(day=1)
    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1, day=1)
    else:
        next_month_start = month_start.replace(month=month_start.month + 1, day=1)
    month_end = next_month_start - timedelta(days=1)

    monthly_incidences = Incidence.objects.filter(
        created_at__date__gte=month_start,
        created_at__date__lt=next_month_start,
    )
    total_incidences = monthly_incidences.count()

    department_counts_qs = (
        monthly_incidences.values("department_id", "department__name")
        .annotate(total=Count("id"))
        .order_by("-total", "department__name")
    )
    chart_data = [
        {
            "Department_Id": row["department_id"],
            "Department_Name": row["department__name"] or "No Department",
            "Incidences_Count": row["total"],
        }
        for row in department_counts_qs
    ]

    return JsonResponse(
        {
            "Date": str(today),
            "Month_Start": str(month_start),
            "Month_End": str(month_end),
            "Month": month_start.strftime("%B"),
            "Total_Incidences_This_Month": total_incidences,
            "Departments_Count": len(chart_data),
            "Chart_Data": chart_data,
        },
        status=200,
    )


@csrf_exempt
@require_http_methods(["GET"])
@employee_access_token_required
def get_latest_incidence_per_department(request):
    latest_incidence_id_subquery = (
        Incidence.objects.filter(department_id=OuterRef("department_id"))
        .order_by("-created_at", "-id")
        .values("id")[:1]
    )

    latest_incidences = (
        Incidence.objects.select_related("department")
        .filter(
            department__isnull=False,
            id=Subquery(latest_incidence_id_subquery),
        )
        .order_by("department__name", "department_id")
    )

    data = [
        {
            "Incidence_Number": incidence.id,
            "Date": incidence.created_at.isoformat() if incidence.created_at else None,
            "Status": incidence.status,
            "Department": {
                "id": incidence.department_id,
                "name": incidence.department.name,
            },
        }
        for incidence in latest_incidences
    ]

    return JsonResponse(
        {
            "Total_Departments": len(data),
            "Latest_Incidences": data,
        },
        status=200,
    )
