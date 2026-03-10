from django.contrib import admin
from .models import User, Article, Comment, Category, UserStats, WellnessPlan

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'date_joined')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'category')
    search_fields = ('title', 'content')

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'health_score')
    search_fields = ('user__username', 'user__email')

@admin.register(WellnessPlan)
class WellnessPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal', 'created_at')
    list_filter = ('goal', 'gender', 'created_at')
    search_fields = ('user__username', 'user__email')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'article', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'author__username', 'article__title')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
