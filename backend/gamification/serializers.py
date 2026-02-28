from rest_framework import serializers
from .models import Badge, UserBadge, GamificationAction


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model = UserBadge
        fields = '__all__'
        read_only_fields = ('user', 'badge', 'earned_at')


class GamificationActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GamificationAction
        fields = '__all__'
        read_only_fields = ('user', 'timestamp', 'xp_earned')
