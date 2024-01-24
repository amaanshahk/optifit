# workout/views.py
from django.shortcuts import render, redirect
from .models import WorkoutSettings

def workout_settings(request):
    if request.method == 'POST':
        # Process and validate form data
        rep_count = request.POST.get('rep_count')
        time_limit = request.POST.get('time_limit')

        # Save to the database
        WorkoutSettings.objects.create(rep_count=rep_count, time_limit=time_limit)

        return redirect('workout_settings')  # Redirect to the same page after submission

    return render(request, 'workout/workout_settings.html')
