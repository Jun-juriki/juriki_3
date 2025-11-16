from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DoctorLoginForm


def doctor_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = DoctorLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Добро пожаловать, {user.get_full_name()}!')

                    # Перенаправление на следующую страницу или по умолчанию на главную
                    next_url = request.GET.get('next', 'index')
                    return redirect(next_url)
                else:
                    messages.error(request, 'Ваш аккаунт деактивирован. Обратитесь к администратору.')
            else:
                messages.error(request, 'Неверный логин или пароль')
    else:
        form = DoctorLoginForm()

    return render(request, 'main/login.html', {'form': form})


@login_required
def doctor_logout(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы')
    return redirect('index')


# Защищаем основные views декоратором login_required
@login_required
def index(request):
    return render(request, 'main/index.html')


@login_required
def patient_list(request):
    from djundjurick.main.models import Patient
    patients = Patient.objects.all()
    return render(request, 'main/patient_list.html', {'patients': patients})


@login_required
def patient_detail(request, patient_id):
    from djundjurick.main.models import Patient
    from django.shortcuts import get_object_or_404

    patient = get_object_or_404(Patient, id=patient_id)
    context = {
        'patient': patient,
        'visits': patient.get_visits() if hasattr(patient, 'get_visits') else []
    }
    return render(request, 'main/patient_detail.html', context)
