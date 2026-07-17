from django.urls import path

from .views import (
    
    get_department_incidences_summary_by_date_range,
    get_department_new_incidences,
    get_employee_completed_and_current_incidences,
    get_home_dashboard,
    get_incidences_heatmap_data,
    search_location_incidences_analysis,
    get_incidences_time_counts_by_date_range,
    get_incidences_status_summary_by_date_range,
    get_incidences_status_overview,
    get_latest_incidence_per_department,
    get_monthly_department_incidences_chart_data,
    get_weekly_incidences_chart_data,
)

urlpatterns = [
    
    path("dashboard/", get_home_dashboard, name="home-dashboard"),
    path("incidence/status-overview/", get_incidences_status_overview, name="incidences-status-overview"),
    path("incidence/heatmap/", get_incidences_heatmap_data, name="incidences-heatmap"),
    path(
        "incidence/location-analysis/",
        search_location_incidences_analysis,
        name="incidence-location-analysis",
    ),
    path(
        "incidence/time-counts-by-date/",
        get_incidences_time_counts_by_date_range,
        name="incidences-time-counts-by-date",
    ),
    path(
        "incidence/department-summary-by-date/",
        get_department_incidences_summary_by_date_range,
        name="department-incidences-summary-by-date",
    ),
    path(
        "incidence/status-summary-by-date/",
        get_incidences_status_summary_by_date_range,
        name="incidences-status-summary-by-date",
    ),
    path("incidence/weekly-chart/", get_weekly_incidences_chart_data, name="weekly-incidences-chart"),
    path(
        "incidence/monthly-department-chart/",
        get_monthly_department_incidences_chart_data,
        name="monthly-department-incidences-chart",
    ),
    path(
        "incidence/latest-per-department/",
        get_latest_incidence_per_department,
        name="latest-incidence-per-department",
    ),
    path("incidence/new/", get_department_new_incidences, name="department-new-incidences"),
    path(
        "incidence/employee/",
        get_employee_completed_and_current_incidences,
        name="employee-completed-current-incidences",
    ),
]
