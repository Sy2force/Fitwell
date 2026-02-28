from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BadgeViewSet, UserBadgeViewSet, GamificationActionViewSet

router = DefaultRouter()
router.register(r'badges', BadgeViewSet)
router.register(r'my-badges', UserBadgeViewSet, basename='user-badge')
router.register(r'history', GamificationActionViewSet, basename='xp-history')

urlpatterns = [
    path('', include(router.urls)),
]
