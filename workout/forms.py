from django import forms
from .models import WorkoutSettings

class WorkoutSettingsForm(forms.ModelForm):
    class Meta:
        model = WorkoutSettings
        fields = ['rep_count', 'time_limit']


