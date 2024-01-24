# workout/urls.py
from django.urls import path
from .views import workout_settings

urlpatterns = [
    path('workout_settings/', workout_settings, name='workout_settings'),
]
