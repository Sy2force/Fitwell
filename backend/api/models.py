from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# -----------------------------------------------------------------------------
# UTILISATEUR PERSONNALISÉ
# -----------------------------------------------------------------------------
class User(AbstractUser):
    """
    On étend l'utilisateur de base Django pour ajouter :
    - Une bio
    - Une photo de profil (avatar) -> URL pour ce prototype
    """
    bio = models.TextField(blank=True)
    avatar = models.CharField(max_length=500, blank=True, null=True) # Changed from ImageField to CharField for URL support
    
    # Champs marketing / admin
    marketing_opt_in = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# -----------------------------------------------------------------------------
# CATÉGORIES
# -----------------------------------------------------------------------------
class Category(models.Model):
    """
    Les thèmes du blog (ex: Nutrition, Force, Mental).
    Le slug est généré automatiquement si on ne le remplit pas.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

# -----------------------------------------------------------------------------
# ARTICLES
# -----------------------------------------------------------------------------
class Article(models.Model):
    """
    Le cœur du contenu.
    Chaque article a un auteur, une catégorie et une image.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    content = models.TextField()
    image = models.CharField(max_length=500, blank=True, null=True) # Changed to CharField for URL support
    is_published = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)
    
    # Dates auto-gérées
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Génération auto du slug (URL friendly) depuis le titre
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# -----------------------------------------------------------------------------
# COMMENTAIRES
# -----------------------------------------------------------------------------
class Comment(models.Model):
    """
    Les réactions des utilisateurs sous un article.
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"

# -----------------------------------------------------------------------------
# GAMIFICATION & STATS
# -----------------------------------------------------------------------------
class UserStats(models.Model):
    """
    Statistiques et progression de l'utilisateur.
    Lié en OneToOne avec User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    current_streak = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    health_score = models.IntegerField(default=0)
    
    # Scores détaillés (Radar Chart)
    fitness_score = models.IntegerField(default=0)
    recovery_score = models.IntegerField(default=0)
    lifestyle_score = models.IntegerField(default=0)
    consistency_score = models.IntegerField(default=0)

    def update_streak(self):
        """
        Updates the current streak based on last activity date.
        Should be called whenever a significant action (login, plan generation) occurs.
        """
        from django.utils import timezone
        today = timezone.now().date()
        
        if self.last_activity_date == today:
            return # Already counted for today
            
        if self.last_activity_date == today - timezone.timedelta(days=1):
            self.current_streak += 1
        else:
            self.current_streak = 1
            
        self.last_activity_date = today
        self.save()

    def add_xp(self, amount):
        """
        Adds XP and handles leveling up.
        """
        self.xp += amount
        # Formula: Level N requires N * 500 XP
        required_xp = self.level * 500
        
        while self.xp >= required_xp:
            self.xp -= required_xp
            self.level += 1
            required_xp = self.level * 500
            
        self.save()

    @property
    def xp_threshold(self):
        return self.level * 500

    @property
    def xp_progress(self):
        if self.xp_threshold == 0: return 0
        return int((self.xp / self.xp_threshold) * 100)

    @property
    def xp_remaining(self):
        return self.xp_threshold - self.xp

    def __str__(self):
        return f"Stats for {self.user.username}"

# -----------------------------------------------------------------------------
# PLANNER / WELLNESS
# -----------------------------------------------------------------------------
class CustomEvent(models.Model):
    """
    Événements personnalisés pour le planning (Sport, Travail, etc.)
    """
    TYPE_CHOICES = [
        ('sport', _('Sport & Fitness')),
        ('work', _('Travail & Carrière')),
        ('lifestyle', _('Vie Perso & Loisirs')),
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

# -----------------------------------------------------------------------------
# BIBLIOTHÈQUE D'EXERCICES
# -----------------------------------------------------------------------------
class Exercise(models.Model):
    MUSCLE_CHOICES = [
        ('chest', _('Pectoraux')),
        ('back', _('Dos')),
        ('legs', _('Jambes')),
        ('shoulders', _('Épaules')),
        ('arms', _('Bras')),
        ('abs', _('Abdominaux')),
        ('cardio', _('Cardio')),
        ('full', _('Corps complet')),
    ]
    DIFFICULTY_CHOICES = [
        ('beginner', _('Débutant')),
        ('intermediate', _('Intermédiaire')),
        ('advanced', _('Avancé')),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    muscle_group = models.CharField(max_length=20, choices=MUSCLE_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    description = models.TextField()
    equipment = models.CharField(max_length=100, blank=True)
    image_url = models.CharField(max_length=500, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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

# -----------------------------------------------------------------------------
# NUTRITION / RECETTES
# -----------------------------------------------------------------------------
class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', _('Facile')),
        ('medium', _('Moyen')),
        ('hard', _('Difficile')),
    ]
    
    CATEGORY_CHOICES = [
        ('breakfast', _('Petit Déjeuner')),
        ('lunch', _('Déjeuner')),
        ('dinner', _('Dîner')),
        ('snack', _('Collation')),
        ('shake', _('Shake / Smoothie')),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='easy')
    prep_time_minutes = models.IntegerField(default=15)
    calories = models.IntegerField(default=0)
    protein_g = models.IntegerField(default=0)
    carbs_g = models.IntegerField(default=0)
    fats_g = models.IntegerField(default=0)
    
    ingredients = models.TextField(help_text="Liste des ingrédients séparés par des sauts de ligne")
    instructions = models.TextField(help_text="Étapes de préparation")
    image_url = models.CharField(max_length=500, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

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
        ('weight_loss', _('Perte de Poids')),
        ('muscle_gain', _('Prise de Masse')),
        ('maintenance', _('Maintien')),
    ]
    
    ACTIVITY_CHOICES = [
        ('sedentary', _('Sédentaire (Peu ou pas d\'exercice)')),
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

# Signal pour créer UserStats automatiquement
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_stats(sender, instance, created, **kwargs):
    if created:
        UserStats.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_stats(sender, instance, **kwargs):
    if hasattr(instance, 'stats'):
        instance.stats.save()
