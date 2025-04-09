from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import uuid

class HospitalManager(BaseUserManager):
    def create_user(self, hospital_id, password=None, **extra_fields):
        if not hospital_id:
            raise ValueError('Hospital ID is required')
        user = self.model(hospital_id=hospital_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, hospital_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(hospital_id, password, **extra_fields)

class Hospital(AbstractBaseUser, PermissionsMixin):
    hospital_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    # Add unique related_name for groups and permissions
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this hospital belongs to.',
        related_name="hospital_groups",
        related_query_name="hospital",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this hospital.',
        related_name="hospital_permissions",
        related_query_name="hospital",
    )


    objects = HospitalManager()

    USERNAME_FIELD = 'hospital_id'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name

class Patient(models.Model):
    aadhaar = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=3)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='patients')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.aadhaar})"

class MedicalRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    report_file = models.FileField(upload_to='medical_reports/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.patient.name}"

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor_name = models.CharField(max_length=100)
    medication = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    instructions = models.TextField()
    issue_date = models.DateField()
    valid_until = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medication} for {self.patient.name}"

class OTP(models.Model):
    aadhaar = models.CharField(max_length=12)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"OTP for {self.aadhaar}"

class PasswordResetToken(models.Model):
    aadhaar = models.CharField(max_length=12)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Reset token for {self.aadhaar}"