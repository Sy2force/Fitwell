from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OnboardingEntryViewSet, DailyHabitViewSet, HealthScoreViewSet, UserPlanViewSet

router = DefaultRouter()
router.register(r'onboarding', OnboardingEntryViewSet, basename='onboarding')
router.register(r'habits', DailyHabitViewSet, basename='habit')
router.register(r'scores', HealthScoreViewSet, basename='health-score')
router.register(r'plans', UserPlanViewSet, basename='plan')

urlpatterns = [
    path('', include(router.urls)),
]
