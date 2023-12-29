from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    # ex: /polls/tester/
    path("", views.test, name="TEST"),
]

urlpatterns += staticfiles_urlpatterns()