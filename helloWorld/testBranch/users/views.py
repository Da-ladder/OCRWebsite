from time import sleep
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from .models import *
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from urllib.parse import urlencode  # Import urlencode
from django.conf import settings
from django.core.mail import send_mail
import re

def mobile(request):
    #Return True if the request comes from a mobile device.
    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    try:
        if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
            return True
        else:
            return False
    except:
        return True

def test(request):
    club = Club.objects.get(name = "Math Team")

    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):

        # gets all posts for the club
        posts = list(reversed(LiveFeed.objects.filter(club = club)))
        empty = False

        # will result in placeholder text if there is no posts
        if len(posts) == 0:
            empty = True

        # limits posts to leaders & advisors
        context = {
            'posts': posts,
            'club': club,
            'userPic': Users.objects.get(email = request.user.email).picURL,
            'postAbility': club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists(),
            "empty": empty
        }

        if mobile(request):
            return render(request, "mobileDisplay/ClubJoined.html", context)
        else:
            return render(request, "desktopDisplay/MathTeam/internalHome.html", context)
    else:
        return render(request, "NuhUh.html")

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
        return render(request, 'mobileDisplay/explore.html', context)
    else:
        return render(request, 'desktopDisplay/explore.html', context)
    

def dis_my_clubs(request):
    if request.user.is_authenticated:
        # if club list is blank, give context so that it is known to be empty
        empty = False

        # adds all clubs that they are a user, leader, or advisor of
        clubs = list(Club.objects.filter(users=Users.objects.get(email = request.user.email)))
        clubs += list(Club.objects.filter(leaders=Users.objects.get(email = request.user.email)))
        clubs += list(Club.objects.filter(advisors=Users.objects.get(email = request.user.email)))

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

    if request.user.is_authenticated and (club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):
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
        return render(request, "mobileDisplay/ClubFront.html", context)
    else:
        return render(request, "desktopDisplay/clubDefault.html", context)

# Triggered when no custom club redirect for their homepage exists
# TODO make custom 404 page
def club_home_default(request):

    # Assumes each club has its own name
    className = request.GET.get('className')
    club = Club.objects.get(name = className)

    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):

        # gets all posts for the club
        posts = list(reversed(LiveFeed.objects.filter(club = club)))
        empty = False

        # will result in placeholder text if there is no posts
        if len(posts) == 0:
            empty = True


        # limits posts to leaders & advisors
        context = {
            'posts': posts,
            'club': club,
            'userPic': Users.objects.get(email = request.user.email).picURL,
            'postAbility': club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists(),
            'empty': empty
        }

        if mobile(request):
            # ignore mobile layout for now
            return render(request, "mobileDisplay/ClubJoined.html", context)
        else:
            return render(request, "desktopDisplay/internalHomeDefault.html", context)
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

    if request.user.is_authenticated and club.advisors.filter(email = request.user.email).exists():
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
    elif request.user.is_authenticated and club.leaders.filter(email = request.user.email).exists():
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

        # get the creator
        creator = Users.objects.get(email = request.user.email)

        # Make the post
        LiveFeed.objects.create(
        title = postTitle,
        text = postBody,
        club = club,
        edited = False,
        creator = creator
        )

        # Email the message out (format it later)
        subject = creator.name.title() + ' posted in ' + club.name + " - " + postTitle
        message = subject + "\n" + postBody
        email_from = settings.EMAIL_HOST_USER

        emails = [user.email for user in club.users.all()] + [leader.email for leader in club.leaders.all()] + [advisor.email for advisor in club.advisors.all()]
        emails.remove(request.user.email)

        send_mail( subject, message, email_from, emails)

        # Allows for default pages to work with get requests
        if (currentPage == "/myClubs/default"):
            # TODO USE AJAX INSTEAD OF THIS STUFF 
            # Define GET parameters
            params = {'className': club.name}

            # Encode the parameters to a query string
            query_string = urlencode(params)

            # Construct the full URL with the parameters
            url = f"{'myClubs/default'}?{query_string}"

            # Create a HttpResponseRedirect object
            return HttpResponseRedirect(url)
        else:
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
        # Allows for default pages to work with get requests
        if (currentPage == "/myClubs/default"):
            # TODO USE AJAX INSTEAD OF THIS STUFF 
            # Define GET parameters
            params = {'className': club.name}

            # Encode the parameters to a query string
            query_string = urlencode(params)

            # Construct the full URL with the parameters
            url = f"{'myClubs/default'}?{query_string}"

            # Create a HttpResponseRedirect object
            return HttpResponseRedirect(url)
        else:
            # return them to the page they were on
            return redirect(currentPage)
    else:
        # if they do not have access, deny them
        return render(request, "NuhUh.html")

def viewClubPost(request):
    # get the postkey along with the club with the post
    postKey = request.GET.get("postKey")

    post = LiveFeed.objects.get(id = postKey)
    club = Club.objects.get(name = post.club.name)
    replies = Replies.objects.filter(post=post)

    

    # Make sure they have proper credentials
    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):
        context = {
            'post': post,
            'replies': replies,
            'club': club,
            'userPic': Users.objects.get(email = request.user.email).picURL,
        } 

        if mobile(request):
            # ignore mobile layout for now
            return render(request, "mobileDisplay/post.html", context)
        else:
            return render(request, "desktopDisplay/post.html", context)

        
    else:
        # no credentials no eyes
        return render(request, "NuhUh.html")

def addComment(request):
    postKey = request.POST.get("postNumber")
    commentText = request.POST.get("body")

    # get club by checking what club the org post comes from & get the post
    post = LiveFeed.objects.get(id = postKey)
    club = Club.objects.get(name = post.club.name)

    # Check if they are authed to make comments on the post
    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):

        # get the creator
        creator = Users.objects.get(email = request.user.email)

        # Make the post with all fields filled out
        Replies.objects.create(
        text = commentText,
        post = post,
        edited = False,
        linkToOtherReply = False,
        creator = creator
        )

        # Email the message out (format it later)
        subject = creator.name.title() + ' replied to your post "' + post.title + '"'
        message = subject + "\n" + creator.name.title() + " responded with: " + commentText
        email_from = settings.EMAIL_HOST_USER

        email = [post.creator.email, ]
        send_mail( subject, message, email_from, email)
        
        # TODO USE AJAX INSTEAD OF THIS STUFF 
        # Define GET parameters
        params = {'postKey': postKey}

        # Encode the parameters to a query string
        query_string = urlencode(params)

        # Construct the full URL with the parameters
        url = f"{'viewPost'}?{query_string}"

        # Create a HttpResponseRedirect object
        return HttpResponseRedirect(url)
    else:
        return render(request, "NuhUh.html")

def addReplyToComment(request):
    postKey = request.POST.get("postNumber")
    replyKey = request.POST.get("replyNumber")
    commentText = request.POST.get("body")

    # get club by checking what club the org post comes from & get the post
    post = LiveFeed.objects.get(id = postKey)
    club = Club.objects.get(name = post.club.name)

    # Check if they are authed to make comments on the post
    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):
        
        # get the creator and reply to link
        creator = Users.objects.get(email = request.user.email)
        replyLink = Replies.objects.get(id = replyKey)

        # Make the post with all fields filled out
        Replies.objects.create(
        text = commentText,
        post = post,
        edited = False,
        linkToOtherReply = True,
        replyLink = replyLink,
        creator = creator
        )

        # Email the message out (to person replied to) (format it later)
        subject = creator.name.title() + ' replied to your comment "' + replyLink.text + '"'
        message = subject + "\n" + creator.name.title() + " responded with: " + commentText
        email_from = settings.EMAIL_HOST_USER

        email = [replyLink.creator.email, ]
        send_mail( subject, message, email_from, email)

        # Email the message out (format it later)
        subject = creator.name.title() + ' replied to your post "' + post.title + '"'
        message = subject + "\n" + creator.name.title() + " responded with: " + commentText
        email_from = settings.EMAIL_HOST_USER

        email = [post.creator.email, ]
        send_mail( subject, message, email_from, email)


        # TODO USE AJAX INSTEAD OF THIS STUFF 
        # Define GET parameters
        params = {'postKey': postKey}

        # Encode the parameters to a query string
        query_string = urlencode(params)

        # Construct the full URL with the parameters
        url = f"{'viewPost'}?{query_string}"

        # Create a HttpResponseRedirect object
        return HttpResponseRedirect(url)
    else:
        return render(request, "NuhUh.html")

def deleteComment(request):
    replyKey = request.POST.get("replyKey")
    postKey = request.POST.get("postNumber")

    # get club by checking what club the org post comes from & get the post
    post = LiveFeed.objects.get(id = postKey)
    club = Club.objects.get(name = post.club.name)

    # get the comment
    reply = Replies.objects.get(id = replyKey)

    if request.user.is_authenticated and (reply.creator.email == request.user.email 
        or club.advisors.filter(email = request.user.email).exists() 
        or club.leaders.filter(email = request.user.email).exists()):

        # delete the comment if it passes auth check
        reply.delete()


        # TODO USE AJAX INSTEAD OF THIS STUFF 
        # Define GET parameters
        params = {'postKey': postKey}

        # Encode the parameters to a query string
        query_string = urlencode(params)

        # Construct the full URL with the parameters
        url = f"{'viewPost'}?{query_string}"

        # Create a HttpResponseRedirect object
        return HttpResponseRedirect(url)
    else:
        return render(request, "NuhUh.html")


# custom club homepages are created below
# change from localhost to dhsclubs.org when pushing updates
def nehsInternalHome(request):
    club = Club.objects.get(name = "National English Honor Society (NEHS)")

    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):

        # gets all posts for the club
        posts = reversed(LiveFeed.objects.filter(club = club))

        # limits posts to leaders & advisors
        context = {
            'posts': posts,
            'club': club,
            'userPic': Users.objects.get(email = request.user.email).picURL,
            'postAbility': club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()
        }

        if mobile(request):
            return render(request, "mobileDisplay/ClubJoined.html", context)
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