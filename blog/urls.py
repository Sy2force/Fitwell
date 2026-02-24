from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ArticleViewSet, CategoryViewSet, CommentViewSet, UserRegistrationView, UserProfileView, UserPlanViewSet
)

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'plans', UserPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
]
