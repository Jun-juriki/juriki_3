from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'specialization', 'department_name', 'is_staff', 'is_active')
    list_filter = ('specialization', 'department_name', 'is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'specialization')

    fieldsets = UserAdmin.fieldsets + (
        ('Профессиональная информация', {
            'fields': (
                'specialization',
                'department_name',
                'department_code',
                'phone',
                'license_number',
                'years_of_experience',
                'bio'
            )
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Профессиональная информация', {
            'fields': (
                'email',
                'first_name',
                'last_name',
                'specialization',
                'department_name',
                'department_code',
                'phone',
                'years_of_experience'
            )
        }),
    )