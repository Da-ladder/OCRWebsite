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

    
    return render(request, 'mobileDisplay/mobileClassDisplay.html', context)

def dis_my_clubs(request):
    if request.user.is_authenticated:
        # if club list is blank, give context so that it is known to be empty
        empty = False
        clubs = Club.objects.filter(users=Users.objects.get(email = request.user.email))
        if len(clubs) == 0:
            empty = True

        # give needed context to templates
        context = {
            'classes': clubs,
            'pic': Users.objects.get(email = request.user.email).picURL,
            'empty': empty,
        }

        if mobile(request):
            return render(request, 'mobileDisplay/mobileHome.html', context)
        else:
            return render(request, 'desktopDisplay/myClubs.html', context)
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
        return render(request, "desktopDisplay/clubDefault.html", context)

# Triggered when no custom club redirect for their homepage exists
# TODO make custom 404 page
def club_home_default(request):

    # Assumes each club has its own name
    className = request.GET.get('className')
    club = Club.objects.get(name = className)

    context = {
        'club': club
    }

    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):
        if mobile(request):
            return render(request, "mobileDisplay/mobileClubJoinedDefault.html", context)
        else:
            return render(request, "clubHomeDefault.html", context)
    else:
        return render(request, "NuhUh.html")
    

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

    # gets current leaders and users
    users = club.users.all()

    leaders = club.leaders.all()

    if request.user.is_authenticated and club.advisors.filter(email = request.user.email).exists():
        context = {
            'tags': tags,
            'users': users,
            'leaders': leaders,
            'currTags': currTags,
            'club': club,
            'editUsers' : True,
        }
        return render(request, "clubEditDefault.html", context)
    elif request.user.is_authenticated and club.leaders.filter(email = request.user.email).exists():
        context = {
            'tags': tags,
            'currTags': currTags,
            'club': club,
            'editUsers' : False, # to be implemented
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
    clubUsers = request.POST.get("users")
    clubLeaders = request.POST.get("leaders")

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
        tags = ClubTag.objects.filter(name__in = tags)
        club.tagOrTags.set(tags)

        # setting the many to many field using the user emails directly
        clubUsers = clubUsers.split(",  ")
        clubUsers = Users.objects.filter(email__in = clubUsers)
        club.users.set(clubUsers)

        # setting the many to many field using the leaders emails directly
        clubLeaders = clubLeaders.split(",  ")
        clubLeaders = Users.objects.filter(email__in = clubLeaders)
        club.leaders.set(clubLeaders)

        club.save()
        return redirect("/clubs")
    else:
        return render(request, "NuhUh.html")

def addClubPost(request):
    
    # Grab information
    currentPage = request.POST.get('curPage')

    club = Club.objects.get(name = request.POST.get("clubName"))
    postTitle = request.POST.get("title")
    postBody = request.POST.get("body")

    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):
        # Make the post
        LiveFeed.objects.create(
        title = postTitle,
        text = postBody,
        club = club,
        edited = False,
        creator = Users.objects.get(email = request.user.email)
        )

        # return them to the page they were on
        return redirect(currentPage)
    else:
        # if they do not have access, deny them
        return render(request, "NuhUh.html")

def deleteClubPost(request):
    
    # get required information to delete post
    currentPage = request.POST.get("curPage")

    # We will get the club by tracing back from the post in order to ensure that
    # malicious actors can not delete posts from other clubs
    club = Club.objects.get(name = request.POST.get("clubName"))
    postKey = request.POST.get("postKey")

    # get the post to be deleted
    post = LiveFeed.objects.get(id = postKey)

    # where we get the verifed club
    club = Club.objects.get(name = post.club.name)

    # users will be able to delete their own posts
    # advisors and leaders will be able to delete any posts
    if request.user.is_authenticated and (post.creator.email == request.user.email 
        or club.advisors.filter(email = request.user.email).exists() 
        or club.leaders.filter(email = request.user.email).exists()):
        # Delete the post
        post.delete()

        # return them to the page they were on
        return redirect(currentPage)
    else:
        # if they do not have access, deny them
        return render(request, "NuhUh.html")






# custom club homepages are created below
# change from localhost to dhsclubs.org when pushing updates
def nehsInternalHome(request):
    club = Club.objects.get(name = "National English Honor Society (NEHS)")


    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):

        # gets all posts for the club
        posts = LiveFeed.objects.filter(club = club)

        context = {
            'posts': posts,
            'club': club,
            'userPic': Users.objects.get(email = request.user.email).picURL,
        }

        if mobile(request):
            # ignore mobile layout for now
            return render(request, "mobileDisplay/Nehs/internalHome.html", context)
        else:
            return render(request, "desktopDisplay/Nehs/internalHome.html", context)
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