# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')

# accounts/forms.py
from django import forms

class SquatCustomizationForm(forms.Form):
    rep_count_squat = forms.IntegerField(label='Rep Count for Squats')
    time_limit_squat = forms.IntegerField(label='Time Limit for Squats')

class BicepCurlCustomizationForm(forms.Form):
    rep_count_bicep_curl = forms.IntegerField(label='Rep Count for Bicep Curls')
    time_limit_bicep_curl = forms.IntegerField(label='Time Limit for Bicep Curls')

