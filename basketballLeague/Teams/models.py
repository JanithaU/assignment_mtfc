from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings

# Create your views here.



class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('coach', 'Coach'),
        ('player', 'Player'),
    )
    role = models.CharField(max_length=10, choices=ROLES)

class LoginActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)



class Team(models.Model):
    name = models.CharField(max_length=100)
    coach = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='coached_team')

    def clean(self):
        if self.coach and self.coach.role != 'coach':
            raise ValidationError(f"The user {self.coach} does not have the role of 'coach'.")
        
    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)
    
    
    def average_score(self):
        players = self.players.all()
        if players:
            total_score = sum(player.average_score for player in players)
            return total_score / len(players)
        return 0

    def winning_percentage(self):
        total_games = self.team1_games.count() + self.team2_games.count()
        won_games = self.won_games.count()
        if total_games > 0:
            return (won_games / total_games) * 100
        return 0




class Player(models.Model):
    name = models.CharField(max_length=100)
    height = models.FloatField()
    team = models.ForeignKey(Team,  null=True, blank=True, on_delete=models.SET_NULL, related_name='players')
    games_played = models.IntegerField(default=0)
    field_goals = models.IntegerField(default=0)
    average_score = models.FloatField(null=True, blank=True, editable=False)
    
    def save(self, *args, **kwargs):
        if self.team and self.team.players.count() >= 10 and not self.pk:
            raise ValidationError("A team cannot have more than 10 players.")
        super(Player, self).save(*args, **kwargs)



    def calculate_average_score(self):
        if self.games_played > 0:
            self.average_score = self.field_goals / self.games_played
        else:
            self.average_score = 0
        self.save()