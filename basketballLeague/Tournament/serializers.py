from rest_framework import serializers
from .models import Tournament, TournamentRound, Game, Score
from Teams.serializers import TeamSerializerShort

# Create your views here.


class TournamentSerializer(serializers.ModelSerializer):
    champion = TeamSerializerShort(read_only=True)
    class Meta:
        model = Tournament
        fields = ['id', 'name', 'start_date', 'end_date', 'champion']

    

class TournamentSerializerShort(TournamentSerializer):
    # champion_team = serializers.SerializerMethodField()
    class Meta:
        model = Tournament
        fields = ['id', 'name']    

    # def get_champion_team(self, obj):
    #     return obj.champion.name if obj.champion else None




class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['id', 'game', 'score1', 'score2']


    def create(self, validated_data):
        instance = super().create(validated_data)
        
        # Access the game instance
        game_instance = instance.game
        # Call the determine_winner function on the game instance
        game_instance.determine_winner()


        #If round condition then nextround
        game_instance.round.tournament.progress_to_next_round()
        
        return instance

    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        
        # Access the game instance
        game_instance = instance.game
        
        # Call the determine_winner function on the game instance
        game_instance.determine_winner()
        
        #If round condition then nextround
        game_instance.round.tournament.progress_to_next_round()

        return instance



class GameSerializer(serializers.ModelSerializer):
    winner = TeamSerializerShort(read_only=True)
    # round = TournamentRoundSerializer(read_only=True)
    round_number = serializers.SerializerMethodField()
    score = ScoreSerializer(read_only=True)
    class Meta:
        model = Game
        fields = ['id', 'round', 'round_number', 'team1', 'team2', 'date', 'winner','score']


    def get_round_number(self, obj):
        return obj.round.round_number if obj.round else None



    def validate(self, data):
        team1 = data.get('team1')
        team2 = data.get('team2')
        round_instance = data.get('round')

        if team1 and team2:
            # Ensure that each team has at most 10 players
            if team1.players.count() > 10:
                raise serializers.ValidationError({"team1": "Team 1 cannot have more than 10 players."})
            if team2.players.count() > 10:
                raise serializers.ValidationError({"team2": "Team 2 cannot have more than 10 players."})

            # Ensure each team has a coach
            if not team1.coach:
                raise serializers.ValidationError({"team1": "Team 1 must have a coach."})
            if not team2.coach:
                raise serializers.ValidationError({"team2": "Team 2 must have a coach."})

            # Ensure the teams are different
            if team1 == team2:
                raise serializers.ValidationError("Team 1 and Team 2 must be different.")


            # Ensure the teams are in the current round
            participating_teams = {game.team1 for game in round_instance.games.all()}.union(
                                  {game.team2 for game in round_instance.games.all()})
            
            if round_instance.round_number == 1:
                if team1 in participating_teams:
                    raise serializers.ValidationError({"team1": "Team 1 is in the current round."})
                if team2 in participating_teams:
                    raise serializers.ValidationError({"team2": "Team 2 is in the current round."})
            else:
                if team1 not in participating_teams:
                    raise serializers.ValidationError({"team1": "Team 1 is not in the current round."})
                if team2 not in participating_teams:
                    raise serializers.ValidationError({"team2": "Team 2 is not in the current round."})

            if round_instance.games.all().count() >= 16:
                raise serializers.ValidationError({"Games": "Maximum(16) Number of games in the tournament-round"})
            

        return data
    

class GameSerializerShort(GameSerializer):
    # winner = TeamSerializerShort(read_only=True)
    # # round = TournamentRoundSerializer(read_only=True)
    # round_number = serializers.SerializerMethodField()
    class Meta:
        model = Game
        fields = ['id', 'round', 'round_number', 'team1', 'team2', 'date', 'winner','score']



class TournamentRoundSerializer(serializers.ModelSerializer):
    #tournament = TournamentSerializerShort()
    games = GameSerializerShort(many=True)
    class Meta:
        model = TournamentRound
        fields = ['id', 'tournament', 'round_number', 'games']
