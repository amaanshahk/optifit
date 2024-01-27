from django.shortcuts import render
from .models import WorkoutSettings

def workout_settings(request):
    workout_data = WorkoutSettings.objects.all()
    return render(request, 'workout/settings.html', {'workout_data': workout_data})
