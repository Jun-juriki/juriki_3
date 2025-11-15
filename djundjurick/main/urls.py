from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # http://127.0.0.1:8000/
    path('patients/', views.PatientListView.as_view(), name='patient-list'),  # http://127.0.0.1:8000/patients/
    path('patients/<str:patient_id>/', views.patient_detail, name='patient-detail'),
]