from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Tournament import views



urlpatterns = [
    path('games/', views.GameList.as_view()),
    path('games/<int:pk>/', views.GameDetail.as_view()),

    path('scores/', views.ScoreList.as_view()),
    path('scores/<int:pk>/', views.ScoreDetail.as_view()),

    path('tournaments/', views.TournamentList.as_view()),
    path('tournaments/<int:pk>/', views.TournamentDetail.as_view()),

    path('tournamentrounds/', views.TournamentRoundList.as_view()),
    path('tournamentrounds/<int:pk>/', views.TournamentRoundDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
