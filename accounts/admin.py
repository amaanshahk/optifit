# accounts/admin.py
from django.contrib import admin
from .models import SquatCustomization, BicepCurlCustomization

admin.site.register(SquatCustomization)
admin.site.register(BicepCurlCustomization)
