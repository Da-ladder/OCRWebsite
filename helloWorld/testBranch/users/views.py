from time import sleep
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import *
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
import re

def mobile(request):
    #Return True if the request comes from a mobile device.
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        return True
    else:
        return False

def home(request):
    if request.user.is_authenticated:
        pic_url = Users.objects.get(email = request.user.email).picURL
        if mobile(request):
            return render(request, 'mobileDisplay/mobileLogIn.html', {'pic': pic_url})
        else:
            return render(request, 'home.html', {'pic': pic_url})

    else:
        if mobile(request):
            return render(request, 'mobileDisplay/mobileLogIn.html')
        else:
            return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect("/")

def club_display_new(request):
    # get all clubs and put them in a dictionary where each club will have tags related to them seperated
    # by ",  " for easy deciper on the js side
    clubsWithCategory = {}
    
    clubs = Club.objects.all()
    for club in clubs:
        ClubTagStr = ""

        # Gets the tag field
        field_object = Club._meta.get_field('tagOrTags')
        field_value = field_object.value_from_object(club)

        # Breaks it down into a single string 
        for val in field_value:
            if (len(ClubTagStr) != 0):
                ClubTagStr += ",  "  # seperated by two spaces after comma
            ClubTagStr += str(val)
        
        clubsWithCategory[club] = ClubTagStr

    # Buttons are dynamically added so all tags are taken from the database
    tags = ClubTag.objects.all()


    if request.user.is_authenticated:
        context = {
            'clubsWithCategory': clubsWithCategory,
            'tags' : tags,
            'pic': Users.objects.get(email = request.user.email).picURL,
        }
    else:
        context = {
            'clubsWithCategory': clubsWithCategory,
            'tags' : tags,
        }

    if mobile(request):
        #ignore mobile for now
        return club_display(request)
    else:
        return render(request, 'desktopDisplay/explore.html', context)
    
    
    


    

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

    if mobile(request):
        return render(request, 'mobileDisplay/mobileClassDisplay.html', context)
    else:
        return render(request, 'webClassDisplay.html', context)

def dis_my_clubs(request):
    if request.user.is_authenticated:
        clubs = Club.objects.filter(users=Users.objects.get(email = request.user.email))
        pic_url = Users.objects.get(email = request.user.email).picURL

        if mobile(request):
            return render(request, 'mobileDisplay/mobileHome.html', {'classes': clubs, 'pic': pic_url})
        else:
            return render(request, 'myClubs.html', {'classes': clubs, 'pic': pic_url})
    else:
        return redirect("/")


# Triggered when no custom club redirect exists
# TODO make custom 404 page
def club_default(request):

    # Assumes each club has its own name
    className = request.GET.get('className')
    club = Club.objects.get(name = className)

    if request.user.is_authenticated and club.advisors.filter(email = request.user.email).exists():
        context = {
            'club': club,
            'edit' : True,
        }
    else:
        context = {
            'club': club,
            'edit': False,
        }

    if mobile(request):
        return render(request, "mobileDisplay/mobileClubFrontDefault.html", context)
    else:
        return render(request, "clubDefault.html", context)

# Triggered when no custom club redirect for their homepage exists
# TODO make custom 404 page
def club_home_default(request):

    # Assumes each club has its own name
    className = request.GET.get('className')

    context = {
        'club': Club.objects.get(name = className)
    }

    if mobile(request):
        return render(request, "mobileDisplay/mobileClubJoinedDefault.html", context)
    else:
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

def club_edit(request):
    className = request.GET.get('clubName')

    club = Club.objects.get(name = className)

    # gets all the tags that the club is tagged to (get it?)
    ClubTagStr = ""

    # Gets the tag field
    field_object = Club._meta.get_field('tagOrTags')
    currTags = field_object.value_from_object(club)
    

    # get all tags from the database
    tags = ClubTag.objects.all()

    if request.user.is_authenticated and club.advisors.filter(email = request.user.email).exists():
        context = {
            'tags': tags,
            'currTags': currTags,
            'club': club,
            'edit' : True,
        }
        return render(request, "clubEditDefault.html", context)
    else:
        return render(request, "NuhUh.html")

def changeClub(request):
    className = request.POST.get('clubName')
    classAbout = request.POST.get('about')
    classSchedule = request.POST.get('schedule')
    classLoc = request.POST.get('location')
    classContact = request.POST.get('contacts')
    classAdvisor = request.POST.get('advisors')
    picURL = request.POST.get("picURL")
    tags = request.POST.get("tags")

    club = Club.objects.get(name = className)

    if request.user.is_authenticated and club.advisors.filter(email = request.user.email).exists(): #change this later
        club.discription = classAbout
        club.contact = classContact
        club.generalMeets = classSchedule
        club.location = classLoc
        club.advisorOrAdvisors = classAdvisor
        club.homeURL = picURL

        # setting the many to many field using the tag names directly
        tags = tags.split(",  ")
        tags = ClubTag.objects.filter(name__in=tags)
        club.tagOrTags.set(tags)
        return redirect("/clubs")
    else:
        return render(request, "NuhUh.html")


# TODO: fix issue with always trigger upon signing in
@receiver(user_signed_up)
def populate_profile(sociallogin, user, **kwargs):      

    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        picture_url = user.socialaccount_set.filter(provider='google')[0].extra_data['picture']           
        email = user_data['email']
        first_name = user.first_name

    Users.objects.get_or_create(
    name = first_name,
    email = email,
    picURL = picture_url,
    extraData = user_data
    )