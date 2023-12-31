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

def test(request):
    middleware.csrf.get_token(request) 
    template = loader.get_template("polls/test.html")
    return HttpResponse(template.render())

def start(request):
    VideoAnalysis.process_vid("https://www.youtube.com/watch?v=uCrFhEUjyLY")
    return HttpResponse("It Finished!")

def simpleTest(request):
    # User will not see progress bar if pop-ups are blocked
    # Fix this eventually with HTML GET request later on
    template = loader.get_template("polls/videoSubmit.html")
    return HttpResponse(template.render())
    #return HttpResponse("""<html><script>window.open('http://127.0.0.1:8000/progress/');
    #                    window.location.replace('/start');
    #                    </script></html>""")

def about(request):
    template = loader.get_template("templates/about.html")
    return HttpResponse(template.render())

def contact(request):
    template = loader.get_template("polls/contact.html")
    return HttpResponse(template.render())

def robotics(request):
    template = loader.get_template("polls/robotics.html")
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
    template = loader.get_template('polls/progress.html')
    context = {'strVar': simpleString}
    time.sleep(1.2)
    return HttpResponse(template.render(context, request))

#@csrf_exempt
def action_page(request):
  start(request)
  return progressBar(request)