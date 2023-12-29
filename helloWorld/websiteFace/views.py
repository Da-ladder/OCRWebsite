from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect

from django.http import HttpResponse
from django.template import loader

from .functFun import randomShit
from .webFuncts.find import process_vid


def test(request):
    template = loader.get_template("polls/test.html")
    return HttpResponse(template.render())

def simpleTest(request):
    num = 2+3
    process_vid("https://www.youtube.com/watch?v=pLBcp3nJlFQ")
    randomShit()
    print(num)
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")