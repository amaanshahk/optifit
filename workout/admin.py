# workout/admin.py
from django.contrib import admin
from .models import WorkoutSettings

class WorkoutSettingsAdmin(admin.ModelAdmin):
    list_display = ('exercise_name', 'reps', 'time_limit')

# Register the model and admin class
admin.site.register(WorkoutSettings, WorkoutSettingsAdmin)
