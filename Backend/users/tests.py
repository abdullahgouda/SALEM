import json
from datetime import datetime, timedelta, timezone

import jwt
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Department, Incidence, OperatorNotification, User


class IncidenceByIdAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Roads")
        self.employee = User.objects.create(
            name="Assigned Employee",
            national_id="88888888888888",
            phone_number="01088888888",
            email="assigned.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.department,
            region="Giza",
        )
        self.citizin = User.objects.create(
            name="Incidence Owner",
            national_id="99999999999999",
            phone_number="01099999999",
            email="incidence.owner@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="2000-01-01",
            username="incidence_owner",
        )
        self.incidence = Incidence.objects.create(
            description="Damaged sidewalk",
            latlatitude="30.1000000",
            longitude="31.1000000",
            location_name="Downtown",
            status=Incidence.Status.ASSIGNED,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "before.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
            assigned_employee=self.employee,
        )

    def test_get_incidence_by_id_returns_full_incidence(self):
        response = self.client.get(f"/api/incidence/{self.incidence.id}/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()["incidence"]
        self.assertEqual(payload["id"], self.incidence.id)
        self.assertEqual(payload["Status"], Incidence.Status.ASSIGNED)
        self.assertTrue(payload["Created_At"])
        self.assertEqual(payload["Department"]["id"], self.department.id)
        self.assertEqual(payload["Citizin"]["Name"], self.citizin.name)
        self.assertEqual(payload["Citizin"]["Phone_Number"], self.citizin.phone_number)
        self.assertEqual(payload["Assigned_Employee"]["id"], self.employee.id)

    def test_get_incidence_by_id_returns_404_for_missing_incidence(self):
        response = self.client.get("/api/incidence/999999/")
        self.assertEqual(response.status_code, 404)


class EmployeeListAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Employee Department")
        self.requester_employee = User.objects.create(
            name="Requester Employee",
            national_id="10101010101010",
            phone_number="01010101010",
            email="requester.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.ADMIN,
            department=self.department,
            region="Cairo",
            is_active=True,
        )
        self.active_employee = User.objects.create(
            name="Active Employee",
            national_id="20202020202020",
            phone_number="01020202020",
            email="active.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.department,
            region="Giza",
            is_active=True,
        )
        self.inactive_employee = User.objects.create(
            name="Inactive Employee",
            national_id="30303030303030",
            phone_number="01030303030",
            email="inactive.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.TECHNICAL,
            department=self.department,
            region="Alex",
            is_active=False,
        )
        User.objects.create(
            name="Citizin User",
            national_id="40404040404040",
            phone_number="01040404040",
            email="citizin.user@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="2002-02-02",
            username="citizin_user_4040",
        )

    def _build_employee_access_token(self, user):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "national_id": user.national_id,
            "user_type": user.user_type,
            "role": user.role,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=15),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def test_get_all_employees_returns_employees_with_account_status(self):
        token = self._build_employee_access_token(self.requester_employee)
        response = self.client.get(
            "/api/employee/",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Total_Employees"], 3)
        employees_by_id = {item["id"]: item for item in payload["employees"]}

        self.assertEqual(employees_by_id[self.active_employee.id]["Name"], self.active_employee.name)
        self.assertEqual(employees_by_id[self.active_employee.id]["Email"], self.active_employee.email)
        self.assertEqual(employees_by_id[self.active_employee.id]["Role"], self.active_employee.role)
        self.assertEqual(employees_by_id[self.active_employee.id]["Account_Status"], "نشط")

        self.assertEqual(employees_by_id[self.inactive_employee.id]["Name"], self.inactive_employee.name)
        self.assertEqual(employees_by_id[self.inactive_employee.id]["Email"], self.inactive_employee.email)
        self.assertEqual(employees_by_id[self.inactive_employee.id]["Role"], self.inactive_employee.role)
        self.assertEqual(employees_by_id[self.inactive_employee.id]["Account_Status"], "معطل")


class EmployeeSignupAccountStatusAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Signup Department")

    def test_employee_signup_accepts_disabled_account_status(self):
        response = self.client.post(
            "/api/employee/signup/",
            data=json.dumps(
                {
                    "Name": "Signup Employee Disabled",
                    "National_Id": "81818181818181",
                    "Phone_Number": "01081818181",
                    "Email": "signup.employee.disabled@test.com",
                    "Password": "employeePass123",
                    "User_Type": "employee",
                    "Role": "operator",
                    "Region": "Cairo",
                    "Department": str(self.department.id),
                    "Account_Status": "معطل",
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        payload = response.json()
        self.assertEqual(payload["user"]["Account_Status"], "معطل")

        employee = User.objects.get(email="signup.employee.disabled@test.com")
        self.assertFalse(employee.is_active)

    def test_employee_signup_defaults_account_status_to_active(self):
        response = self.client.post(
            "/api/employee/signup/",
            data=json.dumps(
                {
                    "Name": "Signup Employee Active",
                    "National_Id": "91919191919191",
                    "Phone_Number": "01091919191",
                    "Email": "signup.employee.active@test.com",
                    "Password": "employeePass123",
                    "User_Type": "employee",
                    "Role": "operator",
                    "Region": "Giza",
                    "Department": str(self.department.id),
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

        payload = response.json()
        self.assertEqual(payload["user"]["Account_Status"], "نشط")

        employee = User.objects.get(email="signup.employee.active@test.com")
        self.assertTrue(employee.is_active)


class EmployeeManagementAPITest(TestCase):
    def setUp(self):
        self.department_a = Department.objects.create(name="Employee Mgmt Department A")
        self.department_b = Department.objects.create(name="Employee Mgmt Department B")
        self.requester_employee = User.objects.create(
            name="Requester Manager",
            national_id="62626262626262",
            phone_number="01062626262",
            email="requester.manager@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.ADMIN,
            department=self.department_a,
            region="Cairo",
            is_active=True,
        )
        self.target_employee = User.objects.create(
            name="Target Employee",
            national_id="73737373737373",
            phone_number="01073737373",
            email="target.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.department_a,
            region="Giza",
            is_active=True,
        )

    def _build_employee_access_token(self, user):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "national_id": user.national_id,
            "user_type": user.user_type,
            "role": user.role,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=15),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def test_update_employee_updates_fields_and_account_status(self):
        token = self._build_employee_access_token(self.requester_employee)
        response = self.client.patch(
            f"/api/employee/{self.target_employee.id}/update/",
            data=json.dumps(
                {
                    "Name": "Updated Employee",
                    "Email": "updated.employee@test.com",
                    "Role": "technical",
                    "Region": "Alex",
                    "Department": str(self.department_b.id),
                    "Account_Status": "معطل",
                }
            ),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["employee"]["Name"], "Updated Employee")
        self.assertEqual(payload["employee"]["Email"], "updated.employee@test.com")
        self.assertEqual(payload["employee"]["Role"], User.EmployeeRole.TECHNICAL)
        self.assertEqual(payload["employee"]["Region"], "Alex")
        self.assertEqual(payload["employee"]["Department"]["id"], self.department_b.id)
        self.assertEqual(payload["employee"]["Account_Status"], "معطل")

        self.target_employee.refresh_from_db()
        self.assertEqual(self.target_employee.name, "Updated Employee")
        self.assertEqual(self.target_employee.email, "updated.employee@test.com")
        self.assertEqual(self.target_employee.role, User.EmployeeRole.TECHNICAL)
        self.assertEqual(self.target_employee.region, "Alex")
        self.assertEqual(self.target_employee.department_id, self.department_b.id)
        self.assertFalse(self.target_employee.is_active)

    def test_update_employee_rejects_invalid_account_status(self):
        token = self._build_employee_access_token(self.requester_employee)
        response = self.client.patch(
            f"/api/employee/{self.target_employee.id}/update/",
            data=json.dumps({"Account_Status": "unknown"}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Account_Status must be either 'نشط' or 'معطل'.")

    def test_update_employee_returns_404_for_missing_employee(self):
        token = self._build_employee_access_token(self.requester_employee)
        response = self.client.patch(
            "/api/employee/999999/update/",
            data=json.dumps({"Name": "No One"}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_employee_deletes_target_employee(self):
        token = self._build_employee_access_token(self.requester_employee)
        response = self.client.delete(
            f"/api/employee/{self.target_employee.id}/delete/",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(id=self.target_employee.id).exists())

    def test_delete_employee_rejects_self_delete(self):
        token = self._build_employee_access_token(self.requester_employee)
        response = self.client.delete(
            f"/api/employee/{self.requester_employee.id}/delete/",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "You cannot delete your own account.")
        self.assertTrue(User.objects.filter(id=self.requester_employee.id).exists())


class IncidenceListFiltersAPITest(TestCase):
    def setUp(self):
        self.department_main = Department.objects.create(name="Main Department")
        self.department_other = Department.objects.create(name="Other Department")
        self.citizin = User.objects.create(
            name="Filter Citizin",
            national_id="12121212121212",
            phone_number="01012121212",
            email="filter.citizin@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="1998-08-08",
            username="filter_citizin",
        )
        self.today = datetime.now(timezone.utc).date()
        self.yesterday = self.today - timedelta(days=1)

    def _create_incidence(self, description, status, department, created_at_date):
        return Incidence.objects.create(
            description=description,
            latlatitude="30.1234567",
            longitude="31.1234567",
            location_name="Test Location",
            status=status,
            department=department,
            image_before_analysis=SimpleUploadedFile(
                f"{description.replace(' ', '_')}.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
            created_at=datetime(
                created_at_date.year,
                created_at_date.month,
                created_at_date.day,
                12,
                0,
                tzinfo=timezone.utc,
            ),
        )

    def test_get_incidences_filters_by_department_date_status_and_search_id(self):
        target = self._create_incidence(
            "Target incidence",
            Incidence.Status.ASSIGNED,
            self.department_main,
            self.today,
        )
        self._create_incidence(
            "Different department",
            Incidence.Status.ASSIGNED,
            self.department_other,
            self.today,
        )
        self._create_incidence(
            "Different status",
            Incidence.Status.NEW,
            self.department_main,
            self.today,
        )
        self._create_incidence(
            "Different date",
            Incidence.Status.ASSIGNED,
            self.department_main,
            self.yesterday,
        )

        response = self.client.get(
            "/api/incidence/",
            data={
                "Department": str(self.department_main.id),
                "Date": str(self.today),
                "Status": "assigned",
                "Search": str(target.id),
            },
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(len(payload["incidences"]), 1)
        self.assertEqual(payload["incidences"][0]["id"], target.id)
        self.assertEqual(payload["incidences"][0]["Department"]["id"], self.department_main.id)
        self.assertEqual(payload["incidences"][0]["Status"], Incidence.Status.ASSIGNED)

    def test_get_incidences_filters_return_400_for_invalid_date(self):
        response = self.client.get("/api/incidence/", data={"Date": "12-01-2026"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Date must be in YYYY-MM-DD format.")

    def test_get_incidences_filters_return_400_for_invalid_status(self):
        response = self.client.get("/api/incidence/", data={"Status": "unknown-status"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Invalid status filter.")

    def test_get_incidences_filters_return_400_for_non_numeric_search_id(self):
        response = self.client.get("/api/incidence/", data={"Search": "abc"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Search by id must be a valid integer.")


class NewIncidencesAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Lighting")
        self.citizin = User.objects.create(
            name="New Incidence Owner",
            national_id="34343434343434",
            phone_number="01034343434",
            email="new.incidence.owner@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="1997-07-07",
            username="new_incidence_owner",
        )
        self.new_incidence = Incidence.objects.create(
            description="Street light not working",
            latlatitude="30.5555555",
            longitude="31.5555555",
            location_name="Nasr City",
            status=Incidence.Status.NEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "new-incidence.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        Incidence.objects.create(
            description="Already assigned incidence",
            latlatitude="30.6666666",
            longitude="31.6666666",
            location_name="Heliopolis",
            status=Incidence.Status.ASSIGNED,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "assigned-incidence.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )

    def test_get_new_incidences_returns_only_new_status(self):
        response = self.client.get("/api/incidence/new/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Status"], Incidence.Status.NEW)
        self.assertEqual(payload["Total_New_Incidences"], 1)
        self.assertEqual(len(payload["incidences"]), 1)
        self.assertEqual(payload["incidences"][0]["id"], self.new_incidence.id)
        self.assertEqual(payload["incidences"][0]["Status"], Incidence.Status.NEW)


class AssignedIncidencesAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Road Maintenance")
        self.citizin = User.objects.create(
            name="Assigned Incidence Owner",
            national_id="56565656565656",
            phone_number="01056565656",
            email="assigned.incidence.owner@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="1996-06-06",
            username="assigned_incidence_owner",
        )
        self.assigned_incidence = Incidence.objects.create(
            description="Road crack requires assignment",
            latlatitude="30.7777777",
            longitude="31.7777777",
            location_name="Maadi",
            status=Incidence.Status.ASSIGNED,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "assigned-incidence-only.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        Incidence.objects.create(
            description="Not assigned incidence",
            latlatitude="30.8888888",
            longitude="31.8888888",
            location_name="Zamalek",
            status=Incidence.Status.NEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "not-assigned-incidence.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )

    def test_get_assigned_incidences_returns_only_assigned_status(self):
        response = self.client.get("/api/incidence/assigned/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Status"], Incidence.Status.ASSIGNED)
        self.assertEqual(payload["Total_Assigned_Incidences"], 1)
        self.assertEqual(len(payload["incidences"]), 1)
        self.assertEqual(payload["incidences"][0]["id"], self.assigned_incidence.id)
        self.assertEqual(payload["incidences"][0]["Status"], Incidence.Status.ASSIGNED)


class ReviewIncidencesAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Parks")
        self.citizin = User.objects.create(
            name="Review Incidence Owner",
            national_id="78787878787878",
            phone_number="01078787878",
            email="review.incidence.owner@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="1995-05-05",
            username="review_incidence_owner",
        )
        self.review_incidence = Incidence.objects.create(
            description="Park maintenance completed and waiting review",
            latlatitude="30.1111111",
            longitude="31.1111111",
            location_name="Dokki Park",
            status=Incidence.Status.REVIEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "review-incidence-only.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        Incidence.objects.create(
            description="Not review incidence",
            latlatitude="30.2222222",
            longitude="31.2222222",
            location_name="Orman",
            status=Incidence.Status.NEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "not-review-incidence.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )

    def test_get_review_incidences_returns_only_review_status(self):
        response = self.client.get("/api/incidence/review/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Status"], Incidence.Status.REVIEW)
        self.assertEqual(payload["Total_Review_Incidences"], 1)
        self.assertEqual(len(payload["incidences"]), 1)
        self.assertEqual(payload["incidences"][0]["id"], self.review_incidence.id)
        self.assertEqual(payload["incidences"][0]["Status"], Incidence.Status.REVIEW)


class CompletedIncidencesAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Waste")
        self.citizin = User.objects.create(
            name="Completed Incidence Owner",
            national_id="90909090909090",
            phone_number="01090909090",
            email="completed.incidence.owner@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="1993-03-03",
            username="completed_incidence_owner",
        )
        self.completed_incidence = Incidence.objects.create(
            description="Issue solved and completed",
            latlatitude="30.3333333",
            longitude="31.3333333",
            location_name="Shubra",
            status=Incidence.Status.FINISHED,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "completed-incidence-only.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        Incidence.objects.create(
            description="Not completed incidence",
            latlatitude="30.4444444",
            longitude="31.4444444",
            location_name="Abbasia",
            status=Incidence.Status.ASSIGNED,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "not-completed-incidence.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )

    def test_get_completed_incidences_returns_only_completed_status(self):
        response = self.client.get("/api/incidence/completed/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Status"], "Completed")
        self.assertEqual(payload["Total_Completed_Incidences"], 1)
        self.assertEqual(len(payload["incidences"]), 1)
        self.assertEqual(payload["incidences"][0]["id"], self.completed_incidence.id)
        self.assertEqual(payload["incidences"][0]["Status"], Incidence.Status.FINISHED)


class InProgressIncidencesAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Infrastructure")
        self.citizin = User.objects.create(
            name="In Progress Owner",
            national_id="91919191919191",
            phone_number="01091919191",
            email="in.progress.owner@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="1992-02-02",
            username="in_progress_owner",
        )
        self.in_progress_incidence = Incidence.objects.create(
            description="Work started and in progress",
            latlatitude="30.4545454",
            longitude="31.4545454",
            location_name="Ain Shams",
            status=Incidence.Status.IN_PROGRESS,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "in-progress-incidence-only.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        Incidence.objects.create(
            description="Not in progress incidence",
            latlatitude="30.5656565",
            longitude="31.5656565",
            location_name="Helwan",
            status=Incidence.Status.REVIEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "not-in-progress-incidence.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )

    def test_get_in_progress_incidences_returns_only_in_progress_status(self):
        response = self.client.get("/api/incidence/in-progress/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Status"], Incidence.Status.IN_PROGRESS)
        self.assertEqual(payload["Total_In_Progress_Incidences"], 1)
        self.assertEqual(len(payload["incidences"]), 1)
        self.assertEqual(payload["incidences"][0]["id"], self.in_progress_incidence.id)
        self.assertEqual(payload["incidences"][0]["Status"], Incidence.Status.IN_PROGRESS)


class ForwordedIncidencesAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Traffic")
        self.citizin = User.objects.create(
            name="Forworded Owner",
            national_id="92929292929292",
            phone_number="01092929292",
            email="forworded.owner@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="1991-01-01",
            username="forworded_owner",
        )
        self.forworded_incidence = Incidence.objects.create(
            description="Forwarded to another team",
            latlatitude="30.6767676",
            longitude="31.6767676",
            location_name="October",
            status=Incidence.Status.FORWORDED,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "forworded-incidence-only.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        Incidence.objects.create(
            description="Not forworded incidence",
            latlatitude="30.7878787",
            longitude="31.7878787",
            location_name="Hadayek",
            status=Incidence.Status.REVIEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "not-forworded-incidence.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )

    def test_get_forworded_incidences_returns_only_forworded_status(self):
        response = self.client.get("/api/incidence/forworded/")
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Status"], Incidence.Status.FORWORDED)
        self.assertEqual(payload["Total_Forworded_Incidences"], 1)
        self.assertEqual(len(payload["incidences"]), 1)
        self.assertEqual(payload["incidences"][0]["id"], self.forworded_incidence.id)
        self.assertEqual(payload["incidences"][0]["Status"], Incidence.Status.FORWORDED)


class CompleteIncidenceByRoleAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Completion Department")
        self.admin_employee = User.objects.create(
            name="Admin Employee",
            national_id="87878787878787",
            phone_number="01087878787",
            email="admin.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.ADMIN,
            department=self.department,
            region="Cairo",
        )
        self.supervisior_employee = User.objects.create(
            name="Supervisior Employee",
            national_id="89898989898989",
            phone_number="01089898989",
            email="supervisior.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.SUPERVISIOR,
            department=self.department,
            region="Giza",
        )
        self.operator_employee = User.objects.create(
            name="Operator Employee",
            national_id="90909090909090",
            phone_number="01090909090",
            email="operator.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.department,
            region="Alex",
        )
        self.citizin = User.objects.create(
            name="Completion Owner",
            national_id="91929292929292",
            phone_number="01091929292",
            email="completion.owner@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="2000-10-10",
            username="completion_owner",
        )
        self.incidence_new = Incidence.objects.create(
            description="Incidence to complete from new",
            latlatitude="30.4545454",
            longitude="31.4545454",
            location_name="Dokki",
            status=Incidence.Status.NEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "complete-new.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        self.incidence_review = Incidence.objects.create(
            description="Incidence to complete from review",
            latlatitude="30.5656565",
            longitude="31.5656565",
            location_name="Mohandessin",
            status=Incidence.Status.REVIEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "complete-review.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )

    def _build_employee_access_token(self, user):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "national_id": user.national_id,
            "user_type": user.user_type,
            "role": user.role,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=15),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def test_admin_can_move_any_incidence_status_to_completed(self):
        token = self._build_employee_access_token(self.admin_employee)
        response = self.client.post(
            "/api/incidence/complete/",
            data=json.dumps({"Incidence_id": self.incidence_new.id}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["incidence"]["Status"], Incidence.Status.FINISHED)

        self.incidence_new.refresh_from_db()
        self.assertEqual(self.incidence_new.status, Incidence.Status.FINISHED)
        self.assertIsNotNone(self.incidence_new.completed_at)

    def test_supervisior_can_move_any_incidence_status_to_completed(self):
        token = self._build_employee_access_token(self.supervisior_employee)
        response = self.client.post(
            "/api/incidence/complete/",
            data=json.dumps({"Incidence_id": self.incidence_review.id}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["incidence"]["Status"], Incidence.Status.FINISHED)

        self.incidence_review.refresh_from_db()
        self.assertEqual(self.incidence_review.status, Incidence.Status.FINISHED)
        self.assertIsNotNone(self.incidence_review.completed_at)

    def test_operator_cannot_move_incidence_to_completed(self):
        token = self._build_employee_access_token(self.operator_employee)
        response = self.client.post(
            "/api/incidence/complete/",
            data=json.dumps({"Incidence_id": self.incidence_new.id}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["message"],
            "Only admin or supervisior can move incidence to Completed.",
        )

        self.incidence_new.refresh_from_db()
        self.assertEqual(self.incidence_new.status, Incidence.Status.NEW)


class NotifyDepartmentRegionOperatorsAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Electricity")
        self.other_department = Department.objects.create(name="Roads")

        self.sender_employee = User.objects.create(
            name="API Sender",
            national_id="11111111111111",
            phone_number="01011111111",
            email="sender.employee@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.TECHNICAL,
            department=self.department,
            region="Giza",
        )
        self.operator_same_region = User.objects.create(
            name="Operator Same Region",
            national_id="22222222222222",
            phone_number="01022222222",
            email="operator.same.region@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.department,
            region="Giza",
        )
        self.operator_same_region_second = User.objects.create(
            name="Operator Same Region 2",
            national_id="33333333333333",
            phone_number="01033333333",
            email="operator.same.region.2@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.department,
            region="Giza",
        )
        self.operator_different_region = User.objects.create(
            name="Operator Different Region",
            national_id="44444444444444",
            phone_number="01044444444",
            email="operator.different.region@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.department,
            region="Cairo",
        )
        self.operator_different_department = User.objects.create(
            name="Operator Different Department",
            national_id="55555555555555",
            phone_number="01055555555",
            email="operator.different.department@test.com",
            password="raw-password",
            user_type=User.UserType.EMPLOYEE,
            role=User.EmployeeRole.OPERATOR,
            department=self.other_department,
            region="Giza",
        )
        self.citizin = User.objects.create(
            name="Incidence Owner",
            national_id="66666666666666",
            phone_number="01066666666",
            email="incidence.owner.2@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="2001-01-01",
            username="incidence_owner_2",
        )
        self.incidence = Incidence.objects.create(
            description="Power outage in street light",
            latlatitude="30.0123456",
            longitude="31.0123456",
            location_name="Dokki",
            status=Incidence.Status.ASSIGNED,
            priority=Incidence.Priority.HIGH,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "before.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
            assigned_employee=self.sender_employee,
        )
        self.other_department_incidence = Incidence.objects.create(
            description="Broken road",
            latlatitude="30.1000000",
            longitude="31.1000000",
            location_name="Mohandessin",
            status=Incidence.Status.NEW,
            priority=Incidence.Priority.MEDIUM,
            department=self.other_department,
            image_before_analysis=SimpleUploadedFile(
                "before2.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )

    def _build_employee_access_token(self, user):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "national_id": user.national_id,
            "user_type": user.user_type,
            "role": user.role,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=15),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def test_notify_department_region_operators_sends_to_matching_operators_only(self):
        token = self._build_employee_access_token(self.sender_employee)
        response = self.client.post(
            "/api/incidence/notify-operators/",
            data=json.dumps({"Incidence_id": self.incidence.id}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Recipients_Count"], 2)
        recipient_ids = {item["id"] for item in payload["Recipients"]}
        self.assertSetEqual(
            recipient_ids,
            {self.operator_same_region.id, self.operator_same_region_second.id},
        )
        self.assertEqual(payload["Notification_Data"]["Location"], "Dokki")
        self.assertEqual(payload["Notification_Data"]["Employee_Name"], self.sender_employee.name)
        self.assertEqual(payload["Notification_Data"]["Priority"], Incidence.Priority.HIGH)
        self.assertEqual(payload["Notification_Data"]["Incidence_id"], self.incidence.id)
        self.assertEqual(payload["Notification_Data"]["Department"], self.department.name)
        self.assertEqual(payload["Notification_Data"]["Employee_Email"], self.sender_employee.email)

        notifications = OperatorNotification.objects.filter(incidence=self.incidence).order_by("operator_id")
        self.assertEqual(notifications.count(), 2)
        self.assertEqual(notifications[0].operator_id, self.operator_same_region.id)
        self.assertEqual(notifications[1].operator_id, self.operator_same_region_second.id)
        self.assertTrue(
            all(
                notification.department_name == self.department.name
                and notification.employee_name == self.sender_employee.name
                and notification.employee_email == self.sender_employee.email
                and notification.location_name == self.incidence.location_name
                and str(notification.latlatitude) == str(self.incidence.latlatitude)
                and str(notification.longitude) == str(self.incidence.longitude)
                and notification.priority == self.incidence.priority
                for notification in notifications
            )
        )

    def test_notify_department_region_operators_rejects_incidence_of_other_department(self):
        token = self._build_employee_access_token(self.sender_employee)
        response = self.client.post(
            "/api/incidence/notify-operators/",
            data=json.dumps({"Incidence_id": self.other_department_incidence.id}),
            content_type="application/json",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(OperatorNotification.objects.count(), 0)


class CitizinIncidencesAPITest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Sanitation")
        self.citizin = User.objects.create(
            name="Citizin One",
            national_id="77777777777777",
            phone_number="01077777777",
            email="citizin.one@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="2002-02-02",
            username="citizin_one",
        )
        self.other_citizin = User.objects.create(
            name="Citizin Two",
            national_id="12345123451234",
            phone_number="01012345123",
            email="citizin.two@test.com",
            password="raw-password",
            user_type=User.UserType.CITIZIN,
            birthdate="2003-03-03",
            username="citizin_two",
        )
        self.my_incidence_newer = Incidence.objects.create(
            description="Overflowing garbage bin",
            latlatitude="30.2200000",
            longitude="31.2200000",
            location_name="Agouza",
            status=Incidence.Status.NEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "before-c1-new.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        self.my_incidence_older = Incidence.objects.create(
            description="Street needs cleaning",
            latlatitude="30.1200000",
            longitude="31.1200000",
            location_name="Dokki",
            status=Incidence.Status.ASSIGNED,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "before-c1-old.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.citizin,
        )
        self.other_citizin_incidence = Incidence.objects.create(
            description="Blocked sewer",
            latlatitude="30.3300000",
            longitude="31.3300000",
            location_name="Haram",
            status=Incidence.Status.NEW,
            department=self.department,
            image_before_analysis=SimpleUploadedFile(
                "before-c2.jpg",
                b"fake-image-bytes",
                content_type="image/jpeg",
            ),
            citizin=self.other_citizin,
        )

    def _build_citizin_access_token(self, user):
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user.id),
            "national_id": user.national_id,
            "user_type": user.user_type,
            "role": user.role,
            "type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=15),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def test_get_citizin_incidences_returns_only_logged_in_citizin_incidences(self):
        token = self._build_citizin_access_token(self.citizin)
        response = self.client.get(
            "/api/incidence/citizin/",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)

        payload = response.json()
        self.assertEqual(payload["Citizin"]["id"], self.citizin.id)
        self.assertEqual(payload["Total_Incidences"], 2)
        returned_ids = [item["id"] for item in payload["incidences"]]
        self.assertEqual(
            returned_ids,
            [self.my_incidence_older.id, self.my_incidence_newer.id],
        )

    def test_get_citizin_incidence_by_id_returns_incidence_if_owner(self):
        token = self._build_citizin_access_token(self.citizin)
        response = self.client.get(
            f"/api/incidence/citizin/{self.my_incidence_newer.id}/",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["incidence"]["id"], self.my_incidence_newer.id)

    def test_get_citizin_incidence_by_id_returns_404_if_not_owner(self):
        token = self._build_citizin_access_token(self.citizin)
        response = self.client.get(
            f"/api/incidence/citizin/{self.other_citizin_incidence.id}/",
            headers={"Authorization": f"Bearer {token}"},
        )
        self.assertEqual(response.status_code, 404)
