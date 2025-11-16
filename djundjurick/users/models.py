from django.contrib.auth.models import AbstractUser
from django.db import models


class Doctor(AbstractUser):

    specialization = models.CharField(
        max_length=100,
        verbose_name="Специализация"
    )


    department_name = models.CharField(
        max_length=150,
        verbose_name="Название отделения"
    )

    department_code = models.CharField(
        max_length=20,
        verbose_name="Код отделения",
        help_text="Внутренний код отделения"
    )

    # Контактная информация
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

    # Статус врача
    is_verified = models.BooleanField(
        default=False,
        verbose_name="Верифицирован администратором"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активный сотрудник"
    )

    # Дополнительные поля
    years_of_experience = models.IntegerField(
        default=0,
        verbose_name="Стаж работы (лет)"
    )

    bio = models.TextField(
        blank=True,
        verbose_name="О враче",
        help_text="Краткая информация о специализации и опыте"
    )

    # Автоматические поля
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
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
        return f"{self.specialization} | {self.department_name}"

    def save(self, *args, **kwargs):
        if not self.email and self.username:
            self.email = f"{self.username}@hospital.local"
        super().save(*args, **kwargs)