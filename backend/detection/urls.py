from django.urls import path
from . import views

urlpatterns = [
    path('detect/', views.detect_file, name='detect_file'),
    path('history/', views.get_detection_history, name='detection_history'),
]
