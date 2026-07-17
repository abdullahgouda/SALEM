from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=120, unique=True, db_column="Name")
    logo = models.FileField(
        upload_to="departments/logos/",
        null=True,
        blank=True,
        db_column="Logo",
    )

    class Meta:
        db_table = "Department"

    def __str__(self):
        return self.name


class User(models.Model):

    USERNAME_FIELD = "national_id"
    REQUIRED_FIELDS = []
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    class UserType(models.TextChoices):
        CITIZIN = "citizin", "Citizin"
        EMPLOYEE = "employee", "Employee"


    class EmployeeRole(models.TextChoices):
        TECHNICAL = "technical", "Technical"
        OPERATOR = "operator", "Operator"
        ADMIN = "admin", "Admin"
        SUPERVISIOR = "supervisior", "Supervisior"

    name = models.CharField(max_length=255, db_column="Name")
    national_id = models.CharField(max_length=14, unique=True, db_column="National_Id")
    phone_number = models.CharField(max_length=11, unique=True, db_column="Phone_Number")
    email = models.EmailField(unique=True, db_column="Email")
    password = models.CharField(max_length=255, db_column="Password")
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        db_column="User_Type",
    )
    is_active = models.BooleanField(default=True, db_column="Is_Active")

    role = models.CharField(
        max_length=20,
        choices=EmployeeRole.choices,
        null=True,
        blank=True,
        db_column="Role",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
        db_column="Department",
    )
    region = models.CharField(max_length=120, null=True, blank=True, db_column="Region")

    birthdate = models.DateField(null=True, blank=True, db_column="Birthdate")
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        db_column="Username",
    )
    trust_score = models.FloatField(
    default=0.5,
    db_column="Trust_Score"
)

    trust_level = models.CharField(
    max_length=20,
    default="Medium",
    db_column="Trust_Level"
)

    valid_ratio = models.FloatField(
    default=0,
    db_column="Valid_Ratio"
)

    duplicate_rate = models.FloatField(
    default=0,
    db_column="Duplicate_Rate"
)

    fake_image_ratio = models.FloatField(
    default=0,
    db_column="Fake_Image_Ratio"
)

    class Meta:
        db_table = "Users"
        constraints = [
            models.CheckConstraint(
                name="employee_required_fields",
                # تم تغيير condition إلى check للتوافق مع Django 5.0
                check=(
                    ~Q(user_type="employee")
                    | (
                        Q(role__isnull=False)
                        & ~Q(role="")
                        & Q(department__isnull=False)
                        & Q(region__isnull=False)
                        & ~Q(region="")
                    )
                ),
            ),
            models.CheckConstraint(
                name="citizin_required_fields",
                # تم تغيير condition إلى check للتوافق مع Django 5.0
                check=(
                    ~Q(user_type="citizin")
                    | (
                        Q(birthdate__isnull=False)
                        & Q(username__isnull=False)
                        & ~Q(username="")
                    )
                ),
            ),
        ]

    def clean(self):
        errors = {}

        if self.user_type == self.UserType.EMPLOYEE:
            if not self.role:
                errors["role"] = "Role is required when user_type is employee."
            if not self.department:
                errors["department"] = "Department is required when user_type is employee."
            if not self.region:
                errors["region"] = "Region is required when user_type is employee."
        elif self.user_type == self.UserType.CITIZIN:
            if not self.birthdate:
                errors["birthdate"] = "Birthdate is required when user_type is citizin."
            if not self.username:
                errors["username"] = "Username is required when user_type is citizin."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.user_type})"


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="password_reset_otps",
        db_column="User_Id",
    )
    email = models.EmailField(db_column="Email")
    otp_code = models.CharField(max_length=6, db_column="OTP_Code")
    is_verified = models.BooleanField(default=False, db_column="Is_Verified")
    is_used = models.BooleanField(default=False, db_column="Is_Used")
    expires_at = models.DateTimeField(db_column="Expires_At")
    created_at = models.DateTimeField(auto_now_add=True, db_column="Created_At")

    class Meta:
        db_table = "Password_Reset_OTP"
        indexes = [
            models.Index(fields=["email", "otp_code"]),
            models.Index(fields=["email", "is_verified", "is_used"]),
        ]

    def __str__(self):
        return f"{self.email} - {self.otp_code}"


class Incidence(models.Model):
    class Status(models.TextChoices):
        NEW = "New", "New"
        ASSIGNED = "Assigned", "Assigned"
        IN_PROGRESS = "In_Progress", "In_Progress"
        REVIEW = "Review", "Review"
        FORWORDED = "Forworded", "Forworded"
        FINISHED = "Finished", "Finished"
        REJECTED = "Rejected", "Rejected"

    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"

    description = models.TextField(db_column="Description")
    latlatitude = models.DecimalField(max_digits=10, decimal_places=7, db_column="Latlatitude")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, db_column="Longitude")
    location_name = models.CharField(max_length=255, db_column="Location_Name")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        db_column="Status",
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        db_column="Completed_At",
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        db_column="Created_At",
        db_index=True,
    )
    forward_reason = models.CharField(
    max_length=100,
    null=True,
    blank=True
)
    dashboard_date = models.DateField(
        default=timezone.localdate,
        db_column="Dashboard_Date",
        db_index=True,
    )
    location_confirmation = models.BooleanField(
        default=False,
        db_column="Location_Confirmation",
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name="incidences",
        null=True,
        blank=True,
        db_column="Department",
    )
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        null=True,
        blank=True,
        db_column="Priority",
    )
    image_before_analysis = models.FileField(
        upload_to="incidence/before/",
        null=True,
        blank=False,
        db_column="Image_Before_Analysis",
    )
    image_after_analysis = models.FileField(
        upload_to="incidence/after/",
        null=True,
        blank=True,
        db_column="Image_After_Analysis",
    )
    ai_analysis_label_before = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="Ai_Analysis_Label_Before",
    )
    ai_analysis_label_after = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        db_column="Ai_Analysis_Label_After",
    )
    what_was_done = models.TextField(
        null=True,
        blank=True,
        db_column="What_was_done",
    )
    citizin = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_incidences",
        db_column="Citizin_Id",
        limit_choices_to={"user_type": User.UserType.CITIZIN},
    )
    assigned_employee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_incidences",
        null=True,
        blank=True,
        db_column="Assigned_Employee_Id",
        limit_choices_to={"user_type": User.UserType.EMPLOYEE},
    )

    duplicate = models.BooleanField(
    default=False,
    db_column="Duplicate"
)

    duplicate_similarity = models.FloatField(
    null=True,
    blank=True,
    db_column="Duplicate_Similarity"
)

    trust_score = models.FloatField(
    null=True,
    blank=True,
    db_column="Trust_Score"
)

    trust_level = models.CharField(
    max_length=20,
    null=True,
    blank=True,
    db_column="Trust_Level"
)

    severity_prediction = models.CharField(
    max_length=20,
    null=True,
    blank=True,
    db_column="Severity_Prediction"
)

    severity_score = models.FloatField(
    null=True,
    blank=True,
)

    priority_prediction = models.CharField(
    max_length=20,
    null=True,
    blank=True,
)

    priority_score = models.FloatField(
    null=True,
    blank=True,
)

    road_prediction = models.CharField(
    max_length=50,
    null=True,
    blank=True,
)

    road_confidence = models.FloatField(
    null=True,
    blank=True,
)

    image_authenticity = models.CharField(
    max_length=50,
    null=True,
    blank=True,
)

    image_confidence = models.FloatField(
    null=True,
    blank=True,
)

    class Meta:
        db_table = "Incidence"

    def clean(self):
        errors = {}

        if self.citizin and self.citizin.user_type != User.UserType.CITIZIN:
            errors["citizin"] = "Citizin must be a user with user_type='citizin'."

        if self.assigned_employee and self.assigned_employee.user_type != User.UserType.EMPLOYEE:
            errors["assigned_employee"] = "Assigned employee must have user_type='employee'."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        previous_status = None
        if self.pk:
            previous_status = (
                Incidence.objects.filter(pk=self.pk).values_list("status", flat=True).first()
            )

        if self.status == self.Status.FINISHED:
            if previous_status != self.Status.FINISHED or self.completed_at is None:
                self.completed_at = timezone.now()
        elif previous_status == self.Status.FINISHED:
            self.completed_at = None

        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Incidence #{self.id} - {self.status}"


class OperatorNotification(models.Model):
    operator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_operator_notifications",
        db_column="Operator_Id",
        limit_choices_to={
            "user_type": User.UserType.EMPLOYEE,
            "role": User.EmployeeRole.OPERATOR,
        },
    )
    sender_employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_operator_notifications",
        db_column="Sender_Employee_Id",
        limit_choices_to={"user_type": User.UserType.EMPLOYEE},
    )
    incidence = models.ForeignKey(
        Incidence,
        on_delete=models.CASCADE,
        related_name="operator_notifications",
        db_column="Incidence_Id",
    )
    location_name = models.CharField(max_length=255, db_column="Location_Name")
    latlatitude = models.DecimalField(max_digits=10, decimal_places=7, db_column="Latlatitude")
    longitude = models.DecimalField(max_digits=10, decimal_places=7, db_column="Longitude")
    priority = models.CharField(
        max_length=10,
        choices=Incidence.Priority.choices,
        null=True,
        blank=True,
        db_column="Priority",
    )
    department_name = models.CharField(max_length=120, db_column="Department_Name")
    employee_name = models.CharField(max_length=255, db_column="Employee_Name")
    employee_email = models.EmailField(db_column="Employee_Email")
    is_read = models.BooleanField(default=False, db_column="Is_Read")
    created_at = models.DateTimeField(auto_now_add=True, db_column="Created_At", db_index=True)

    class Meta:
        db_table = "Operator_Notification"
        indexes = [
            models.Index(fields=["operator", "is_read", "created_at"]),
            models.Index(fields=["incidence", "created_at"]),
        ]

    def __str__(self):
        return f"Notification #{self.id} to operator {self.operator_id}"