from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    scores = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('avatar', 'bio', 'level', 'xp', 'current_streak', 'health_score', 'updated_at', 'scores')
        read_only_fields = ('level', 'xp', 'current_streak', 'health_score', 'updated_at')

    def get_scores(self, obj):
        try:
            from wellness.models import HealthScore
            latest = HealthScore.objects.filter(user=obj.user).order_by('-date').first()
            if latest:
                return {
                    'fitness': latest.fitness_score,
                    'recovery': latest.recovery_score,
                    'lifestyle': latest.lifestyle_score,
                    'consistency': latest.consistency_score
                }
        except Exception:
            pass
        return None


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'is_verified',
            'marketing_opt_in', 'date_joined', 'profile', 'is_staff'
        )
        read_only_fields = ('id', 'date_joined', 'is_verified', 'is_staff')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        # Create profile
        Profile.objects.create(user=user)
        return user
