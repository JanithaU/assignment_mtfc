from rest_framework import serializers
from .models import User, LoginActivity, Player, Team


class LoginActivitySerializer(serializers.ModelSerializer):
    login_count = serializers.SerializerMethodField()

    class Meta:
        model = LoginActivity
        fields = ['id', 'user',  'login_time', 'logout_time', 'duration', 'login_count' ]


    def get_login_count(self, obj):
        return obj.user.login_count
    

class LoginActivitySerializerShort(serializers.ModelSerializer):
    
    class Meta:
        model = LoginActivity
        fields = ['id', 'login_time', 'logout_time', 'duration' ]

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
    login_activities = LoginActivitySerializerShort(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'login_count', 'total_time_spent', 'is_online','login_activities']
        read_only_fields = ['login_count','total_time_spent','is_online']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class PlayerSerializer(serializers.ModelSerializer):
    average_score = serializers.FloatField(read_only=True)
    class Meta:
        model = Player
        fields = ['id', 'name', 'height', 'team', 'games_played','field_goals','average_score']
        read_only_fields = ['average_score']

        

    def validate_team(self, value):
        if value and value.players.count() >= 10:
            raise serializers.ValidationError("A team cannot have more than 10 players.")
        return value


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    average_score = serializers.SerializerMethodField()
    winning_percentage = serializers.SerializerMethodField()
    coach_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'coach','coach_name', 'players', 'average_score', 'winning_percentage']

    def get_coach_name(self, obj):
        return obj.coach.username if obj.coach else None

    def get_average_score(self, obj):
        return obj.average_score()

    def get_winning_percentage(self, obj):
        return obj.winning_percentage()
    


class TeamSerializerShort(TeamSerializer):
    
    class Meta:
        model = Team
        fields = ['id', 'name','average_score', 'winning_percentage']