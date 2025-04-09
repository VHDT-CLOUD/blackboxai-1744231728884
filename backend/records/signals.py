from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Patient, MedicalRecord, Prescription, PasswordResetToken
import os

@receiver(post_save, sender=Patient)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Secure Medical Records'
        message = f"""
        Dear {instance.name},
        
        Your medical records account has been created successfully.
        Aadhaar: {instance.aadhaar}
        Hospital: {instance.hospital.name}
        
        You can now access your medical records through our secure portal.
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )

@receiver(pre_save, sender=MedicalRecord)
def validate_medical_record(sender, instance, **kwargs):
    if not instance.title:
        instance.title = f"Medical Report - {instance.created_at.strftime('%Y-%m-%d')}"

@receiver(pre_delete, sender=MedicalRecord)
def delete_report_file(sender, instance, **kwargs):
    if instance.report_file:
        if os.path.isfile(instance.report_file.path):
            os.remove(instance.report_file.path)

@receiver(post_save, sender=PasswordResetToken)
def send_password_reset_email(sender, instance, created, **kwargs):
    if created:
        try:
            patient = Patient.objects.get(aadhaar=instance.aadhaar)
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={instance.token}"
            
            subject = 'Password Reset Request'
            message = f"""
            Dear {patient.name},
            
            You requested a password reset for your medical records account.
            Please click the link below to reset your password:
            
            {reset_link}
            
            This link will expire in 24 hours.
            """
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [patient.email],
                fail_silently=False,
            )
        except Patient.DoesNotExist:
            pass

@receiver(post_save, sender=Prescription)
def notify_patient_prescription(sender, instance, created, **kwargs):
    if created:
        subject = 'New Prescription Issued'
        message = f"""
        Dear {instance.patient.name},
        
        A new prescription has been issued for you:
        
        Medication: {instance.medication}
        Dosage: {instance.dosage}
        Doctor: {instance.doctor_name}
        Valid Until: {instance.valid_until.strftime('%Y-%m-%d')}
        
        Instructions:
        {instance.instructions}
        """
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.patient.email],
            fail_silently=False,
        )