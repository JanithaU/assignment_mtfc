from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone
from django.db.models import Sum, Count, F



# Create your views here.



class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('coach', 'Coach'),
        ('player', 'Player'),
    )
    role = models.CharField(max_length=10, choices=ROLES)

    @property
    def login_count(self):
        return self.login_activities.count()

    @property
    def total_time_spent(self):
        total_duration = self.login_activities.filter(logout_time__isnull=False).aggregate(
            total_time=Sum(F('logout_time') - F('login_time'), output_field=models.DurationField())
        )['total_time']
        if total_duration is None:
            total_duration = timezone.timedelta()
        return total_duration

    @property
    def is_online(self):
        return self.login_activities.filter(logout_time__isnull=True).exists()
    


class LoginActivity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='login_activities')
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    
    
    def duration(self):
        if self.logout_time:
            return self.logout_time - self.login_time
        return timezone.now() - self.login_time



class Team(models.Model):
    
    name = models.CharField(max_length=100,unique=True)
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


    def __str__(self):
            return self.name



class Player(models.Model):
    name = models.CharField(max_length=100)
    height = models.FloatField()
    team = models.ForeignKey(Team,  null=True, blank=True, on_delete=models.SET_NULL, related_name='players')
    games_played = models.IntegerField(default=0)
    field_goals = models.IntegerField(default=0)
    # useracc = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='playeracc')
   # average_score = models.FloatField(null=True, blank=True, editable=False)
    

    @property
    def average_score(self):
        if self.games_played and self.games_played > 0:
            return self.field_goals / self.games_played
        return 0.0
    

    def clean(self):
        if self.team and self.team.players.count() >= 10:
            raise ValidationError("A team cannot have more than 10 players.")
        

    def save(self, *args, **kwargs):
        self.clean()  # Validate before saving
        super().save(*args, **kwargs)
