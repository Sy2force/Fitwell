from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User

# -----------------------------------------------------------------------------
# PLANNER / WELLNESS
# -----------------------------------------------------------------------------
class CustomEvent(models.Model):
    """
    Événements personnalisés pour le planning (Sport, Travail, etc.)
    """
    TYPE_CHOICES = [
        ('sport', _('Sport & fitness')),
        ('work', _('Travail & carrière')),
        ('lifestyle', _('Vie perso & loisirs')),
        ('nutrition', _('Nutrition')),
    ]
    
    PRIORITY_CHOICES = [
        ('low', _('Faible')),
        ('medium', _('Moyenne')),
        ('high', _('Haute')),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_events')
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='work')
    day_of_week = models.CharField(max_length=10, blank=True, null=True) # e.g., 'monday'
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class WellnessPlan(models.Model):
    """
    Plan généré par l'IA.
    Stocke les données biométriques et le résultat JSON.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans')
    
    # Choices
    GENDER_CHOICES = [
        ('male', _('Homme')),
        ('female', _('Femme')),
    ]
    
    GOAL_CHOICES = [
        ('weight_loss', _('Perte de poids')),
        ('muscle_gain', _('Prise de masse')),
        ('maintenance', _('Maintien')),
    ]
    
    ACTIVITY_CHOICES = [
        ('sedentary', _('Sédentaire (peu ou pas d\'exercice)')),
        ('moderate', _('Modéré (1-3 fois par semaine)')),
        ('active', _('Actif (3-5 fois par semaine)')),
        ('elite', _('Élite (6-7 fois par semaine)')),
    ]
    
    # Inputs
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.IntegerField() # cm
    weight = models.FloatField() # kg
    goal = models.CharField(max_length=50, choices=GOAL_CHOICES)
    activity_level = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    
    # Generated Outputs (JSON)
    workout_plan = models.JSONField(default=dict)
    nutrition_plan = models.JSONField(default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plan for {self.user.username} ({self.created_at})"

# -----------------------------------------------------------------------------
# SUIVI QUOTIDIEN (DAILY LOG)
# -----------------------------------------------------------------------------
class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(auto_now_add=True)
    
    # Métriques
    water_liters = models.FloatField(default=0.0)
    sleep_hours = models.FloatField(default=0.0)
    mood = models.IntegerField(default=5) # 1-10
    weight = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"Log {self.user.username} - {self.date}"
