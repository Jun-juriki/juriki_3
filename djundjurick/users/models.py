# backend/apps/users/models.py
from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название отделения")
    code = models.CharField(max_length=10, unique=True, verbose_name="Код отделения")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Отделение"
        verbose_name_plural = "Отделения"


class MedicalStaff(models.Model):
    SPECIALIZATION_CHOICES = [
        ('therapist', 'Терапевт'),
        ('surgeon', 'Хирург'),
        ('cardiologist', 'Кардиолог'),
        ('neurologist', 'Невролог'),
        ('traumatologist', 'Травматолог'),
        ('pediatrician', 'Педиатр'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Отделение")
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, verbose_name="Специализация")
    license_number = models.CharField(max_length=50, unique=True, verbose_name="Номер лицензии")

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_specialization_display()}"

    class Meta:
        verbose_name = "Медицинский работник"
        verbose_name_plural = "Медицинские работники"
