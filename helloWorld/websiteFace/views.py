from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect

from django.http import HttpResponse
from django.template import loader


def test(request):
    template = loader.get_template("polls/test.html")
    return HttpResponse(template.render())