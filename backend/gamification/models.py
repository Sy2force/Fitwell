from django.db import models
from django.conf import settings


class Badge(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    icon_url = models.URLField(blank=True, null=True)
    xp_reward = models.IntegerField(default=0)
    condition_code = models.CharField(max_length=50, help_text="Internal code to trigger badge check", unique=True)

    def __str__(self):
        return self.name


class UserBadge(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']

    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"


class GamificationAction(models.Model):
    """
    Log of XP earning actions to prevent abuse and track history.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp_logs')
    action_type = models.CharField(max_length=50)  # e.g., 'gym_session', 'daily_login'
    xp_earned = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} +{self.xp_earned}XP ({self.action_type})"
