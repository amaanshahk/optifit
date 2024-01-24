# workout/admin.py

from django.contrib import admin
from .models import WorkoutSettings

@admin.register(WorkoutSettings)
class WorkoutSettingsAdmin(admin.ModelAdmin):
    list_display = ['rep_count', 'time_limit']
