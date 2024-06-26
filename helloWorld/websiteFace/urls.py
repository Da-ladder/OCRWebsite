from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from . import views

urlpatterns = [
    # Shows the URL needed after the domain name
    # /
    path("", views.frontPage, name="TEST"),
    #/admin/
    path("admin/", admin.site.urls),
    # /video_analysis/
    path("video_analysis", views.videoAnalysis, name="TEST2"),
    # /about/
    path("about/", views.about, name="ABOUT"),
    # /find_team/ <- GET only requests
    path("findteam/", views.find_team, name="teamFinder"),
    # /start/ <- GET only requests
    path("start/", views.start, name="START"),
    # /action_page/
    path("action_page/", views.action_page, name="POSTtest"),
    # /checkProgress/
    path("checkProgress/", views.progressBar, name="HEHE"),
    # /contact/
    path("contact/", views.contact,name="CONTACT"),
    # /robotics/
    path("robotics/", views.robotics,name="ROBOTICS"),
]

urlpatterns += staticfiles_urlpatterns()