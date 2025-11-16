from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.doctor_login, name='doctor-login'),
    path('logout/', views.doctor_logout, name='doctor-logout'),
]