from django.urls import path
from .views import analyze_pr
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the PR Summarizer Bot!")

urlpatterns = [
    path('', home, name='home'),         # root URL
    path('analyze/', analyze_pr, name='analyze_pr'),
]
