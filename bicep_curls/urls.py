from django.urls import path
from .views import index, video_feed

urlpatterns = [
    path('', index, name='bicep_curls_index'),
    path('video_feed/', video_feed, name='bicep_curls_video_feed'),
]
