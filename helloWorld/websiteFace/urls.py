from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    # ex: /polls/tester/
    path("", views.test, name="TEST"),
    path("simple_function", views.simpleTest, name="TEST2")
]

urlpatterns += staticfiles_urlpatterns()