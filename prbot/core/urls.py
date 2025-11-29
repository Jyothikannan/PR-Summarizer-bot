from django.urls import path
from .views import analyze_pr

urlpatterns = [
    path("analyze/", analyze_pr, name="analyze_pr"),
]
