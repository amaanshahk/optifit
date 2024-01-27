# customization/views.py
from django.shortcuts import render, redirect, get_object_or_404
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

        # Add more workout
        if 'add_more_workout' in request.POST:
            if form.is_valid():
                order = routine.workout_set.count() + 1
                workout = form.save(commit=False)
                workout.routine = routine
                workout.order = order
                workout.save()

        # Remove workout
        elif 'remove_workout' in request.POST:
            workout_id = request.POST['remove_workout']
            workout = get_object_or_404(Workout, id=workout_id, routine=routine)
            workout.delete()

        # Save routine
        elif 'save_routine' in request.POST:
            return redirect('customize_routine')  # Redirect to refresh the page after submission
    else:
        form = WorkoutForm()

    workouts = routine.workout_set.all()

    return render(request, 'customization/customize_routine.html', {'form': form, 'workouts': workouts})
