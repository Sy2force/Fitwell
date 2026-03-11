from django.contrib import admin
from .models import User, Article, Comment, Category, UserStats, WellnessPlan

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Administration des utilisateurs.
    Affiche les infos principales et permet le filtrage par statut/date.
    """
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    Gestion des articles du blog.
    Permet de filtrer par publication et catégorie.
    """
    list_display = ('title', 'author', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'content')

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    """
    Vue admin pour les statistiques de gamification (XP, Niveau).
    """
    list_display = ('user', 'level', 'xp', 'health_score')
    search_fields = ('user__username', 'user__email')

@admin.register(WellnessPlan)
class WellnessPlanAdmin(admin.ModelAdmin):
    """
    Suivi des plans générés par les utilisateurs.
    """
    list_display = ('user', 'goal', 'created_at')
    list_filter = ('goal', 'gender', 'created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Modération des commentaires.
    """
    list_display = ('author', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'article__title')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Gestion des catégories d'articles.
    Le slug est pré-rempli automatiquement basé sur le nom.
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
