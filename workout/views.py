# workout/views.py
from django.shortcuts import render

def workout_settings(request):
    # Add your view logic here
    return render(request, 'workout/workout_settings.html')  # Replace with the actual template name
