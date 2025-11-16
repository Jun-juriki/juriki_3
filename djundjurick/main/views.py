# main/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Patient
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request, 'main/main.html')
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'main/patient_detail.html', {'patient': patient})

class PatientListView(ListView):
    model = Patient
    template_name = 'main/patient_list.html'
    context_object_name = 'patients'

    def get_queryset(self):
        queryset = Patient.objects.filter(is_active=True)

        # Фильтрация по уровню срочности
        urgency_filter = self.request.GET.get('urgency')
        if urgency_filter and urgency_filter in ['1', '2', '3', '4']:
            queryset = queryset.filter(urgency_level=int(urgency_filter))

        # Сортировка по уровню срочности
        return queryset.order_by('urgency_level', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_urgency'] = self.request.GET.get('urgency', '')
        return context


def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, encrypted_id=patient_id, is_active=True)

    context = {
        'patient': patient,
        'visits': patient.get_visits()
    }
    return render(request, 'main/patient_detail.html', context)


@login_required
def queue_view(request):
    """Страница очереди пациентов с расписанием"""
    # Получаем активных пациентов, отсортированных по неотложности
    patients = Patient.objects.filter(is_active=True).order_by('-emergency_criteria')

    # Создаем расписание с 12:00 с интервалом 1 час
    start_time = datetime.strptime('12:00', '%H:%M')
    schedule = []

    for i, patient in enumerate(patients):
        appointment_time = (start_time + timedelta(hours=i)).strftime('%H:%M')
        schedule.append({
            'patient': patient,
            'appointment_time': appointment_time,
            'time_slot': i + 1  # номер временного слота
        })

    context = {
        'schedule': schedule,
        'total_patients': len(patients)
    }

    return render(request, 'main/queue.html', context)