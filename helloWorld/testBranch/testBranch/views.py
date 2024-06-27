import re
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django import middleware

def frontPage(request):
    middleware.csrf.get_token(request) 
    template = loader.get_template("frontPage.html")
    return HttpResponse(template.render())