# customization/urls.py
from django.urls import path
from .views import customize_routine_view

urlpatterns = [
    path('customize-routine/', customize_routine_view, name='customize_routine'),

]
