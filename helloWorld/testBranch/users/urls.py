from django.urls import path
from . import views



urlpatterns = [
    path("", views.home),
    path("loggedIn", views.registerUser),
    path("logout", views.logout_view),
    path("clubs/", views.club_display),
    path("clubs/default", views.club_default),
    path("joinClub", views.joinClub),
    path("myClubs/", views.dis_my_clubs),
    path("myClubs/default", views.club_default),
]