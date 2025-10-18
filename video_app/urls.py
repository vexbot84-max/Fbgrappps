from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),                         # Home page
    path("video-info/", views.fetch_video, name="fetch_video"),  # Fetch video info from API
    path("download/", views.download_video, name="download_video"),  # Download/stream video
]
