# customization/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WorkoutForm
from .models import Routine, Workout

@login_required
def customize_routine_view(request):
    routines = Routine.objects.filter(user=request.user)

    # Create a new routine if the user doesn't have any
    if not routines.exists():
        routine = Routine.objects.create(user=request.user)
    else:
        routine = routines.first()

    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if 'add_more_workout' in request.POST:
            # Add more workout
            if form.is_valid():
                order = routine.workout_set.count() + 1
                workout = form.save(commit=False)
                workout.routine = routine
                workout.order = order
                workout.save()
        elif 'save_routine' in request.POST:
            # Save routine
            return redirect('customize_routine')  # Redirect to refresh the page after submission
    else:
        form = WorkoutForm()

    workouts = routine.workout_set.all()

    return render(request, 'customization/customize_routine.html', {'form': form, 'workouts': workouts})
