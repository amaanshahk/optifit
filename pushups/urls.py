# pushups/urls.py
from django.urls import path
from .views import index, video_feed

app_name = 'pushups'  # This sets the namespace for the app

urlpatterns = [
    path('', index, name='pushups_index'),
    path('video_feed/', video_feed, name='pushups_video_feed'),  # Add a trailing slash
]
