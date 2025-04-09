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

[Rest of the models remain the same...]