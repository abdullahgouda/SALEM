from django.contrib import admin
from .models import Department, User, PasswordResetOTP, Incidence, OperatorNotification

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user_type', 'role', 'department', 'is_active')
    list_filter = ('user_type', 'role', 'department', 'is_active')
    search_fields = ('name', 'email', 'national_id', 'phone_number', 'username')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'username', 'email', 'password', 'is_active')
        }),
        ('Identification', {
            'fields': ('national_id', 'phone_number', 'birthdate')
        }),
        ('Classification', {
            'fields': ('user_type', 'role', 'department', 'region')
        }),
    )

@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp_code', 'is_verified', 'is_used', 'expires_at', 'created_at')
    list_filter = ('is_verified', 'is_used')
    search_fields = ('email', 'otp_code')
    readonly_fields = ('created_at',)

@admin.register(Incidence)
class IncidenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'citizin', 'department', 'status', 'priority', 'created_at', 'completed_at')
    list_filter = ('status', 'priority', 'department', 'dashboard_date')
    search_fields = ('description', 'location_name', 'citizin__name', 'assigned_employee__name')
    readonly_fields = ('created_at', 'completed_at')
    
    fieldsets = (
        ('Main Info', {
            'fields': ('description', 'status', 'priority', 'department')
        }),
        ('Location', {
            'fields': ('location_name', 'latlatitude', 'longitude', 'location_confirmation')
        }),
        ('Assignment', {
            'fields': ('citizin', 'assigned_employee')
        }),
        ('AI Analysis & Photos', {
            'fields': (
                'image_before_analysis', 'ai_analysis_label_before',
                'image_after_analysis', 'ai_analysis_label_after',
                'what_was_done'
            )
        }),
        ('Dates', {
            'fields': ('created_at', 'dashboard_date', 'completed_at')
        }),
    )

@admin.register(OperatorNotification)
class OperatorNotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'operator', 'sender_employee', 'incidence', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at', 'priority')
    search_fields = ('employee_name', 'employee_email', 'location_name')
    readonly_fields = ('created_at',)