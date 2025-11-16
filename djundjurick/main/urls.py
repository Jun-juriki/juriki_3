from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('patients/', views.PatientListView.as_view(), name='patient-list'),
    path('patients/<str:patient_id>/', views.patient_detail, name='patient-detail'),
    path('queue/', views.queue_view, name='queue')
]