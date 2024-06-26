import re
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django import middleware
from .webFuncts.models import ResultStorage


#from .webFuncts.find import VideoAnalysis
from .tasks import *
import time

simpleString = ""

def frontPage(request):
    middleware.csrf.get_token(request) 
    template = loader.get_template("frontPage.html")
    return HttpResponse(template.render())

def start(request):
    if request.method == 'GET':
        link = request.GET.get('link', None)
        addVid_async.delay(link)
    return HttpResponse("Process has completed (your video is either in queue or is processing)")

def find_team(request):
    if request.method == 'GET':
        link = request.GET.get('link', None)
        team = request.GET.get('team', None)
        findTeam_async.delay(link, team)
    return HttpResponse("Process for find_team has finished")
    
def videoAnalysis(request):
    # All models that are found are put in the videos list
    
    videos = ResultStorage.objects.all()

    videos = list(videos)[::-1]

    # Django admin doesn't allow links to be stored on the database so we separate ourselves
    # For loop to split the video links into seperate elements on a list (for hyperlinking)
    for video in videos:
        # Split vid_links by space (assuming links are separated by spaces)

        video.vid_links = re.split(r'\n|Link:', video.vid_links)
        #video.vid_links = video.vid_links.split("\n") # Turn vid_links into a list

    # Create a list of instances
    context = {
        'videos': videos,
    }

    # Render the page with videoSubmit template and give the html file the list of instances
    return render(request, 'videoSubmit.html', context)

def about(request):
    template = loader.get_template("about.html")
    return HttpResponse(template.render())

def contact(request):
    template = loader.get_template("contact.html")
    return HttpResponse(template.render())

def robotics(request):
    template = loader.get_template("robotics.html")
    return HttpResponse(template.render())

def progressBar(request):
    global simpleString
    simpleString = ""
    curProgress = 0 #VideoAnalysis.getStat()
    if curProgress[0] == 1:
        simpleString = "download %" + str(curProgress[1])
    elif curProgress[0] == 2:
        simpleString = "Frame Capture %" + str(curProgress[1])
    elif curProgress [0] == 3:
        simpleString = "Analysis %" + str(curProgress[1])
    else:
        simpleString = "Oops! Something went wrong"
    template = loader.get_template('progress.html')
    context = {'strVar': simpleString}
    time.sleep(1.2)
    return HttpResponse(template.render(context, request))

#@csrf_exempt
def action_page(request):
  start(request)
  return progressBar(request)