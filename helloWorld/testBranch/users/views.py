from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .models import *
from .models import Club

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def club_display(request):
    categories = [
        'STEM',
        'Chill & Relax',
        'Journalism & English',
        'Art',
        'Music & Theater',
        'Business, Finance & Medicine',
        'Other',
        'Debate & Other Humanities',
        'Activism/Community Service',
        'Language & Culture/Food',
        'Honor Societies',
    ]
    
    # Create a dictionary to store clubs filtered by each category
    clubs_by_category = {}
    for category in categories:
        clubs_by_category[category] = Club.objects.filter(tagOrTags__name=category)
    
    context = {
        'clubs_by_category': clubs_by_category
    }
    
    return render(request, 'classDisplay.html', context)

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


def club_list(request):
    clubs_by_category = {}

    # Fetch all unique categories
    categories = Club.objects.values_list('category', flat=True).distinct()

    # Fetch clubs for each category
    for category in categories:
        clubs_by_category[category] = Club.objects.filter(category=category)

    context = {
        'clubs_by_category': clubs_by_category
    }

    return render(request, 'club_list.html', context)


# Create your views here.
