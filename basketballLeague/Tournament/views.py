from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics
from .models import Game, Score, Tournament, TournamentRound
from .serializers import GameSerializer, ScoreSerializer, TournamentSerializer, TournamentRoundSerializer
from .permissions import OnlyAdmin
from rest_framework import permissions


# Create your views here.


# Game 
class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,OnlyAdmin]

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,OnlyAdmin]
    



# Score 
class ScoreList(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,OnlyAdmin]

class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,OnlyAdmin]


# Tournament 
class TournamentList(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,OnlyAdmin]

class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,OnlyAdmin]


# TournamentRound 
class TournamentRoundList(generics.ListCreateAPIView):
    queryset = TournamentRound.objects.all()
    serializer_class = TournamentRoundSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,OnlyAdmin]

class TournamentRoundDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TournamentRound.objects.all()
    serializer_class = TournamentRoundSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,OnlyAdmin]