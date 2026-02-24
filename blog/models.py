from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

class User(AbstractUser):
    """
    Custom User model to allow future extensions.
    """
    bio = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)

class Category(models.Model):
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
        ordering = ['name']

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='articles')
    image_url = models.URLField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.article.title}"

    class Meta:
        ordering = ['created_at']

class UserPlan(models.Model):
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('maintenance', 'Maintenance'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='plan')
    age = models.IntegerField()
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
