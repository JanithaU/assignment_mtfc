from django.shortcuts import render
from rest_framework import generics
from .models import User, LoginActivity, Team, Player
from .serializers import UserSerializer,LoginActivitySerializer,PlayerSerializer,TeamSerializer

# Create your views here.

# Player 
class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer   


# User 
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer   


# LoginActivity 
class LoginActivityList(generics.ListAPIView):
    queryset = LoginActivity.objects.all()
    serializer_class = LoginActivitySerializer

class LoginActivityDetail(generics.RetrieveAPIView):
    queryset = LoginActivity.objects.all()
    serializer_class = LoginActivitySerializer   


# Team 
class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer   