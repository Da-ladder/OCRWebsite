from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import *

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def club_display(request):
    clubs = Club.objects.all()
    return render(request, 'classDisplay.html', {'classes': clubs})


# Create your views here.
