from time import sleep
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import *
from .models import Club
from django.dispatch import receiver

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
    
    return render(request, 'webClassDisplay.html', context)

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

# Triggered when no custom club redirect for their homepage exists
# TODO make custom 404 page
def club_home_default(request):

    # Assumes each club has its own name
    className = request.GET.get('className')

    context = {
        'club': Club.objects.get(name = className)
    }

    return render(request, "clubHomeDefault.html", context)

def registerUser(request):
    if request.user.is_authenticated:
        user, created = User.objects.get_or_create(
        name = request.user.first_name,
        email = request.user.email
        )

        if created:
            # redirects user to a certain page if the account was just created
            return redirect("/clubs") # change this to a success screen or something
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
    
def leaveClub(request):
    if request.user.is_authenticated:
        className = request.GET.get('clubName')
        Club.objects.get(name = className).users.remove(User.objects.get(email = request.user.email))
        return redirect("/myClubs")
    else:
        return redirect("/")  



@receiver
def populate_profile(sociallogin, user, **kwargs):      

    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        picture_url = user.socialaccount_set.filter(provider='google')[0].extra_data['picture']           
        email = user_data['email']
        first_name = user_data['first_name']

    user, created = User.objects.get_or_create(
    name = first_name,
    email = email
    
    )


    user.profile.avatar_url = picture_url
    user.profile.email_address = email
    user.profile.first_name = first_name
    user.profile.save()      