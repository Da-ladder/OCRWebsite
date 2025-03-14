from django.urls import path
from . import views



urlpatterns = [
    path("", views.home),
    path("loggedIn", views.registerUserAs),
    path("logout", views.logout_view),
    path("clubs/", views.club_display_new),
    path("clubs/default", views.club_default),
    path("edit", views.club_edit),
    path("editClub", views.changeClub),
    path("addPost", views.addClubPost),
    path("deletePost", views.deleteClubPost),
    path("joinClub", views.joinClub),
    path("myClubs/", views.dis_my_clubs),
    path("myClubs/mathTeam/", views.mathTeamIntHome),
    path("myClubs/mathTeam/changeRounds", views.mathTeamChangeRound),
    path("myClubs/mathTeam/newRound", views.mathTeamNewRound),
    path("myClubs/mathTeam/viewComp", views.mathTeamViewComp),
    path("myClubs/nehs", views.nehsInternalHome),
    path("myClubs/default", views.club_home_default),
    path("leaveClub", views.leaveClub),
    path("viewPost", views.viewClubPost),
    path("addComment", views.addComment),
    path("addReplyToComment", views.addReplyToComment),
    path("deleteComment", views.deleteComment),
    path("trivia", views.trivia),
    path("triviaQuestionMaker", views.triviaQuestionMaker),
    # path("triviaQuestionUpload"),
] 