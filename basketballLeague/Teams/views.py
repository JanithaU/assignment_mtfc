from django.shortcuts import render
from rest_framework import generics
from .models import User, LoginActivity, Team, Player
from .serializers import UserSerializer,LoginActivitySerializer,PlayerSerializer,TeamSerializer
from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import IsAdminOrOwner, OnlyAdmin, IsAdminOrCoach,IsAdminOrCoachOwner,IsAdminOrCoachPlayerPermission,IsAdminOrCoachNoPlayer
from django.db.models import Sum, Count, F, FloatField,ExpressionWrapper





# Create your views here.

# Player 
class PlayerList(generics.ListCreateAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdminOrCoachPlayerPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if user.role != 'admin':
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().create(request, *args, **kwargs)


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdminOrCoachPlayerPermission]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Perform custom validation
        team  = serializer.validated_data.get('team')
        if request.user.role != 'admin':
            if team and team.coach != request.user.coached_team.coach :
                return Response({'error': f"The user  does not owns the {team}."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)


class TopPlayersByTeamView(generics.ListAPIView):
    serializer_class = PlayerSerializer
    permission_classes = [IsAdminOrCoachNoPlayer]

    def get_queryset(self):
        team_id = self.kwargs['pk']
        team = Team.objects.filter(id=team_id).first()

        if not team:
            return Player.objects.none()

        players = team.players.annotate().filter(
            games_played__gt=0,
            field_goals__gt=0
        )

        average_scores = sorted(
            [(player.field_goals / player.games_played) for player in players if player.games_played and player.games_played > 0]
        )

        if not average_scores:
            return Player.objects.none()

        index = int(len(average_scores) * 0.9) - 1
        percentile_90_score = average_scores[max(index, 0)]

        return [player for player in players if player.average_score >= percentile_90_score]

# User 
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminOrOwner]
    #permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != 'admin':
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer   
    permission_classes = [permissions.IsAuthenticated,IsAdminOrOwner]


# LoginActivity 
class LoginActivityList(generics.ListAPIView):
    queryset = LoginActivity.objects.all()
    serializer_class = LoginActivitySerializer
    permission_classes = [OnlyAdmin]



class LoginActivityDetail(generics.RetrieveAPIView):
    queryset = LoginActivity.objects.all()
    serializer_class = LoginActivitySerializer   
    permission_classes = [OnlyAdmin]
    # permission_classes = [IsAdminOrOwner]
    
    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'admin':
    #         return LoginActivity.objects.all()
    #     return LoginActivity.objects.filter(user=user)


# Team 
class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrCoach]
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if user.role == 'player':
            return Response(
                {'detail': 'You do not have permission to perform this action.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Perform custom validation
        coach = serializer.validated_data.get('coach')
        if coach and coach.role != 'coach':
            return Response({'error': f"The user {coach} does not have the role of 'coach'."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer   
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsAdminOrCoachOwner]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Perform custom validation
        coach = serializer.validated_data.get('coach')
        if coach and coach.role != 'coach':
            return Response({'error': f"The user {coach} does not have the role of 'coach'."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Team deleted successfully'}, status=status.HTTP_202_ACCEPTED)