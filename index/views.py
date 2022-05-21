from django.shortcuts import render
from django.views import View


def home_view(request):
    return render(request, 'index.html')
