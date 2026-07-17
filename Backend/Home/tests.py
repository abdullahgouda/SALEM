from datetime import datetime, time, timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from users.models import Department, Incidence, User
from users.views import _build_token


class HomeDashboardAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Operations")
        self.other_department = Department.objects.create(name="Water")
        self.employee = User.objects.create(
            name="Dashboard Employee",
            national_id="12345678901234",
            phone_number="01000000001",
            email="employee@example.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.department,
            region="Cairo",
        )
        self.citizin = User.objects.create(
            name="Citizin User",
            national_id="12345678901235",
            phone_number="01000000002",
            email="citizin@example.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="1999-01-01",
            username="citizin_user",
        )
        self.access_token = _build_token(self.employee, "access", timedelta(minutes=15))

    def _image(self, file_name):
        return SimpleUploadedFile(file_name, b"fake-image-bytes", content_type="image/jpeg")

    def _create_incidence(
        self,
        status,
        dashboard_date,
        image_name,
        department=None,
        assigned_employee=None,
        created_at_date=None,
        location_name="Test Location",
        latlatitude="30.0000000",
        longitude="31.0000000",
    ):
        if department is None:
            department = self.department

        incidence_data = {
            "description": "Incidence test",
            "latlatitude": latlatitude,
            "longitude": longitude,
            "location_name": location_name,
            "status": status,
            "dashboard_date": dashboard_date,
            "department": department,
            "image_before_analysis": self._image(image_name),
            "citizin": self.citizin,
            "assigned_employee": assigned_employee,
        }
        if created_at_date:
            incidence_data["created_at"] = timezone.make_aware(datetime.combine(created_at_date, time(12, 0, 0)))

        return Incidence.objects.create(
            **incidence_data,
        )

    def test_home_dashboard_counts_and_carryover(self):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)

        carry_new = self._create_incidence(Incidence.Status.NEW, yesterday, "carry-new.jpg")
        carry_review = self._create_incidence(Incidence.Status.REVIEW, yesterday, "carry-review.jpg")
        old_completed = self._create_incidence(Incidence.Status.FINISHED, yesterday, "old-completed.jpg")
        self._create_incidence(Incidence.Status.NEW, today, "today-new.jpg")
        self._create_incidence(Incidence.Status.ASSIGNED, today, "today-assigned.jpg")
        self._create_incidence(Incidence.Status.FINISHED, today, "today-completed.jpg")

        response = self.client.get(
            "/api/home/dashboard/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Employee_Name"], self.employee.name)
        self.assertEqual(payload["Date"], str(today))
        self.assertEqual(payload["Carried_From_Previous_Days"], 2)
        self.assertEqual(payload["Total_Incidences"], 5)
        self.assertEqual(payload["New_Incidences"], 2)
        self.assertEqual(payload["In_Work_Incidences"], 2)
        self.assertEqual(payload["Completed_Incidences"], 1)

        carry_new.refresh_from_db()
        carry_review.refresh_from_db()
        old_completed.refresh_from_db()

        self.assertEqual(carry_new.dashboard_date, today)
        self.assertEqual(carry_review.dashboard_date, today)
        self.assertEqual(old_completed.dashboard_date, yesterday)

    def test_get_department_new_incidences_filters_by_employee_department(self):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)

        include_today = self._create_incidence(Incidence.Status.NEW, today, "include-today.jpg")
        include_yesterday = self._create_incidence(Incidence.Status.NEW, yesterday, "include-yesterday.jpg")
        self._create_incidence(Incidence.Status.REVIEW, today, "exclude-status.jpg")
        self._create_incidence(
            Incidence.Status.NEW,
            today,
            "exclude-department.jpg",
            department=self.other_department,
        )

        response = self.client.get(
            "/api/home/incidence/new/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Department"]["id"], self.department.id)
        self.assertEqual(payload["Department"]["name"], self.department.name)
        self.assertEqual(payload["Total_New_Incidences"], 2)

        returned_ids = [item["id"] for item in payload["incidences"]]
        self.assertEqual(returned_ids, [include_yesterday.id, include_today.id])
        self.assertTrue(all(item.get("Created_At") for item in payload["incidences"]))

    def test_get_employee_completed_and_current_incidences(self):
        today = timezone.localdate()

        completed_1 = self._create_incidence(
            Incidence.Status.FINISHED,
            today,
            "emp-completed-1.jpg",
            assigned_employee=self.employee,
        )
        current_1 = self._create_incidence(
            Incidence.Status.IN_PROGRESS,
            today,
            "emp-current-1.jpg",
            assigned_employee=self.employee,
        )
        current_2 = self._create_incidence(
            Incidence.Status.REVIEW,
            today,
            "emp-current-2.jpg",
            assigned_employee=self.employee,
        )
        self._create_incidence(Incidence.Status.NEW, today, "not-assigned.jpg")

        response = self.client.get(
            "/api/home/incidence/employee/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Employee"]["id"], self.employee.id)
        self.assertEqual(payload["Employee"]["Name"], self.employee.name)
        self.assertEqual(payload["Total_Completed_Incidences"], 1)
        self.assertEqual(payload["Total_Current_Incidences"], 2)

        completed_ids = [item["id"] for item in payload["Completed_Incidences"]]
        current_ids = [item["id"] for item in payload["Current_Incidences"]]

        self.assertEqual(completed_ids, [completed_1.id])
        self.assertEqual(current_ids, [current_2.id, current_1.id])

    def test_get_incidences_status_overview(self):
        today = timezone.localdate()
        month_start = today.replace(day=1)
        if month_start.month == 12:
            next_month_start = month_start.replace(year=month_start.year + 1, month=1, day=1)
        else:
            next_month_start = month_start.replace(month=month_start.month + 1, day=1)
        previous_month_day = month_start - timedelta(days=1)

        self._create_incidence(Incidence.Status.NEW, today, "overview-new.jpg")
        self._create_incidence(Incidence.Status.ASSIGNED, month_start, "overview-assigned.jpg")
        self._create_incidence(Incidence.Status.IN_PROGRESS, today, "overview-in-progress.jpg")
        self._create_incidence(Incidence.Status.REVIEW, today, "overview-review.jpg")
        self._create_incidence(Incidence.Status.FORWORDED, today, "overview-forwarded.jpg")
        self._create_incidence(Incidence.Status.FINISHED, today, "overview-completed-this-month.jpg")
        self._create_incidence(
            Incidence.Status.FINISHED,
            previous_month_day,
            "overview-completed-previous-month.jpg",
        )

        response = self.client.get(
            "/api/home/incidence/status-overview/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Date"], str(today))
        self.assertEqual(payload["Month_Start"], str(month_start))
        self.assertEqual(payload["Month_End"], str(next_month_start - timedelta(days=1)))
        self.assertEqual(payload["Total_Incidences"], 6)
        self.assertEqual(payload["Assigned_And_In_Progress_Incidences"], 2)
        self.assertEqual(payload["In_Review_Incidences"], 1)
        self.assertEqual(payload["Forwarded_Incidences"], 1)
        self.assertEqual(payload["Completed_This_Month_Incidences"], 1)
        self.assertEqual(payload["Completed_Today_Incidences"], 1)

    def test_get_weekly_incidences_chart_data(self):
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        previous_week_day = week_start - timedelta(days=1)

        self._create_incidence(
            Incidence.Status.NEW,
            week_start,
            "chart-week-start-1.jpg",
            created_at_date=week_start,
        )
        self._create_incidence(
            Incidence.Status.NEW,
            week_start,
            "chart-week-start-2.jpg",
            created_at_date=week_start,
        )
        self._create_incidence(
            Incidence.Status.ASSIGNED,
            week_start + timedelta(days=2),
            "chart-mid-week.jpg",
            created_at_date=week_start + timedelta(days=2),
        )
        self._create_incidence(
            Incidence.Status.REVIEW,
            week_end,
            "chart-week-end.jpg",
            created_at_date=week_end,
        )
        self._create_incidence(
            Incidence.Status.FINISHED,
            previous_week_day,
            "chart-previous-week.jpg",
            created_at_date=previous_week_day,
        )

        response = self.client.get(
            "/api/home/incidence/weekly-chart/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Date"], str(today))
        self.assertEqual(payload["Week_Start"], str(week_start))
        self.assertEqual(payload["Week_End"], str(week_end))
        self.assertEqual(payload["Total_Incidences_This_Week"], 4)
        self.assertEqual(len(payload["Chart_Data"]), 7)

        data_by_date = {item["Date"]: item for item in payload["Chart_Data"]}
        self.assertEqual(data_by_date[str(week_start)]["Incidences_Count"], 2)
        self.assertEqual(data_by_date[str(week_start + timedelta(days=2))]["Incidences_Count"], 1)
        self.assertEqual(data_by_date[str(week_end)]["Incidences_Count"], 1)
        self.assertEqual(data_by_date[str(week_start + timedelta(days=1))]["Incidences_Count"], 0)
        self.assertTrue(data_by_date[str(week_start)]["Day"])
        self.assertTrue(data_by_date[str(week_start)]["Month"])

    def test_get_monthly_department_incidences_chart_data(self):
        today = timezone.localdate()
        month_start = today.replace(day=1)
        if month_start.month == 12:
            next_month_start = month_start.replace(year=month_start.year + 1, month=1, day=1)
        else:
            next_month_start = month_start.replace(month=month_start.month + 1, day=1)
        previous_month_day = month_start - timedelta(days=1)

        self._create_incidence(
            Incidence.Status.NEW,
            month_start,
            "month-dep-main-1.jpg",
            department=self.department,
            created_at_date=month_start,
        )
        self._create_incidence(
            Incidence.Status.ASSIGNED,
            today,
            "month-dep-main-2.jpg",
            department=self.department,
            created_at_date=today,
        )
        self._create_incidence(
            Incidence.Status.REVIEW,
            today,
            "month-dep-main-3.jpg",
            department=self.department,
            created_at_date=today,
        )
        self._create_incidence(
            Incidence.Status.NEW,
            today,
            "month-dep-other-1.jpg",
            department=self.other_department,
            created_at_date=today,
        )
        self._create_incidence(
            Incidence.Status.FORWORDED,
            today,
            "month-dep-other-2.jpg",
            department=self.other_department,
            created_at_date=today,
        )
        self._create_incidence(
            Incidence.Status.FINISHED,
            previous_month_day,
            "month-dep-previous.jpg",
            department=self.other_department,
            created_at_date=previous_month_day,
        )

        response = self.client.get(
            "/api/home/incidence/monthly-department-chart/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Date"], str(today))
        self.assertEqual(payload["Month_Start"], str(month_start))
        self.assertEqual(payload["Month_End"], str(next_month_start - timedelta(days=1)))
        self.assertEqual(payload["Total_Incidences_This_Month"], 5)
        self.assertEqual(payload["Departments_Count"], 2)

        chart_by_department_id = {item["Department_Id"]: item for item in payload["Chart_Data"]}
        self.assertEqual(chart_by_department_id[self.department.id]["Department_Name"], self.department.name)
        self.assertEqual(chart_by_department_id[self.department.id]["Incidences_Count"], 3)
        self.assertEqual(
            chart_by_department_id[self.other_department.id]["Department_Name"],
            self.other_department.name,
        )
        self.assertEqual(chart_by_department_id[self.other_department.id]["Incidences_Count"], 2)

    def test_get_latest_incidence_per_department(self):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)

        # Department 1: latest should be the one created today.
        self._create_incidence(
            Incidence.Status.NEW,
            yesterday,
            "latest-dep1-old.jpg",
            department=self.department,
            created_at_date=yesterday,
        )
        dep1_latest = self._create_incidence(
            Incidence.Status.REVIEW,
            today,
            "latest-dep1-new.jpg",
            department=self.department,
            created_at_date=today,
        )

        # Department 2: same created_at date, latest should fallback to higher id.
        self._create_incidence(
            Incidence.Status.ASSIGNED,
            today,
            "latest-dep2-first.jpg",
            department=self.other_department,
            created_at_date=today,
        )
        dep2_latest = self._create_incidence(
            Incidence.Status.FORWORDED,
            today,
            "latest-dep2-second.jpg",
            department=self.other_department,
            created_at_date=today,
        )

        response = self.client.get(
            "/api/home/incidence/latest-per-department/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Total_Departments"], 2)

        latest_by_department_id = {item["Department"]["id"]: item for item in payload["Latest_Incidences"]}
        self.assertEqual(latest_by_department_id[self.department.id]["Incidence_Number"], dep1_latest.id)
        self.assertEqual(latest_by_department_id[self.department.id]["Status"], Incidence.Status.REVIEW)
        self.assertEqual(latest_by_department_id[self.department.id]["Department"]["name"], self.department.name)
        self.assertTrue(latest_by_department_id[self.department.id]["Date"])

        self.assertEqual(latest_by_department_id[self.other_department.id]["Incidence_Number"], dep2_latest.id)
        self.assertEqual(latest_by_department_id[self.other_department.id]["Status"], Incidence.Status.FORWORDED)
        self.assertEqual(
            latest_by_department_id[self.other_department.id]["Department"]["name"],
            self.other_department.name,
        )

    def test_get_incidences_status_summary_by_date_range(self):
        today = timezone.localdate()
        start_date = today - timedelta(days=2)
        end_date = today
        before_start = start_date - timedelta(days=1)
        after_end = end_date + timedelta(days=1)

        self._create_incidence(
            Incidence.Status.ASSIGNED,
            start_date,
            "range-assigned.jpg",
            created_at_date=start_date,
        )
        self._create_incidence(
            Incidence.Status.IN_PROGRESS,
            start_date + timedelta(days=1),
            "range-in-progress.jpg",
            created_at_date=start_date + timedelta(days=1),
        )
        self._create_incidence(
            Incidence.Status.REVIEW,
            end_date,
            "range-review.jpg",
            created_at_date=end_date,
        )
        self._create_incidence(
            Incidence.Status.FORWORDED,
            end_date,
            "range-forworded.jpg",
            created_at_date=end_date,
        )
        self._create_incidence(
            Incidence.Status.FINISHED,
            start_date + timedelta(days=1),
            "range-completed.jpg",
            created_at_date=start_date + timedelta(days=1),
        )
        self._create_incidence(
            Incidence.Status.NEW,
            start_date,
            "range-new.jpg",
            created_at_date=start_date,
        )

        self._create_incidence(
            Incidence.Status.FINISHED,
            before_start,
            "range-out-before.jpg",
            created_at_date=before_start,
        )
        self._create_incidence(
            Incidence.Status.REVIEW,
            after_end,
            "range-out-after.jpg",
            created_at_date=after_end,
        )

        response = self.client.get(
            f"/api/home/incidence/status-summary-by-date/?start_date={start_date}&end_date={end_date}",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Start_Date"], str(start_date))
        self.assertEqual(payload["End_Date"], str(end_date))
        self.assertEqual(payload["Total_Incidences"], 6)
        self.assertEqual(payload["Assigned_And_In_Progress_Incidences"], 2)
        self.assertEqual(payload["Review_Incidences"], 1)
        self.assertEqual(payload["Forworded_Incidences"], 1)
        self.assertEqual(payload["Completed_Incidences"], 1)

    def test_get_incidences_status_summary_by_date_range_rejects_invalid_range(self):
        response = self.client.get(
            "/api/home/incidence/status-summary-by-date/?start_date=2026-05-10&end_date=2026-05-01",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Start_Date cannot be after End_Date.")

    def test_get_department_incidences_summary_by_date_range(self):
        today = timezone.localdate()
        start_date = today - timedelta(days=2)
        end_date = today
        before_start = start_date - timedelta(days=1)

        self._create_incidence(
            Incidence.Status.NEW,
            start_date,
            "dep-range-main-1.jpg",
            department=self.department,
            created_at_date=start_date,
        )
        self._create_incidence(
            Incidence.Status.ASSIGNED,
            start_date + timedelta(days=1),
            "dep-range-main-2.jpg",
            department=self.department,
            created_at_date=start_date + timedelta(days=1),
        )
        self._create_incidence(
            Incidence.Status.REVIEW,
            end_date,
            "dep-range-other-1.jpg",
            department=self.other_department,
            created_at_date=end_date,
        )
        incidence_no_department = self._create_incidence(
            Incidence.Status.IN_PROGRESS,
            end_date,
            "dep-range-no-department.jpg",
            created_at_date=end_date,
        )
        incidence_no_department.department = None
        incidence_no_department.save(update_fields=["department"])

        # خارج النطاق الزمني (لازم لا يتحسب)
        self._create_incidence(
            Incidence.Status.FINISHED,
            before_start,
            "dep-range-outside.jpg",
            department=self.other_department,
            created_at_date=before_start,
        )

        response = self.client.get(
            f"/api/home/incidence/department-summary-by-date/?start_date={start_date}&end_date={end_date}",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Start_Date"], str(start_date))
        self.assertEqual(payload["End_Date"], str(end_date))
        self.assertEqual(payload["Total_Incidences"], 4)
        self.assertEqual(payload["Departments_Count"], 3)

        counts_by_department_name = {
            item["Department_Name"]: item["Incidences_Count"] for item in payload["Departments"]
        }
        self.assertEqual(counts_by_department_name[self.department.name], 2)
        self.assertEqual(counts_by_department_name[self.other_department.name], 1)
        self.assertEqual(counts_by_department_name["No Department"], 1)

    def test_get_department_incidences_summary_by_date_range_rejects_invalid_range(self):
        response = self.client.get(
            "/api/home/incidence/department-summary-by-date/?start_date=2026-05-10&end_date=2026-05-01",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Start_Date cannot be after End_Date.")

    def test_get_incidences_heatmap_data(self):
        today = timezone.localdate()

        self._create_incidence(
            Incidence.Status.NEW,
            today,
            "heatmap-downtown-1.jpg",
            location_name="Downtown",
            latlatitude="30.1234567",
            longitude="31.1234567",
        )
        self._create_incidence(
            Incidence.Status.REVIEW,
            today,
            "heatmap-downtown-2.jpg",
            location_name="Downtown",
            latlatitude="30.1234567",
            longitude="31.1234567",
        )
        self._create_incidence(
            Incidence.Status.ASSIGNED,
            today,
            "heatmap-nasr-city.jpg",
            location_name="Nasr City",
            latlatitude="30.9876543",
            longitude="31.9876543",
        )

        response = self.client.get(
            "/api/home/incidence/heatmap/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Total_Incidences"], 3)
        self.assertEqual(payload["Total_Locations"], 2)

        data_by_location = {item["Location_Name"]: item for item in payload["Heatmap_Data"]}
        self.assertEqual(data_by_location["Downtown"]["Incidences_Count"], 2)
        self.assertEqual(data_by_location["Downtown"]["Latlatitude"], 30.1234567)
        self.assertEqual(data_by_location["Downtown"]["Longitude"], 31.1234567)
        self.assertEqual(data_by_location["Nasr City"]["Incidences_Count"], 1)

    def test_search_location_incidences_analysis(self):
        today = timezone.localdate()
        location_name = "Nile Street"

        finished_1 = self._create_incidence(
            Incidence.Status.FINISHED,
            today,
            "location-analysis-finished-1.jpg",
            department=self.department,
            created_at_date=today,
            location_name=location_name,
            latlatitude="30.1100000",
            longitude="31.1100000",
        )
        finished_2 = self._create_incidence(
            Incidence.Status.FINISHED,
            today,
            "location-analysis-finished-2.jpg",
            department=self.department,
            created_at_date=today,
            location_name=location_name,
            latlatitude="30.1100000",
            longitude="31.1100000",
        )
        self._create_incidence(
            Incidence.Status.REVIEW,
            today,
            "location-analysis-review.jpg",
            department=self.other_department,
            created_at_date=today,
            location_name=location_name,
            latlatitude="30.2200000",
            longitude="31.2200000",
        )
        self._create_incidence(
            Incidence.Status.NEW,
            today,
            "location-analysis-other-location.jpg",
            department=self.department,
            created_at_date=today,
            location_name="Different Street",
            latlatitude="30.3300000",
            longitude="31.3300000",
        )

        finished_1.completed_at = finished_1.created_at + timedelta(hours=2)
        finished_1.save(update_fields=["completed_at"])
        finished_2.completed_at = finished_2.created_at + timedelta(hours=4, minutes=30)
        finished_2.save(update_fields=["completed_at"])

        response = self.client.get(
            f"/api/home/incidence/location-analysis/?location_name={location_name}",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Location_Name"], location_name)
        self.assertEqual(payload["Total_Incidences_On_Street"], 3)
        self.assertEqual(payload["Solved_Incidences_Count"], 2)
        self.assertEqual(payload["Average_Solve_Duration_Seconds"], 11700)
        self.assertEqual(payload["Average_Solve_Duration"], "0d 3h 15m 0s")

        self.assertEqual(payload["Most_Frequent_Department"]["id"], self.department.id)
        self.assertEqual(payload["Most_Frequent_Department"]["name"], self.department.name)
        self.assertEqual(payload["Most_Frequent_Department"]["Incidences_Count"], 2)

        incidence_by_id = {item["Incidence_Number"]: item for item in payload["incidences"]}
        self.assertEqual(incidence_by_id[finished_1.id]["Solve_Duration_Seconds"], 7200)
        self.assertEqual(incidence_by_id[finished_2.id]["Solve_Duration_Seconds"], 16200)
        self.assertEqual(incidence_by_id[finished_1.id]["Lat"], "30.1100000")
        self.assertEqual(incidence_by_id[finished_1.id]["Long"], "31.1100000")

    def test_search_location_incidences_analysis_requires_location_name(self):
        response = self.client.get(
            "/api/home/incidence/location-analysis/",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Location_Name is required.")

    def test_get_incidences_time_counts_by_date_range(self):
        today = timezone.localdate()
        month_start = today.replace(day=1)
        start_date = month_start - timedelta(days=4)
        end_date = month_start + timedelta(days=4)
        before_start = start_date - timedelta(days=1)

        d1 = start_date
        d2 = start_date + timedelta(days=2)
        d3 = month_start + timedelta(days=1)
        d4 = month_start + timedelta(days=3)

        self._create_incidence(
            Incidence.Status.NEW,
            d1,
            "time-range-1.jpg",
            department=self.department,
            created_at_date=d1,
        )
        self._create_incidence(
            Incidence.Status.ASSIGNED,
            d2,
            "time-range-2.jpg",
            department=self.department,
            created_at_date=d2,
        )
        self._create_incidence(
            Incidence.Status.REVIEW,
            d3,
            "time-range-3.jpg",
            department=self.other_department,
            created_at_date=d3,
        )
        self._create_incidence(
            Incidence.Status.FINISHED,
            d4,
            "time-range-4.jpg",
            department=self.other_department,
            created_at_date=d4,
        )
        self._create_incidence(
            Incidence.Status.NEW,
            before_start,
            "time-range-outside.jpg",
            department=self.department,
            created_at_date=before_start,
        )

        response = self.client.get(
            f"/api/home/incidence/time-counts-by-date/?start_date={start_date}&end_date={end_date}",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Start_Date"], str(start_date))
        self.assertEqual(payload["End_Date"], str(end_date))
        self.assertEqual(payload["Total_Incidences"], 4)

        daily_map = {item["Date"]: item["Incidences_Count"] for item in payload["Daily_Counts"]}
        self.assertEqual(daily_map[str(d1)], 1)
        self.assertEqual(daily_map[str(d2)], 1)
        self.assertEqual(daily_map[str(d3)], 1)
        self.assertEqual(daily_map[str(d4)], 1)

        expected_weekly_counts = {}
        for day_value in [d1, d2, d3, d4]:
            week_start = day_value - timedelta(days=day_value.weekday())
            expected_weekly_counts[week_start] = expected_weekly_counts.get(week_start, 0) + 1

        weekly_map = {item["Week_Start"]: item["Incidences_Count"] for item in payload["Weekly_Counts"]}
        for week_start, expected_count in expected_weekly_counts.items():
            self.assertEqual(weekly_map[str(week_start)], expected_count)

        expected_monthly_counts = {}
        for day_value in [d1, d2, d3, d4]:
            month_key = day_value.replace(day=1)
            expected_monthly_counts[month_key] = expected_monthly_counts.get(month_key, 0) + 1

        monthly_map = {item["Month_Start"]: item["Incidences_Count"] for item in payload["Monthly_Counts"]}
        for month_start_value, expected_count in expected_monthly_counts.items():
            self.assertEqual(monthly_map[str(month_start_value)], expected_count)

    def test_get_incidences_time_counts_by_date_range_rejects_invalid_range(self):
        response = self.client.get(
            "/api/home/incidence/time-counts-by-date/?start_date=2026-06-10&end_date=2026-05-01",
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Start_Date cannot be after End_Date.")
