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
import json
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

def trivia(request):
    return render(request, 'trivia.html')
    


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

    # gets current leaders, users, and advisor(s)
    users = club.users.all()

    leaders = club.leaders.all()

    advisors = club.advisors.all()

    # union operator does not work here. Do not know why it breaks it
    allMembers = list(advisors) + list(leaders) + list(users)

    # gets all user roles attached to that club
    userTags = UserTag.objects.filter(club = club)


    # preprocesses tag data so that the template can load proper tags for each person
    # this list will be structured in this way: [[email, [attached roles], [roles available]], repeat]
    masterRoleList = []

    for user in allMembers:
        masterRoleList.append([user.email, [tag.tagName for tag in UserTag.objects.filter(club = club, userList = user)],
        [tag.tagName for tag in UserTag.objects.filter(club = club).exclude(userList = user)]])
    
    

    # changes userTags to a list of tagNames for template processing
    userTags = [tag.tagName for tag in userTags]

    if request.user.is_authenticated and club.advisors.filter(email = request.user.email).exists():
        context = {
            'tags': tags,
            'users': users,
            'leaders': leaders,
            'allMembers': allMembers,
            'userTags': userTags,
            'userRoles': masterRoleList,
            'currTags': currTags,
            'club': club,
            'editUsers' : True,
        }
        return render(request, "clubEditDefault.html", context)
    elif request.user.is_authenticated and club.leaders.filter(email = request.user.email).exists():
        context = {
            'tags': tags,
            'currTags': currTags,
            'allMembers': allMembers,
            'userTags': userTags,
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
    userRoles = request.POST.get("masterRoles")

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

        # setting user roles
        userTags = UserTag.objects.filter(club = club)

        roleDict = {}
        # role Dict stores the various tags for that club
        for uTags in userTags:
            roleDict[uTags.tagName] = []


        # seperates the string in groups of email and roles together
        userRoles = userRoles.split("%")
        if "" in userRoles:
            userRoles.remove("")

        # goes through the strings and seperates roles and emails
        for user in userRoles:
            refined = user.split(',.')
            email = refined[0]
            roles = refined[1].split(';')

            if "" in roles:
                roles.remove("")
            
            # add emails to their roles
            for role in roles:
                try:
                    roleDict[role].append(email)
                except:
                    # do nothing as the role no longer exists
                    # protects against deletion & edit of roles at the same time
                    pass
        
        for roleAssign, emails in roleDict.items():
            roleT = UserTag.objects.get(club = club, tagName = roleAssign)
            roleT.userList.set(Users.objects.filter(email__in = emails))

        # user roles SET
        

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

        # setting user roles
        userTags = UserTag.objects.filter(club = club)

        roleDict = {}
        # role Dict stores the various tags for that club
        for uTags in userTags:
            roleDict[uTags.tagName] = []


        # seperates the string in groups of email and roles together
        userRoles = userRoles.split("%")
        if "" in userRoles:
            userRoles.remove("")

        # goes through the strings and seperates roles and emails
        for user in userRoles:
            refined = user.split(',.')
            email = refined[0]
            roles = refined[1].split(';')

            if "" in roles:
                roles.remove("")
            
            # add emails to their roles
            for role in roles:
                try:
                    roleDict[role].append(email)
                except:
                    # do nothing as the role no longer exists
                    # protects against deletion & edit of roles at the same time
                    pass
        
        for roleAssign, emails in roleDict.items():
            roleT = UserTag.objects.get(club = club, tagName = roleAssign)
            roleT.userList.set(Users.objects.filter(email__in = emails))
        
        # user roles SET

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

def mathTeamIntHome(request):
    # note that this request may be intense in compute
    # optimizations can be made
    club = Club.objects.get(name = "Math Team")

    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):

        # gets all posts for the club
        posts = list(reversed(LiveFeed.objects.filter(club = club)))
        empty = False

        # will result in placeholder text if there is no posts
        if len(posts) == 0:
            empty = True

        # retrieve round data
        multiData = ClubData.objects.filter(club = club)
        # data is stored in json format so it is decoded before use
        roundData = json.decoder.JSONDecoder().decode(multiData[len(multiData)-1].data)

        # gets list of aTeam and bTeam members
        updatedaTeam = [user.email for user in UserTag.objects.get(club = club, tagName = "A Team").userList.all()]
        updatedbTeam = [user.email for user in UserTag.objects.get(club = club, tagName = "B Team").userList.all()]
        curraTeam = roundData[1] # A team members are stored within a list in roundData
        delaTeam = [] # people to delete in A team
        currbTeam = roundData[2] # B team members are stored within a list in roundData
        delbTeam = [] # people to delete in B team

        # EDIT A TEAM ------------------------
        # check for differences in stored team members(deletes by index)
        index = 0
        for people in curraTeam:
            if people[0] in updatedaTeam:
                updatedaTeam.remove(people[0])
            else:
                delaTeam.append(index)

            index += 1

        # delete members who are not supposed to be there
        # reverse deletion so that skipping items does not occur (via index shifts)
        for i in reversed(delaTeam):
            del curraTeam[i]

        # add members to A team who are missing with default rounds (0, 0, 0)
        for people in updatedaTeam:
            curraTeam.append([people, [-1, -1, -1, -1, -1, -1], Users.objects.get(email=people).name])
        # END EDIT A TEAM ------------------------


        # EDIT B TEAM ------------------------
        # check for differences in stored team members(deletes by index)
        index = 0
        for people in currbTeam:
            if people[0] in updatedbTeam:
                updatedbTeam.remove(people[0])
            else:
                delbTeam.append(index)

            index += 1

        # delete members who are not supposed to be there
        # reverse deletion so that skipping items does not occur (via index shifts)
        for i in reversed(delbTeam):
            del currbTeam[i]

        # add members to B team who are missing with default rounds (0, 0, 0)
        for people in updatedbTeam:
            currbTeam.append([people, [-1, -1, -1, -1, -1, -1], Users.objects.get(email=people).name])
        # END EDIT B TEAM ------------------------

        # save edits to the database
        roundData[1] = curraTeam
        roundData[2] = currbTeam

        multiData[len(multiData)-1].data = json.dumps(roundData)
        multiData[len(multiData)-1].save()


        # limits posts to leaders & advisors
        context = {
            'posts': posts,
            'club': club,
            'userPic': Users.objects.get(email = request.user.email).picURL,
            'postAbility': club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists(),
            'ateam': curraTeam,
            'bteam': currbTeam,
            'prevComps': multiData,
            'rndNames': roundData[3],
            'compName': multiData[len(multiData)-1].name,
            # roundData has 4 levels: 1(Users can edit), 2(Only leaders can edit), 3(Users can input scores), 4(Only leaders can input scores)
            'roundEditAbility': roundData[0],
            "empty": empty,
        }

        if mobile(request):
            return render(request, "mobileDisplay/ClubJoined.html", context)
        else:
            return render(request, "desktopDisplay/MathTeam/internalHome.html", context)
    else:
        return render(request, "NuhUh.html")


def mathTeamNewRound(request):

    club = Club.objects.get(name = "Math Team")

    # get all required data
    name = request.POST.get('name')
    r1 = request.POST.get('r1')
    r2 = request.POST.get('r2')
    r3 = request.POST.get('r3')
    r4 = request.POST.get('r4')
    r5 = request.POST.get('r5')
    r6 = request.POST.get('r6')

    # auth
    if request.user.is_authenticated and (club.advisors.filter(email = request.user.email).exists() 
    or club.leaders.filter(email = request.user.email).exists()):

        # prefill data with dummy people (will be written over)
        placeholdData = [1, [["example@gmail.com", [-1, -1, 0, 0, 0, -1], "expName"], ["example1@gmail.com", [-1, 0, 0, 0, -1, -1], "expName1"]], [["example2@danbury.k12.ct.us", [-1, -1, 0, 0, 0, -1], "expName2"]],
                        [r1, r2, r3, r4, r5, r6]]

        # make new data entry
        ClubData.objects.create(
            club = club,
            name = name,
            data = json.dumps(placeholdData)
        )

        return redirect("/myClubs/mathTeam")
    else:
        return render(request, "NuhUh.html")


def mathTeamChangeRound(request):
    aTeam = request.POST.get('aTeam')
    bTeam = request.POST.get('bTeam')
    roundToggler = request.POST.get('toggle')
    club = Club.objects.get(name = "Math Team")

    # server side code so it is ok if it is outside of auth measures
    # retrieve round data
    multiData = ClubData.objects.filter(club = club)
    # data is stored in json format so it is decoded before use
    roundData = json.decoder.JSONDecoder().decode(multiData[len(multiData)-1].data)

    if request.user.is_authenticated and (club.advisors.filter(email = request.user.email).exists() or 
        club.leaders.filter(email = request.user.email).exists()):
        aTeam = aTeam.split("%")
        del aTeam[-1] # removes the last empty space
        bTeam = bTeam.split("%") 
        del bTeam[-1]

        for person in aTeam:
            rawData = person.split(',.')
            email = rawData[0]
            rounds = rawData[1].split(";")
            del rounds[-1]

            # changing all strings to numbers
            for i in range(len(rounds)):
                rounds[i] = int(rounds[i])

            # goes through data and changes rounds if user exists
            # omg the inefficiency
            # bc only a couple of items, it's ok
            for user in roundData[1]:
                if user[0] == email:
                    user[1] = rounds

        for person in bTeam:
            rawData = person.split(',.')
            email = rawData[0]
            rounds = rawData[1].split(";")
            del rounds[-1]

            # changing all strings to numbers
            for i in range(len(rounds)):
                rounds[i] = int(rounds[i])

            # goes through data and changes rounds if user exists
            for user in roundData[2]:
                if user[0] == email:
                    user[1] = rounds
        
        # changes edit state
        roundData[0] = int(roundToggler)

        # saves data
        multiData[len(multiData)-1].data = json.dumps(roundData)
        multiData[len(multiData)-1].save()    

    elif request.user.is_authenticated and club.users.filter(email = request.user.email).exists():
        # can't edit so they are kicked back
        if roundData[0] == 2:
            return redirect("/myClubs/mathTeam")

        if (request.user.email in aTeam):
            aTeam = aTeam.split("%")
            del aTeam[-1]

            # iterates through every submitted aTeam member
            for person in aTeam:
                rawData = person.split(',.')
                email = rawData[0]
                rounds = rawData[1].split(";")
                del rounds[-1]

                # changing all strings to numbers
                for i in range(len(rounds)):
                    rounds[i] = int(rounds[i])

                # skip if their email is not the same as they are a user
                if (email != request.user.email):
                    continue
                else:
                    # goes through data and changes rounds if it exists
                    for user in roundData[1]:
                        if user[0] == email:
                            user[1] = rounds

            # saves data
            multiData[len(multiData)-1].data = json.dumps(roundData)
            multiData[len(multiData)-1].save()     

        elif (request.user.email in bTeam):
            
            bTeam = bTeam.split("%")
            del bTeam[-1]

            # iterates through every submitted aTeam member
            for person in bTeam:
                rawData = person.split(',.')
                email = rawData[0]
                rounds = rawData[1].split(";")
                del rounds[-1]

                # changing all strings to numbers
                for i in range(len(rounds)):
                    rounds[i] = int(rounds[i])

                # skip if their email is not the same as they are a user
                if (email != request.user.email):
                    continue
                else:
                    # goes through data and changes rounds if it exists
                    for user in roundData[2]:
                        if user[0] == email:
                            user[1] = rounds
                    
            
            # saves data
            print(roundData)
            multiData[len(multiData)-1].data = json.dumps(roundData)
            multiData[len(multiData)-1].save() 
    else:
        return render(request, "NuhUh.html")

    return redirect("/myClubs/mathTeam")

def mathTeamViewComp(request):
    club = Club.objects.get(name = "Math Team")

    # server side code so it is ok if it is outside of auth measures
    # retrieve round data
    comp = ClubData.objects.get(club = club, name = request.GET.get('name'))
    # data is stored in json format so it is decoded before use
    roundData = json.decoder.JSONDecoder().decode(comp.data)

    if request.user.is_authenticated and (club.users.filter(email = request.user.email).exists() or 
        club.advisors.filter(email = request.user.email).exists() or club.leaders.filter(email = request.user.email).exists()):

        # only gives read only access to previous comps
        context = {
            'club': club,
            'ateam': roundData[1],
            'bteam': roundData[2],
            'rndNames': roundData[3],
            'compName': comp.name,
        }

        if mobile(request):
            # mobile screen has not been configured yet
            return render(request, "mobileDisplay/ClubJoined.html", context)
        else:
            return render(request, "desktopDisplay/MathTeam/prevComp.html", context)
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