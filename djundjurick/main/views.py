# main/views.py
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Patient


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