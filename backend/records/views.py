from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from .models import Hospital, Patient, MedicalRecord, Prescription, OTP, PasswordResetToken
from .serializers import (
    HospitalSerializer,
    PatientSerializer,
    MedicalRecordSerializer,
    PrescriptionSerializer
)

class HospitalLoginView(APIView):
    def post(self, request):
        hospital_id = request.data.get('hospitalId')
        password = request.data.get('password')

        hospital = authenticate(request, hospital_id=hospital_id, password=password)
        if hospital is not None:
            refresh = RefreshToken.for_user(hospital)
            return Response({
                'token': str(refresh.access_token),
                'hospitalId': hospital.hospital_id,
                'name': hospital.name
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class PatientLoginView(APIView):
    def post(self, request):
        aadhaar = request.data.get('aadhaar')
        otp = request.data.get('otp')

        # Mock OTP verification - accept "123456" or any OTP from database
        try:
            otp_record = OTP.objects.filter(aadhaar=aadhaar, is_used=False).latest('created_at')
            if otp == "123456" or otp_record.otp == otp:
                # Mark OTP as used
                otp_record.is_used = True
                otp_record.save()

                try:
                    patient = Patient.objects.get(aadhaar=aadhaar)
                    refresh = RefreshToken.for_user(patient)
                    return Response({
                        'token': str(refresh.access_token),
                        'aadhaar': patient.aadhaar,
                        'name': patient.name
                    }, status=status.HTTP_200_OK)
                except Patient.DoesNotExist:
                    return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
        except OTP.DoesNotExist:
            return Response({'error': 'OTP not found or expired'}, status=status.HTTP_404_NOT_FOUND)

class ForgotPasswordView(APIView):
    def post(self, request):
        aadhaar = request.data.get('aadhaar')
        
        try:
            patient = Patient.objects.get(aadhaar=aadhaar)
            # Generate and save reset token
            reset_token = PasswordResetToken.objects.create(aadhaar=aadhaar)
            
            # In a real implementation, send email with reset link
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token.token}"
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [patient.email],
                fail_silently=False,
            )
            
            return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

class HospitalPatientsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            hospital = Hospital.objects.get(hospital_id=request.user.hospital_id)
            patients = Patient.objects.filter(hospital=hospital)
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Hospital.DoesNotExist:
            return Response({'error': 'Hospital not found'}, status=status.HTTP_404_NOT_FOUND)

class PatientRecordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            patient = Patient.objects.get(aadhaar=request.user.aadhaar)
            records = MedicalRecord.objects.filter(patient=patient)
            prescriptions = Prescription.objects.filter(patient=patient)
            
            records_serializer = MedicalRecordSerializer(records, many=True)
            prescriptions_serializer = PrescriptionSerializer(prescriptions, many=True)
            
            return Response({
                'medical_records': records_serializer.data,
                'prescriptions': prescriptions_serializer.data
            }, status=status.HTTP_200_OK)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

class SendOTPView(APIView):
    def post(self, request):
        aadhaar = request.data.get('aadhaar')
        
        # Mock OTP implementation - always use "123456" in development
        otp = "123456"
        OTP.objects.create(aadhaar=aadhaar, otp=otp)
        
        # Log mock OTP (in production, this would send via SMS)
        print(f"Mock OTP for {aadhaar}: {otp} (always use this for testing)")
        
        return Response({
            'message': 'OTP sent successfully',
            'mock_otp': otp  # Return mock OTP for development convenience
        }, status=status.HTTP_200_OK)
