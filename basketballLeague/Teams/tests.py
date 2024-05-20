from django.test import TestCase, Client
from .models import Team, Player,User
from django.core.exceptions import ValidationError

from django.utils import timezone
# from django.contrib.auth import  login, logout
from django.test.client import RequestFactory
from .models import LoginActivity
from datetime import timedelta

# Create your views here.

#User / Login testcases
class LoginActivityTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_login_activity_recorded(self):
        self.client.login(username='testuser', password='password')
        
        # Check if LoginActivity is created
        self.assertEqual(LoginActivity.objects.filter(user=self.user).count(), 1)
        activity = LoginActivity.objects.get(user=self.user)
        self.assertIsNotNone(activity.login_time)
        self.assertIsNone(activity.logout_time)
        self.client.logout()

    def test_logout_activity_recorded(self):
        self.client.login(username='testuser', password='password')
        self.client.logout()
        
        # Check if LoginActivity is updated
        activity = LoginActivity.objects.get(user=self.user)
        self.assertIsNotNone(activity.logout_time)

    def test_user_login_count(self):
        for _ in range(3):
            self.client.login(username='testuser', password='password')
            self.client.logout()
        
        self.assertEqual(self.user.login_count, 3)

    def test_user_total_time_spent(self):
        self.client.login(username='testuser', password='password')

        activity = LoginActivity.objects.get(user=self.user)
        activity.logout_time = activity.login_time + timedelta(hours=1)
        activity.save()
        
        self.client.login(username='testuser', password='password')
        activity = LoginActivity.objects.filter(user=self.user, logout_time__isnull=True).latest('login_time')
        activity.logout_time = activity.login_time + timedelta(hours=2)
        activity.save()
        
        self.assertEqual(self.user.total_time_spent, timedelta(hours=3))

    def test_user_is_online(self):
        self.client.login(username='testuser', password='password')
        
        self.assertTrue(self.user.is_online)
        
        self.client.logout()
        
        self.assertFalse(self.user.is_online)



#Player test cases
class PlayerModelTest(TestCase):
    def setUp(self):
        self.team = Team.objects.create(name='Team A')
        self.user = User.objects.create_user(username='player1', password='password', role='player')

        # Create a player
        self.player = Player.objects.create(
            name='John Doe',
            height=6.2,
            games_played=10,
            field_goals=50,
        
        )

    def test_team_cannot_have_more_than_10_players(self):
        for i in range(10):
            Player.objects.create(name=f'Player {i}', height=6.0,  team=self.team)

        with self.assertRaises(ValidationError):
            Player.objects.create(name='Player 11', height=6.0, team=self.team)

    def test_average_score(self):
        #self.player.calculate_average_score()
       # self.assertEqual(self.player.average_score, 5.0)
        self.assertEqual(self.player.average_score, 5.0)

#Team Testcases
class TeamModelTest(TestCase):
    def setUp(self):
        self.coach = User.objects.create_user(username='coach1', password='password', role='coach')
        self.team1 = Team.objects.create(name='Team 1', coach=self.coach)

    def test_cannot_assign_coach_to_multiple_teams(self):
        team2 = Team(name='Team 2', coach=self.coach)
        with self.assertRaises(ValidationError):
            team2.full_clean()  # This will call the model's validation methods

    def test_assign_non_coach_user_as_coach(self):
        non_coach = User.objects.create_user(username='player1', password='password', role='player')
        team = Team(name='Team 3', coach=non_coach)
        with self.assertRaises(ValidationError):
            team.full_clean()  # This will call the model's validation methods