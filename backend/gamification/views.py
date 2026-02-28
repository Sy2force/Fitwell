from rest_framework import viewsets, permissions
from .models import Badge, UserBadge, GamificationAction
from .serializers import BadgeSerializer, UserBadgeSerializer, GamificationActionSerializer


class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserBadgeViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserBadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserBadge.objects.filter(user=self.request.user).order_by('-earned_at')


class GamificationActionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GamificationActionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return GamificationAction.objects.filter(user=self.request.user).order_by('-timestamp')
