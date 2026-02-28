from django.contrib import admin
from .models import Badge, UserBadge, GamificationAction


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'xp_reward', 'icon_url')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ('user', 'badge', 'earned_at')
    list_filter = ('badge',)
    search_fields = ('user__username', 'badge__name')


@admin.register(GamificationAction)
class GamificationActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_type', 'xp_earned', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('user__username',)
