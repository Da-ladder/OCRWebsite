from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=150) # just to be safe
    email = models.CharField(max_length=255) # just to be safe

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
    users = models.ManyToManyField(User)
    tagOrTags = models.ManyToManyField(ClubTag)

    url = models.URLField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.name



