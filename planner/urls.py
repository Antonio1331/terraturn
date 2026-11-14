from django.urls import path
from . import views

urlpatterns = [
    path("", views.planner_dashboard, name="planner_dashboard"),
    path("api/v1/nasa-sync/", views.api_nasa_sync, name="nasa_sync"),
    path("api/v1/rotations/evaluate/", views.api_evaluate_rotations, name="evaluate_rotations"),
]