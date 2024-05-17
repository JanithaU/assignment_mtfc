from rest_framework import serializers
from .models import Tournament, TournamentRound, Game, Score
from Teams.serializers import TeamSerializer

# Create your views here.


class TournamentSerializer(serializers.ModelSerializer):
    champion = TeamSerializer(read_only=True)
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'start_date', 'end_date', 'champion']

class TournamentRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = TournamentRound
        fields = ['id', 'tournament', 'round_number']


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'game', 'score1', 'score2']


class GameSerializer(serializers.ModelSerializer):
    winner = TeamSerializer(read_only=True)
    class Meta:
        model = Game
        fields = ['id', 'round', 'team1', 'team2', 'date', 'winner']