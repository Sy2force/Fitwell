from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (ArticleViewSet, CommentViewSet, CategoryViewSet, UserViewSet, 
                    WellnessPlanViewSet, EmailTokenObtainPairView, WorkoutSessionViewSet,
                    ExerciseSetViewSet, ExerciseViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'users', UserViewSet)
router.register(r'wellness/plans', WellnessPlanViewSet, basename='wellness-plans')
router.register(r'workouts/sessions', WorkoutSessionViewSet, basename='workout-sessions')
router.register(r'workouts/sets', ExerciseSetViewSet, basename='exercise-sets')
router.register(r'exercises', ExerciseViewSet, basename='exercises')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
