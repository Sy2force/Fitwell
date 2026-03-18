from django.contrib import admin
from .models import User, Article, Comment, Category, UserStats, WellnessPlan, WorkoutSession, ExerciseSet, Exercise, Recipe, DailyLog, CustomEvent, Badge, UserBadge

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

class ExerciseSetInline(admin.TabularInline):
    """
    Affichage inline des sets dans une session.
    """
    model = ExerciseSet
    extra = 0
    fields = ('exercise', 'set_number', 'reps', 'weight', 'rest_seconds')
    readonly_fields = ('created_at',)

@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    """
    Gestion des séances d'entraînement.
    Affiche les sets en inline pour une vue complète.
    """
    list_display = ('user', 'started_at', 'duration_minutes', 'status', 'total_volume')
    list_filter = ('status', 'started_at')
    search_fields = ('user__username', 'notes')
    readonly_fields = ('started_at', 'completed_at', 'duration_minutes', 'total_volume')
    inlines = [ExerciseSetInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(ExerciseSet)
class ExerciseSetAdmin(admin.ModelAdmin):
    """
    Gestion des sets individuels.
    """
    list_display = ('session', 'exercise', 'set_number', 'reps', 'weight', 'volume')
    list_filter = ('exercise__muscle_group', 'created_at')
    search_fields = ('exercise__name', 'session__user__username')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session__user', 'exercise')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """
    Gestion de la bibliothèque d'exercices.
    """
    list_display = ('name', 'muscle_group', 'difficulty', 'equipment')
    list_filter = ('muscle_group', 'difficulty')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Gestion des recettes nutrition.
    """
    list_display = ('title', 'category', 'difficulty', 'calories', 'protein_g')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'ingredients')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    """
    Suivi des logs quotidiens.
    """
    list_display = ('user', 'date', 'water_liters', 'sleep_hours', 'mood', 'weight')
    list_filter = ('date',)
    search_fields = ('user__username',)
    
@admin.register(CustomEvent)
class CustomEventAdmin(admin.ModelAdmin):
    """
    Gestion des événements personnalisés de l'agenda.
    """
    list_display = ('user', 'title', 'event_type', 'priority', 'is_completed', 'created_at')
    list_filter = ('event_type', 'priority', 'is_completed')
    search_fields = ('user__username', 'title')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    """
    Gestion des badges et achievements.
    """
    list_display = ('icon', 'name', 'category', 'condition_type', 'condition_value', 'xp_reward')
    list_filter = ('category', 'condition_type')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    """
    Suivi des badges débloqués par les utilisateurs.
    """
    list_display = ('user', 'badge', 'unlocked_at')
    list_filter = ('badge__category', 'unlocked_at')
    search_fields = ('user__username', 'badge__name')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'badge')
