from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.admin import register
from django.contrib.admin import TabularInline
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from .models import (Patient, Psychologist, Sessions,)


@register(Patient)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name',
        'language', 'telegram_nickname', 'phone',
        'email',
    )
    fieldsets = [
        (None, {'fields': ['username', 'password']}),
        ('Personal info', {'fields': ['first_name', 'last_name',
                                      'language', 'date_of_birth']}),
        ('Contacts', {'fields': ['telegram_nickname', 'phone',
                                 'email', ]}),
        ('Appointment details', {'fields': ['problem_type', 'assigned_id',
                                            'priority', 'processed',
                                 'processed_time', 'approved_time']}),
        # ('Permissions', {'fields': ['groups', 'is_staff']}, ),
    ]
    search_fields = (
        'username', 'first_name', 'last_name',
    )
    list_filter = (
        'username', 'first_name', 'last_name',
    )
    empty_value_display = '-none-'
    ordering = ['username']


@register(Psychologist)
class MyUserAdmin(UserAdmin):
    list_display = (
        'username', 'first_name', 'last_name',
        'language', 'telegram_nickname', 'phone',
        'email',
    )
    fieldsets = [
        (None, {'fields': ['username', 'password']}),
        ('Personal info', {'fields': ['first_name', 'last_name',
                                      'language', 'date_of_birth']}),
        ('Contacts', {'fields': ['telegram_nickname', 'phone',
                                 'email', ]}),
        ('Appointment details', {'fields': ['time_table_id']}),
        ('Permissions', {'fields': ['groups', 'is_staff']}, ),
    ]
    search_fields = (
        'username', 'first_name', 'last_name',
    )
    list_filter = (
        'username', 'first_name', 'last_name',
    )
    empty_value_display = '-none-'
    ordering = ['username']


@register(Sessions)
class SessionsAdmin(ModelAdmin):
    list_display = (
        'psychologists', 'patient', 'date_time',
        'session_type', 'language',
    )
    search_fields = (
        'psychologists', 'patient',
    )
    list_filter = (
        'psychologists', 'patient',
    )
    empty_value_display = '-none-'
    ordering = ['psychologists']
