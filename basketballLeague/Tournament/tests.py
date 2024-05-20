from django.test import TestCase
from django.utils import timezone
from Teams.models import User, Team, Player
from Tournament.models import Tournament, TournamentRound, Game, Score

# Create your tests here.

class TournamentTestCase(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            name="Sample Tournament",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timezone.timedelta(days=30)).date()
        )

    def test_tournament_creation(self):
        self.assertEqual(self.tournament.name, "Sample Tournament")
        self.assertIsNone(self.tournament.champion)
        self.assertGreater(self.tournament.end_date, self.tournament.start_date)

    def test_progress_to_next_round(self):
        round1 = TournamentRound.objects.create(tournament=self.tournament, round_number=1)
        self.assertEqual(round1.round_number, 1)
        self.assertEqual(self.tournament.rounds.count(), 1)




class TournamentRoundTestCase(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            name="Sample Tournament",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timezone.timedelta(days=30)).date()
        )
        self.round = TournamentRound.objects.create(tournament=self.tournament, round_number=1)

    def test_round_creation(self):
        self.assertEqual(self.round.round_number, 1)
        self.assertEqual(self.round.tournament, self.tournament)

    def test_string_representation(self):
        self.assertEqual(str(self.round), f"{self.tournament}_round_1")




class GameTestCase(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            name="Sample Tournament",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timezone.timedelta(days=30)).date()
        )
        self.round = TournamentRound.objects.create(tournament=self.tournament, round_number=1)

        self.coach1 = User.objects.create_user(username='coach1', password='password', role='coach')
        self.coach2 = User.objects.create_user(username='coach2', password='password', role='coach')

        self.team1 = Team.objects.create(name="Team1", coach=self.coach1)
        self.team2 = Team.objects.create(name="Team2", coach=self.coach2)

        self.player1 = Player.objects.create(name="Player1", height=6.1, team=self.team1, games_played=0, field_goals=10)
        self.player2 = Player.objects.create(name="Player2", height=6.2, team=self.team2, games_played=0, field_goals=15)

        self.game = Game.objects.create(round=self.round, team1=self.team1, team2=self.team2, date=timezone.now())

    def test_game_creation(self):
        self.assertEqual(self.game.team1, self.team1)
        self.assertEqual(self.game.team2, self.team2)
        self.assertEqual(self.game.round, self.round)

    def test_determine_winner(self):
        score = Score.objects.create(game=self.game, score1=20, score2=15)
        self.game.determine_winner()
        self.assertEqual(self.game.winner, self.team1)

        score.score1 = 10
        score.score2 = 15
        score.save()
        self.game.determine_winner()
        self.assertEqual(self.game.winner, self.team2)



class ScoreTestCase(TestCase):
    def setUp(self):
        self.tournament = Tournament.objects.create(
            name="Sample Tournament",
            start_date=timezone.now().date(),
            end_date=(timezone.now() + timezone.timedelta(days=30)).date()
        )
        self.round = TournamentRound.objects.create(tournament=self.tournament, round_number=1)

        self.coach1 = User.objects.create_user(username='coach1', password='password', role='coach')
        self.coach2 = User.objects.create_user(username='coach2', password='password', role='coach')

        self.team1 = Team.objects.create(name="Team1", coach=self.coach1)
        self.team2 = Team.objects.create(name="Team2", coach=self.coach2)

        self.player1 = Player.objects.create(name="Player1", height=6.1, team=self.team1, games_played=0, field_goals=10)
        self.player2 = Player.objects.create(name="Player2", height=6.2, team=self.team2, games_played=0, field_goals=15)

        self.game = Game.objects.create(round=self.round, team1=self.team1, team2=self.team2, date=timezone.now())
        self.score = Score.objects.create(game=self.game, score1=20, score2=15)

    def test_score_creation(self):
        self.assertEqual(self.score.game, self.game)
        self.assertEqual(self.score.score1, 20)
        self.assertEqual(self.score.score2, 15)

    def test_determine_winner_via_score(self):
        self.game.determine_winner()
        self.assertEqual(self.game.winner, self.team1)

        self.score.score1 = 10
        self.score.score2 = 15
        self.score.save()
        self.game.determine_winner()
        self.assertEqual(self.game.winner, self.team2)

