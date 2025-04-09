from rest_framework import serializers
from .models import Hospital, Patient, MedicalRecord, Prescription, OTP, PasswordResetToken
from django.contrib.auth.hashers import make_password

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['hospital_id', 'name', 'address', 'contact_number']
        extra_kwargs = {
            'hospital_id': {'read_only': True}
        }

class PatientSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'aadhaar', 
            'name', 
            'date_of_birth', 
            'blood_group', 
            'contact_number', 
            'address', 
            'hospital_name',
            'created_at'
        ]
        extra_kwargs = {
            'aadhaar': {'read_only': True},
            'created_at': {'read_only': True}
        }

class MedicalRecordSerializer(serializers.ModelSerializer):
    hospital_name = serializers.CharField(source='hospital.name', read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    report_url = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = [
            'id',
            'title',
            'description',
            'report_url',
            'hospital_name',
            'patient_name',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_report_url(self, obj):
        request = self.context.get('request')
        if obj.report_file and hasattr(obj.report_file, 'url'):
            return request.build_absolute_uri(obj.report_file.url)
        return None

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    patient_aadhaar = serializers.CharField(source='patient.aadhaar', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'patient_name',
            'patient_aadhaar',
            'doctor_name',
            'medication',
            'dosage',
            'instructions',
            'issue_date',
            'valid_until',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['aadhaar', 'otp', 'created_at']
        read_only_fields = ['created_at']

class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PasswordResetToken
        fields = ['aadhaar', 'token', 'created_at']
        read_only_fields = ['token', 'created_at']

class HospitalLoginSerializer(serializers.Serializer):
    hospital_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

class PatientLoginSerializer(serializers.Serializer):
    aadhaar = serializers.CharField()
    otp = serializers.CharField(write_only=True)

class ForgotPasswordSerializer(serializers.Serializer):
    aadhaar = serializers.CharField()