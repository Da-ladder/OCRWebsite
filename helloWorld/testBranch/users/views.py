from time import sleep
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import *
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

def home(request):
    if request.user.is_authenticated:
        pic_url = Users.objects.get(email = request.user.email).picURL
        return render(request, 'home.html', {'pic': pic_url})
    else:
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
    
    if request.user.is_authenticated:
        context = {
            'clubs_by_category': clubs_by_category,
            'pic': Users.objects.get(email = request.user.email).picURL,
        }
    else:
        context = {
            'clubs_by_category': clubs_by_category
        }
    
    return render(request, 'webClassDisplay.html', context)

def dis_my_clubs(request):
    if request.user.is_authenticated:
        clubs = Club.objects.filter(users=Users.objects.get(email = request.user.email))
        pic_url = Users.objects.get(email = request.user.email).picURL
        return render(request, 'myClubs.html', {'classes': clubs, 'pic': pic_url})
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

# Triggered when no custom club redirect for their homepage exists
# TODO make custom 404 page
def club_home_default(request):

    # Assumes each club has its own name
    className = request.GET.get('className')

    context = {
        'club': Club.objects.get(name = className)
    }

    return render(request, "clubHomeDefault.html", context)

def registerUserAs(request):
    # can be removed in the future
    return redirect("/clubs")

def joinClub(request):
    if request.user.is_authenticated:
        className = request.GET.get('clubName')
        Club.objects.get(name = className).users.add(Users.objects.get(email = request.user.email))
        return redirect("/clubs")
    else:
        return redirect("/")
    
def leaveClub(request):
    if request.user.is_authenticated:
        className = request.GET.get('clubName')
        Club.objects.get(name = className).users.remove(Users.objects.get(email = request.user.email))
        return redirect("/myClubs")
    else:
        return redirect("/")  



@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):      

    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        picture_url = user.socialaccount_set.filter(provider='google')[0].extra_data['picture']           
        email = user_data['email']
        first_name = user.first_name

    Users.objects.create(
    name = first_name,
    email = email,
    picURL = picture_url,
    extraData = user_data
    )