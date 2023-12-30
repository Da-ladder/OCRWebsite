from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [
    # ex: /home/
    path("", views.test, name="TEST"),
    # /home/simple_function
    path("simple_function", views.simpleTest, name="TEST2"),
    path("about/", views.about, name="ABOUT"),
    path("progress/", views.progressBar, name="PROGRESS BAR"),
    path("start/", views.start, name="START"),
    path("action_page/", views.action_page, name="POSTtest"),
    path("checkProgress/", views.progressBar, name="HEHE"),
    path("contact/", views.contact,name="CONTACT"),
    path("robotics/", views.robotics,name="ROBOTICS"),
]

urlpatterns += staticfiles_urlpatterns()