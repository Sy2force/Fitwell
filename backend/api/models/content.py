from django.db import models
from django.utils.text import slugify
from .user import User

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
