# main/models.py
from django.db import models


class Patient(models.Model):
    encrypted_id = models.CharField(max_length=50, unique=True, verbose_name="ID пациента")
    encrypted_name = models.TextField(verbose_name="Зашифрованное имя пациента")


    diagnosis = models.TextField(blank=True, verbose_name="Диагноз")
    icd10_codes = models.TextField(blank=True, verbose_name="Коды МКБ-10")


    urgency_level = models.IntegerField(default=4, verbose_name="Уровень срочности (1-4)")

    clinical_route = models.JSONField(default=dict, verbose_name="Клинический маршрут")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['urgency_level', '-created_at']  # Сортировка по уровню срочности и дате создания

    def __str__(self):
        return f"Пациент {self.encrypted_id} (Ур.{self.urgency_level})"

    def get_urgency_display(self):
        urgency_map = {
            1: '🔴 Критический',
            2: '🟠 Высокий',
            3: '🟡 Средний',
            4: '🟢 Низкий',
        }
        return urgency_map.get(self.urgency_level, '⚪ Неизвестно')


