from django.urls import path
from .views import workout_settings

urlpatterns = [
    path('settings/', workout_settings, name='workout_settings'),
    # Add other URLs as needed
]
