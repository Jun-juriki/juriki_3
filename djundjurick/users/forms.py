from django import forms
from django.contrib.auth.forms import AuthenticationForm

class DoctorLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш логин',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш пароль',
            'autocomplete': 'current-password'
        })
    )