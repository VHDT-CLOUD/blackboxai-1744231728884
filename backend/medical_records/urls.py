from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from records.views import (
    HospitalLoginView,
    PatientLoginView,
    ForgotPasswordView,
    HospitalPatientsView,
    PatientRecordsView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication Endpoints
    path('api/hospital-login/', HospitalLoginView.as_view(), name='hospital-login'),
    path('api/patient-login/', PatientLoginView.as_view(), name='patient-login'),
    path('api/forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Hospital Endpoints
    path('api/hospital/patients/', HospitalPatientsView.as_view(), name='hospital-patients'),
    
    # Patient Endpoints
    path('api/patient/records/', PatientRecordsView.as_view(), name='patient-records'),
    
    # Include DRF auth URLs
    path('api-auth/', include('rest_framework.urls')),
]