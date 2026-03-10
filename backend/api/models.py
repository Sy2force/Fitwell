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

    def __str__(self):
        return f"Stats for {self.user.username}"

# -----------------------------------------------------------------------------
# PLANNER / WELLNESS
# -----------------------------------------------------------------------------
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
