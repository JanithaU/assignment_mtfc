from django.shortcuts import render
from django.shortcuts import render
from rest_framework import generics
from .models import Game, Score, Tournament, TournamentRound
from .serializers import GameSerializer, ScoreSerializer, TournamentSerializer, TournamentRoundSerializer

# Create your views here.


# Game 
class GameList(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

class GameDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer   



# Score 
class ScoreList(generics.ListCreateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

class ScoreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer   



# Tournament 
class TournamentList(generics.ListCreateAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer

class TournamentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tournament.objects.all()
    serializer_class = TournamentSerializer   


# TournamentRound 
class TournamentRoundList(generics.ListCreateAPIView):
    queryset = TournamentRound.objects.all()
    serializer_class = TournamentRoundSerializer

class TournamentRoundDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TournamentRound.objects.all()
    serializer_class = TournamentRoundSerializer   