from django.db import models
from django.conf import settings


class OnboardingEntry(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='onboarding')
    data = models.JSONField(default=dict, help_text="Full questionnaire responses")
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Onboarding for {self.user.username}"


class DailyHabit(models.Model):
    HABIT_TYPES = [
        ('sleep', 'Sleep (Hours)'),
        ('water', 'Water (Liters)'),
        ('steps', 'Steps (Count)'),
        ('stress', 'Stress Level (1-10)'),
        ('nutrition', 'Nutrition Quality (1-10)'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    date = models.DateField()
    habit_type = models.CharField(max_length=20, choices=HABIT_TYPES)
    value = models.FloatField()
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'date', 'habit_type']

    def __str__(self):
        return f"{self.user.username} - {self.habit_type} - {self.date}"


class HealthScore(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_scores')
    date = models.DateField(auto_now_add=True)
    fitness_score = models.IntegerField(default=0)
    recovery_score = models.IntegerField(default=0)
    lifestyle_score = models.IntegerField(default=0)
    consistency_score = models.IntegerField(default=0)
    total_score = models.IntegerField(default=0)

    def __str__(self):
        return f"Score for {self.user.username} on {self.date}: {self.total_score}%"


class UserPlan(models.Model):
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('maintenance', 'Maintenance'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='plan')
    age = models.IntegerField()
    gender = models.CharField(max_length=10, default='male')
    weight = models.FloatField(help_text="Weight in kg")
    height = models.FloatField(help_text="Height in cm")
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    activity_level = models.CharField(max_length=20, default='moderate')
    dietary_preferences = models.TextField(blank=True, null=True)

    # Generated Plan Data
    workout_plan = models.JSONField(default=dict, blank=True)
    nutrition_plan = models.JSONField(default=dict, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Plan for {self.user.username}"
