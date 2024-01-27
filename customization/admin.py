# customization/admin.py
from django.contrib import admin
from .models import Routine, Workout

admin.site.register(Routine)
admin.site.register(Workout)
