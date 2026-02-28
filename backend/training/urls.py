from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExerciseViewSet, ProgramViewSet, WorkoutSessionViewSet

router = DefaultRouter()
router.register(r'exercises', ExerciseViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'sessions', WorkoutSessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
]
