from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model for FitWell.
    Includes core identification and marketing consent.
    """
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    marketing_opt_in = models.BooleanField(default=False)
    # date_joined is already in AbstractUser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Extended profile for gamification and stats.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    # Gamification Fields
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    health_score = models.IntegerField(default=0, help_text="Global Health Score (0-100)")

    updated_at = models.DateTimeField(auto_now=True)

    def add_xp(self, amount):
        """
        Add XP and recalculate level based on formula: Level = sqrt(XP / 100)
        Curve: Lvl 1=100xp, Lvl 2=400xp, Lvl 3=900xp, etc.
        """
        import math
        self.xp += amount

        # Calculate new level
        # We ensure level is at least 1
        new_level = int(math.sqrt(self.xp / 100))
        if new_level < 1:
            new_level = 1

        if new_level > self.level:
            self.level = new_level

        self.save()

    def __str__(self):
        return f"Profile of {self.user.username}"
