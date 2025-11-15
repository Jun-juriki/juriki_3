# main/models.py
from django.db import models
from django.utils import timezone

class Patient(models.Model):
    encrypted_id = models.CharField(max_length=50, unique=True, verbose_name="ID пациента")
    encrypted_name = models.TextField(verbose_name="Зашифрованное имя пациента")


    diagnosis = models.TextField(blank=True, verbose_name="Диагноз")
    icd10_codes = models.TextField(blank=True, verbose_name="Коды МКБ-10")
    hilling_doc=models.CharField(max_length=50, blank=True, verbose_name="Лечащий врач")


    urgency_level = models.IntegerField(default=4, verbose_name="Уровень срочности (1-4)")

    clinical_route = models.JSONField(default=dict, verbose_name="Клинический маршрут")

    visits_data = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Данные визитов"
    )

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

    def get_visits(self):
        """Получить список визитов"""
        return self.visits_data if self.visits_data else []

    def get_visits_count(self):
        """Получить количество визитов"""
        return len(self.get_visits())

    def get_last_visit(self):
        """Получить последний визит"""
        visits = self.get_visits()
        if visits:
            # Сортируем по дате (последние first)
            sorted_visits = sorted(visits, key=lambda x: x.get('visit_date', ''), reverse=True)
            return sorted_visits[0]
        return None

    def add_visit(self, visit_data):
        """Добавить визит"""
        if not self.visits_data:
            self.visits_data = []

        visit = {
            'id': len(self.visits_data) + 1,
            'visit_date': timezone.now().isoformat(),
            'created_at': timezone.now().isoformat(),
            **visit_data
        }

        self.visits_data.append(visit)
        self.save()
        return visit


