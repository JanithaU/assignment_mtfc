from django.db import models
from Teams.models import Team
from django.core.exceptions import ValidationError


# Create your models here.
class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    champion = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='champion_tournaments')

    def progress_to_next_round(self):
        current_round = self.rounds.order_by('-round_number').first()
        next_round_number = current_round.round_number + 1
        print(current_round.round_number)
        print(current_round.games.count())

        if not any(game.winner is None for game in current_round.games.all()):
            # if current_round.round_number < 4 and current_round.games.count() >= 1 :
            winning_teams = [game.winner for game in current_round.games.all() if game.winner]
            if  current_round.games.count() == 1: 
                if len(winning_teams) == 1:
                    self.champion = winning_teams[0]
                    self.save()

            else:
                next_round = TournamentRound.objects.create(tournament=self, round_number=next_round_number)
                print(winning_teams)
                for i in range(0, len(winning_teams), 2):
                    Game.objects.create(round=next_round, team1=winning_teams[i], team2=winning_teams[i+1])
        else:
            pass


    def __str__(self):
        return self.name

class TournamentRound(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='rounds')
    round_number = models.IntegerField()

    def __str__(self):
        return str(self.tournament) +"_round_"+ str(self.round_number) 

class Game(models.Model):
    round = models.ForeignKey(TournamentRound, on_delete=models.CASCADE, related_name='games')
    team1 = models.ForeignKey(Team, related_name='team1_games', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='team2_games', on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='won_games')


    def save(self, *args, **kwargs):
        # Check if the game is being created for the first time
        if self._state.adding:
            super().save(*args, **kwargs)  # Save the game first to ensure it has an ID
            self.update_players_games_played(self.team1)
            self.update_players_games_played(self.team2)
        else:
            super().save(*args, **kwargs)

    def update_players_games_played(self, team):
        for player in team.players.all():
            player.games_played = (player.games_played or 0) + 1
            player.save()

    def determine_winner(self):
        score = self.score
        if score.score1 > score.score2:
            self.winner = self.team1
        elif score.score2 > score.score1:
            self.winner = self.team2
        self.save()

    # def clean(self):
    #     if self.winner and self.winner not in [self.team1, self.team2]:
    #         raise ValidationError("Winner must be either team1 or team2.")

    # def save(self, *args, **kwargs):
    #     self.clean()  # Ensure clean is called during save
    #     super().save(*args, **kwargs)


    def __str__(self):
            return str(self.round) + '_'+ str(self.team1)+"_vs_"+str(self.team2)


class Score(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE,related_name='score')
    score1 = models.IntegerField()
    score2 = models.IntegerField()


    def __str__(self):
            return str(self.game)