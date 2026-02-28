from django.contrib import admin
from .models import Exercise, Program, WorkoutSession, WorkoutSet


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group', 'difficulty', 'equipment')
    list_filter = ('muscle_group', 'difficulty', 'equipment')
    search_fields = ('name', 'description')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficulty', 'days_per_week', 'duration_weeks', 'is_public')
    list_filter = ('difficulty', 'is_public')
    search_fields = ('name',)


class WorkoutSetInline(admin.TabularInline):
    model = WorkoutSet
    extra = 0


@admin.register(WorkoutSession)
class WorkoutSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'program', 'date', 'status', 'duration_minutes')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'notes')
    inlines = [WorkoutSetInline]


@admin.register(WorkoutSet)
class WorkoutSetAdmin(admin.ModelAdmin):
    list_display = ('session', 'exercise', 'set_order', 'reps', 'weight', 'completed')
    list_filter = ('completed',)
    search_fields = ('exercise__name', 'session__user__username')
