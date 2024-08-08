from django.db import models
from django.utils import timezone

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=150) # just to be safe
    email = models.CharField(max_length=255) # just to be safe
    picURL = models.URLField(max_length=255, blank=True, null=True)
    extraData = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.email  # as not to confuse two ppl with the same first & last name

class ClubTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Club(models.Model):
    name = models.CharField(max_length=255)
    discription = models.TextField(blank = True) # will be used for placeholder as primary website layout is developed
    advisorOrAdvisors = models.TextField(blank=True)  # just in case we can handle unlimited advisors seperated by ", " in database
    contact = models.TextField(blank=True) # pulling nothing will yeild a blank string ie "". Null not needed
    generalMeets = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    active = models.BooleanField(default=False) 
    users = models.ManyToManyField(Users, blank=True, related_name='club_users')
    tagOrTags = models.ManyToManyField(ClubTag, blank=True)

    advisors = models.ManyToManyField(Users, blank=True, related_name='club_advisors')
    leaders = models.ManyToManyField(Users, blank=True, related_name='club_leaders')
    frontPage = models.CharField(max_length=255, blank=True, null=True)
    memberPage = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True)
    homeURL = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class LiveFeed(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True) # DO NOT let users type more than 255 for the title
    text = models.TextField(blank=True, null=True, max_length=24000)
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name='clubFeed')
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    creationTime = models.DateTimeField(default=timezone.now)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='op', null=True) # op as in original poster

    def __str__(self):
        return self.club.name + ": " + self.title

class Replies(models.Model):
    text = models.TextField(blank=True, null=True, max_length=3750)
    post = models.ForeignKey(LiveFeed, on_delete=models.CASCADE, related_name='OriginalPost')
    edited = models.BooleanField(default=False)
    creationTime = models.DateTimeField(default=timezone.now)
    linkToOtherReply = models.BooleanField(default=False)
    replyLink = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='OriginalPost', null=True, blank=True)
    creator = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='ReplyOp', null=True) # op as in original poster

    def __str__(self):
        return self.post.title + " reply"


