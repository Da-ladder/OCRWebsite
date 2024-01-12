from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django import middleware

from .webFuncts.functFun import randomShit
from .webFuncts.find import VideoAnalysis
import time

simpleString = ""

def frontPage(request):
    middleware.csrf.get_token(request) 
    template = loader.get_template("frontPage.html")
    return HttpResponse(template.render())

def start(request):
    if request.method == 'GET':
        link = request.GET.get('link', None)
        VideoAnalysis.process_vid(link)
    return HttpResponse("It Finished!")

def videoAnalysis(request):
    template = loader.get_template("videoSubmit.html")
    return HttpResponse(template.render())

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
    curProgress = VideoAnalysis.getStat()
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