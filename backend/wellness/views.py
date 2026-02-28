from rest_framework import viewsets, permissions
from .models import OnboardingEntry, DailyHabit, HealthScore, UserPlan
from .serializers import OnboardingEntrySerializer, DailyHabitSerializer, HealthScoreSerializer, UserPlanSerializer


class OnboardingEntryViewSet(viewsets.ModelViewSet):
    serializer_class = OnboardingEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return OnboardingEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DailyHabitViewSet(viewsets.ModelViewSet):
    serializer_class = DailyHabitSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DailyHabit.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HealthScoreViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HealthScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return HealthScore.objects.filter(user=self.request.user).order_by('-date')


class UserPlanViewSet(viewsets.ModelViewSet):
    serializer_class = UserPlanSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserPlan.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
