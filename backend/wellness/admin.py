from django.contrib import admin
from .models import OnboardingEntry, DailyHabit, HealthScore


@admin.register(OnboardingEntry)
class OnboardingEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'completed_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('completed_at',)


@admin.register(DailyHabit)
class DailyHabitAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'habit_type', 'value')
    list_filter = ('habit_type', 'date')
    search_fields = ('user__username', 'date')


@admin.register(HealthScore)
class HealthScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'total_score', 'fitness_score', 'lifestyle_score')
    search_fields = ('user__username',)
    ordering = ('-date',)
