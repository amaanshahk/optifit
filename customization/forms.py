# customization/forms.py
from django import forms
from .models import Workout

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['exercise', 'rep_count', 'time_limit_seconds']
