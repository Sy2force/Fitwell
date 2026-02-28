from django.db import models
from django.conf import settings


class Exercise(models.Model):
    MUSCLE_GROUPS = [
        ('chest', 'Chest'),
        ('back', 'Back'),
        ('legs', 'Legs'),
        ('shoulders', 'Shoulders'),
        ('arms', 'Arms'),
        ('core', 'Core'),
        ('cardio', 'Cardio'),
        ('full', 'Full Body'),
    ]

    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    muscle_group = models.CharField(max_length=50, choices=MUSCLE_GROUPS)
    equipment = models.CharField(max_length=100, blank=True, help_text="e.g., Dumbbells, Barbell, None")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='beginner')
    video_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    difficulty = models.CharField(max_length=20, choices=Exercise.DIFFICULTY_LEVELS, default='beginner')
    days_per_week = models.IntegerField(default=3)
    duration_weeks = models.IntegerField(default=4)
    is_public = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class WorkoutSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='workout_sessions')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[('started', 'Started'), ('completed', 'Completed'), ('abandoned', 'Abandoned')],
        default='started'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.date.date()}"


class WorkoutSet(models.Model):
    session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name='sets')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    set_order = models.IntegerField(default=1)
    reps = models.IntegerField()
    weight = models.FloatField(help_text="Weight in kg", default=0)
    rpe = models.IntegerField(null=True, blank=True, help_text="Rate of Perceived Exertion (1-10)")
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['set_order']
