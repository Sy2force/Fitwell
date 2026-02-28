from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ('email', 'username', 'is_verified', 'marketing_opt_in', 'date_joined', 'is_staff')
    list_filter = ('is_verified', 'marketing_opt_in', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('FitWell Specific', {'fields': ('is_verified', 'marketing_opt_in')}),
    )

    actions = ['export_users_csv']

    def export_users_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fitwell_leads.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username', 'Email', 'Date Joined', 'Marketing Opt-In', 'Level', 'Health Score'])

        for user in queryset:
            # Access profile safely
            level = user.profile.level if hasattr(user, 'profile') else 0
            health_score = user.profile.health_score if hasattr(user, 'profile') else 0

            writer.writerow([
                user.username,
                user.email,
                user.date_joined.strftime("%Y-%m-%d"),
                user.marketing_opt_in,
                level,
                health_score
            ])

        return response

    export_users_csv.short_description = "Export Selected Users (Lead Center)"


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'current_streak', 'health_score', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('level',)
