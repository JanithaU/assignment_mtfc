from django.core.management.base import BaseCommand
from Teams.models import User, Team, Player
from Tournament.models import Tournament, TournamentRound, Game, Score
from django.utils import timezone

class Command(BaseCommand):
    help = 'Add sample data to the database'

    def handle(self, *args, **kwargs):
        # Create an admin user
        admin_user = User.objects.create_user(
            username='admin', 
            password='admin', 
            role='admin'
        )
        self.stdout.write(self.style.SUCCESS('Successfully added admin user'))

        # Create an player user
        admin_user = User.objects.create_user(
            username='player1', 
            password='player1', 
            role='player'
        )
        self.stdout.write(self.style.SUCCESS('Successfully added admin user'))

        # Create 18 coaches
        coaches = []
        for i in range(1, 19):
            coach = User.objects.create_user(
                username=f'coach{i}', 
                password=f'coach{i}', 
                role='coach'
            )
            coaches.append(coach)
            self.stdout.write(self.style.SUCCESS(f'Successfully added coach{i}'))

        # Create 17 teams 
        teams = []
        for i in range(1, 18):
            team_name = f'Team{i}'
            coach = coaches[i-1] 
            team = Team.objects.create(name=team_name, coach=coach)
            teams.append(team)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {team_name}'))

        # Create 221 players 
        players_data = [
            {"name": f"Player {i}", "height": 6.0 + (i % 10) * 0.1, "games_played": i % 10 + 1, "field_goals": i * 2}
            for i in range(1, 222)
        ]

        player_count = 0
        for i in range(16):  # Iterate over each team
            team = teams[i]
            num_players = 10 if i < 10 else 1
            for _ in range(num_players):
                player_data = players_data[player_count]
                Player.objects.create(
                    name=player_data['name'],
                    height=player_data['height'],
                    team=team,
                    games_played=player_data['games_played'],
                    field_goals=player_data['field_goals']
                )
                player_count += 1

        #create players without a team
        for i in range(len(players_data)-player_count):
            nw = i  + player_count
            player_data = players_data[nw]
            Player.objects.create(
                    name=player_data['name'],
                    height=player_data['height'],
                    games_played=player_data['games_played'],
                    field_goals=player_data['field_goals']
                )
        self.stdout.write(self.style.SUCCESS(f'Successfully added players without a team'))

        
        # Create tournaments
        tournament = Tournament.objects.create(name='Tournament-A', start_date=timezone.now(), end_date=timezone.now() + timezone.timedelta(days=7) )

        # Create tournament rounds
        for i in range(1, 2):
            round_number = f"Round {i}"
            tournament_round = TournamentRound.objects.create(tournament=tournament, round_number=i)
            self.stdout.write(self.style.SUCCESS(f'Successfully added {round_number}'))

            # Create games for each round
            for j in range(1, 9):
                # team1 = teams[(i + j) % 12]
                # team2 = teams[(i + j + 9) % 12]
                team1 = teams[j]
                team2 = teams[-j]
                date = timezone.now() + timezone.timedelta(days=i+j)
                game = Game.objects.create(round=tournament_round, team1=team1, team2=team2, date=date)
                self.stdout.write(self.style.SUCCESS(f'Successfully added game for {round_number}'))

                # Create scores for each game
                if j !=8:
                    Score.objects.create(game=game, score1=10, score2=8)
                    game.determine_winner()
                self.stdout.write(self.style.SUCCESS(f'Successfully added score for game {game}'))





        self.stdout.write(self.style.SUCCESS('Successfully added sample data'))
