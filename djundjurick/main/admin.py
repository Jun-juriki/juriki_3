# backend/apps/main/admin.py
from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['encrypted_id', 'urgency_level', 'diagnosis', 'created_at']
    list_filter = ['urgency_level', 'is_active']
    ordering = ['urgency_level']

