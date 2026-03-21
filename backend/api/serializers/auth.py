from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from api.models import User, UserStats


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
                attrs['username'] = user.username
            except User.DoesNotExist:
                pass
        
        return super().validate(attrs)


class UserStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStats
        fields = ('xp', 'level', 'current_streak', 'health_score', 
                  'fitness_score', 'recovery_score', 'lifestyle_score', 'consistency_score')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile', 'is_staff', 'marketing_opt_in', 'is_verified', 'date_joined')

    def get_profile(self, obj):
        try:
            stats = obj.stats
        except UserStats.DoesNotExist:
            stats = None
            
        stats_data = UserStatsSerializer(stats).data if stats else {}
        
        return {
            'bio': obj.bio,
            'avatar': obj.avatar if obj.avatar else None,
            'level': stats_data.get('level', 1),
            'xp': stats_data.get('xp', 0),
            'current_streak': stats_data.get('current_streak', 0),
            'health_score': stats_data.get('health_score', 0),
            'scores': {
                'fitness': stats_data.get('fitness_score', 0),
                'recovery': stats_data.get('recovery_score', 0),
                'lifestyle': stats_data.get('lifestyle_score', 0),
                'consistency': stats_data.get('consistency_score', 0),
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        
        profile_data = self.initial_data.get('profile', {})
        if profile_data:
            instance.bio = profile_data.get('bio', instance.bio)
            instance.avatar = profile_data.get('avatar', instance.avatar)

        instance.save()
        return instance
