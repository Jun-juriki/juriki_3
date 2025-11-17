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


        urgency_filter = self.request.GET.get('urgency')
        if urgency_filter and urgency_filter in ['1', '2', '3', '4']:
            queryset = queryset.filter(urgency_level=int(urgency_filter))


        return queryset.order_by('urgency_level', '-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_urgency'] = self.request.GET.get('urgency', '')
        return context


@login_required
def doctor_chat(request, specialist):

    try:
        patient = Patient.objects.get(id=1)
    except Patient.DoesNotExist:

        patient = Patient(
            encrypted_id="DEMO001",
            encrypted_name="Иван Иванов",
            diagnosis="Ишемическая болезнь сердца",
            icd10_codes="I25.1",
            hilling_doc="Др. Петров",
            urgency_level=2,
            emergency_criteria=85
        )


    specialists_map = {
        'therapist': {
            'name': 'Терапевт',
            'color': 'primary',
            'scope': 'Общая диагностика, лечение распространенных заболеваний',
            'expertise': [
                'Дифференциальная диагностика',
                'Лечение ОРВИ и простудных заболеваний',
                'Ведение хронических заболеваний',
                'Профилактические осмотры'
            ],
            'examinations': [
                'Общий анализ крови и мочи',
                'Биохимический анализ крови',
                'Рентгенография органов грудной клетки',
                'ЭКГ'
            ]
        },
        'cardiologist': {
            'name': 'Кардиолог',
            'color': 'danger',
            'scope': 'Заболевания сердечно-сосудистой системы',
            'expertise': [
                'Диагностика ишемической болезни сердца',
                'Лечение артериальной гипертензии',
                'Нарушения ритма сердца',
                'Сердечная недостаточность'
            ],
            'examinations': [
                'Эхокардиография',
                'Суточный мониторинг ЭКГ',
                'Нагрузочные тесты',
                'Коронарография'
            ]
        },
        'surgeon': {
            'name': 'Хирург',
            'color': 'warning',
            'scope': 'Хирургические патологии, операции',
            'expertise': [
                'Экстренная хирургическая помощь',
                'Плановые оперативные вмешательства',
                'Послеоперационное ведение',
                'Гнойно-септические заболевания'
            ],
            'examinations': [
                'УЗИ брюшной полости',
                'КТ/МРТ органов',
                'Эндоскопические исследования',
                'Биопсия тканей'
            ]
        },
        'neurologist': {
            'name': 'Невролог',
            'color': 'info',
            'scope': 'Заболевания нервной системы',
            'expertise': [
                'Цереброваскулярные заболевания',
                'Эпилепсия и судорожные синдромы',
                'Неврологические осложнения',
                'Головные боли и мигрени'
            ],
            'examinations': [
                'МРТ головного мозга',
                'ЭЭГ (электроэнцефалография)',
                'УЗДГ сосудов головы и шеи',
                'Люмбальная пункция'
            ]
        },
    }

    specialist_info = specialists_map.get(specialist, {
        'name': 'Врач',
        'icon': '👨‍⚕️',
        'color': 'secondary',
        'scope': 'Медицинские консультации',
        'expertise': ['Медицинские консультации', 'Диагностика'],
        'examinations': ['Обследование по показаниям']
    })


    demo_messages = [
        {'sender': 'current',
         'text': f'Здравствуйте, коллега! Нужна консультация по пациенту {patient.encrypted_name}.', 'time': '10:30'},
        {'sender': specialist, 'text': f'Добрый день! Расскажите, в чём вопрос?', 'time': '10:31'},
        {'sender': 'current',
         'text': f'Пациент с жалобами на {get_complaints_by_specialist(specialist)}. Диагноз: {patient.diagnosis}.',
         'time': '10:32'},
        {'sender': specialist, 'text': f'Рекомендую {get_recommendations_by_specialist(specialist)}', 'time': '10:35'},
        {'sender': 'current', 'text': 'Спасибо за консультацию! Направлю пациента на указанные обследования.',
         'time': '10:36'},
    ]

    context = {
        'specialist': specialist,
        'specialist_info': specialist_info,
        'patient': patient,
        'messages': demo_messages,
        'all_specialists': specialists_map,
    }

    return render(request, 'main/doctor_chat.html', context)


def get_complaints_by_specialist(specialist):
    complaints = {
        'therapist': 'повышенную температуру и кашель',
        'cardiologist': 'боли в области сердца и одышку',
        'surgeon': 'острые боли в животе',
        'neurologist': 'головные боли и головокружение',
    }
    return complaints.get(specialist, 'состоянию пациента')


def get_recommendations_by_specialist(specialist):
    recommendations = {
        'therapist': 'сдать общий анализ крови и сделать рентген грудной клетки',
        'cardiologist': 'провести ЭКГ, ЭхоКГ и суточный мониторинг давления',
        'surgeon': 'сделать УЗИ брюшной полости и общий анализ крови',
        'neurologist': 'провести МРТ головного мозга и консультацию офтальмолога',
    }
    return recommendations.get(specialist, 'провести дополнительные обследования')
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, encrypted_id=patient_id, is_active=True)

    context = {
        'patient': patient,
        'visits': patient.get_visits()
    }
    return render(request, 'main/patient_detail.html', context)


@login_required
def queue_view(request):

    patients = Patient.objects.filter(is_active=True).order_by('-emergency_criteria')
    start_time = datetime.strptime('12:00', '%H:%M')
    schedule = []

    for i, patient in enumerate(patients):
        appointment_time = (start_time + timedelta(hours=i)).strftime('%H:%M')
        schedule.append({
            'patient': patient,
            'appointment_time': appointment_time,
            'time_slot': i + 1
        })

    context = {
        'schedule': schedule,
        'total_patients': len(patients)
    }

    return render(request, 'main/queue.html', context)