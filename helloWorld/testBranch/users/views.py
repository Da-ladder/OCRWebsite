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

# Triggered when no custom club redirect exists
# TODO make custom 404 page
def club_default(request):

    # Assumes each club has its own name
    className = request.GET.get('className')

    context = {
        'club': Club.objects.get(name = className)
    }

    return render(request, "clubDefault.html", context)

def test(request):
    return render(request, "tester.html")


# Create your views here.
