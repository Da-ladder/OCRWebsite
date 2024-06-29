from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import *

def home(request):
    return render(request, "home.html")

def logout_view(request):
    logout(request)
    return redirect("/")

def club_display(request):
    clubs = Club.objects.all()
    return render(request, 'classDisplay.html', {'classes': clubs})

def dis_my_clubs(request):
    if request.user.is_authenticated:
        clubs = Club.objects.filter(users=User.objects.get(email = request.user.email))
        return render(request, 'myClubs.html', {'classes': clubs})
    else:
        return redirect("/")


# Triggered when no custom club redirect exists
# TODO make custom 404 page
def club_default(request):

    # Assumes each club has its own name
    className = request.GET.get('className')

    context = {
        'club': Club.objects.get(name = className)
    }

    return render(request, "clubDefault.html", context)

def registerUser(request):
    if request.user.is_authenticated:
        user, created = User.objects.get_or_create(
        name = request.user.first_name,
        email = request.user.email
        )

        if created:
            # redirects user to a certain page if the account was just created
            return render(request, 'test.html', {'content': user.email}) # change this to a success screen or something
        else:
            # gets user to the primary club page if they already have an account
            return redirect("/clubs")

    else:
        return redirect(request, "/")

def joinClub(request):
    if request.user.is_authenticated:
        className = request.GET.get('clubName')
        Club.objects.get(name = className).users.add(User.objects.get(email = request.user.email))
        return redirect("/clubs")
    else:
        return redirect("/")


# Create your views here.
