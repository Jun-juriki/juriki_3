from django.contrib.auth.models import AbstractUser
from django.db import models


class Doctor(AbstractUser):
    # Указываем уникальные related_name чтобы избежать конфликтов
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='doctor_set',  # Уникальный related_name
        related_query_name='doctor',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='doctor_set',  # Уникальный related_name
        related_query_name='doctor',
    )

    specialization = models.CharField(
        max_length=100,
        verbose_name="Специализация",
        help_text="Например: Кардиолог, Невролог, Терапевт"
    )

    department_name = models.CharField(
        max_length=150,
        verbose_name="Название отделения"
    )

    department_code = models.CharField(
        max_length=20,
        verbose_name="Код отделения"
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон"
    )

    license_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Номер медицинской лицензии"
    )

    is_verified = models.BooleanField(
        default=True,
        verbose_name="Верифицирован"
    )

    years_of_experience = models.IntegerField(
        default=0,
        verbose_name="Стаж работы (лет)"
    )

    bio = models.TextField(
        blank=True,
        verbose_name="О враче"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'
        ordering = ['department_name', 'specialization', 'last_name']

    def __str__(self):
        full_name = self.get_full_name()
        if full_name:
            return f"Др. {full_name} - {self.specialization} ({self.department_code})"
        return f"{self.username} - {self.specialization}"

    def get_short_info(self):
        """Краткая информация о враче"""
        return f"{self.specialization} | {self.department_name}"