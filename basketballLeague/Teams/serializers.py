from rest_framework import serializers
from .models import User, LoginActivity, Player, Team

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']


class LoginActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginActivity
        fields = ['id', 'user', 'login_time', 'logout_time', 'duration']



class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['id', 'name', 'height', 'average_score', 'team', 'games_played','field_goals','average_score']
        read_only_fields = ['average_score']

    ## optional
    # def validate_team(self, value):
    #     if value.players.count() >= 10:
    #         raise serializers.ValidationError("A team cannot have more than 10 players.")
    #     return value


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    average_score = serializers.SerializerMethodField()
    winning_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'coach', 'players', 'average_score', 'winning_percentage']

    def get_average_score(self, obj):
        return obj.average_score()

    def get_winning_percentage(self, obj):
        return obj.winning_percentage()