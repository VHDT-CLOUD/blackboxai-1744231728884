from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Hospital, Patient, MedicalRecord, Prescription, OTP, PasswordResetToken

class HospitalAdmin(UserAdmin):
    list_display = ('hospital_id', 'name', 'address', 'contact_number', 'is_active')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('hospital_id', 'name')
    ordering = ('hospital_id',)
    fieldsets = (
        (None, {'fields': ('hospital_id', 'password')}),
        ('Hospital Info', {'fields': ('name', 'address', 'contact_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('hospital_id', 'name', 'password1', 'password2'),
        }),
    )

class PatientAdmin(admin.ModelAdmin):
    list_display = ('aadhaar', 'name', 'hospital', 'blood_group', 'contact_number')
    list_filter = ('hospital', 'blood_group')
    search_fields = ('aadhaar', 'name', 'contact_number')
    raw_id_fields = ('hospital',)

class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'hospital', 'created_at')
    list_filter = ('hospital', 'created_at')
    search_fields = ('patient__name', 'patient__aadhaar', 'title')
    raw_id_fields = ('patient', 'hospital')
    date_hierarchy = 'created_at'

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medication', 'patient', 'doctor_name', 'issue_date', 'valid_until')
    list_filter = ('issue_date', 'valid_until')
    search_fields = ('patient__name', 'patient__aadhaar', 'medication')
    raw_id_fields = ('patient',)
    date_hierarchy = 'issue_date'

class OTPAdmin(admin.ModelAdmin):
    list_display = ('aadhaar', 'otp', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('aadhaar',)
    date_hierarchy = 'created_at'

class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('aadhaar', 'token', 'created_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('aadhaar',)
    date_hierarchy = 'created_at'

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(MedicalRecord, MedicalRecordAdmin)
admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(OTP, OTPAdmin)
admin.site.register(PasswordResetToken, PasswordResetTokenAdmin)