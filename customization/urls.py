# customization/urls.py
from django.urls import path
from .views import customize_routine_view, workout_redirect_view

urlpatterns = [
    path('customize-routine/', customize_routine_view, name='customize_routine'),
    path('workout_redirect/<str:exercise_name>/<int:rep_count>/<int:time_limit>/', workout_redirect_view, name='workout_redirect'),

]
