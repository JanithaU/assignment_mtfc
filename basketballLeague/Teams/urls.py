from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Teams import views



urlpatterns = [
    path('teams/', views.TeamList.as_view()),
    path('teams/<int:pk>/', views.TeamDetail.as_view()),

    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('players/', views.PlayerList.as_view()),
    path('players/<int:pk>/', views.PlayerDetail.as_view()),

    path('loginactivity/', views.LoginActivityList.as_view()),
    path('loginactivity/<int:pk>/', views.LoginActivityDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
