from django.test import TestCase
from .models import Team, Player,User
from django.core.exceptions import ValidationError

# Create your views here.


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

    def test_calculate_average_score(self):
        self.player.calculate_average_score()
        self.assertEqual(self.player.average_score, 5.0)



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