from django.core.management.base import BaseCommand
from api.models import Badge

class Command(BaseCommand):
    help = 'Seeds badges and achievements'

    def handle(self, *args, **kwargs):
        badges = [
            # WORKOUT BADGES
            {"name": "Première Séance", "slug": "first-workout", "description": "Complète ta première séance d'entraînement", "category": "workout", "icon": "🎯", "condition_type": "workout_count", "condition_value": 1, "xp_reward": 50},
            {"name": "Guerrier", "slug": "warrior-10", "description": "Complète 10 séances d'entraînement", "category": "workout", "icon": "⚔️", "condition_type": "workout_count", "condition_value": 10, "xp_reward": 200},
            {"name": "Spartiate", "slug": "spartan-25", "description": "Complète 25 séances d'entraînement", "category": "workout", "icon": "🛡️", "condition_type": "workout_count", "condition_value": 25, "xp_reward": 500},
            {"name": "Titan", "slug": "titan-50", "description": "Complète 50 séances d'entraînement", "category": "workout", "icon": "⚡", "condition_type": "workout_count", "condition_value": 50, "xp_reward": 1000},
            {"name": "Légende", "slug": "legend-100", "description": "Complète 100 séances d'entraînement", "category": "workout", "icon": "👑", "condition_type": "workout_count", "condition_value": 100, "xp_reward": 2500},
            
            # VOLUME BADGES
            {"name": "Force Montante", "slug": "volume-1000", "description": "Soulève 1000kg de volume total", "category": "workout", "icon": "💪", "condition_type": "total_volume", "condition_value": 1000, "xp_reward": 300},
            {"name": "Powerlifter", "slug": "volume-5000", "description": "Soulève 5000kg de volume total", "category": "workout", "icon": "🏋️", "condition_type": "total_volume", "condition_value": 5000, "xp_reward": 800},
            {"name": "Hercule", "slug": "volume-10000", "description": "Soulève 10000kg de volume total", "category": "workout", "icon": "💎", "condition_type": "total_volume", "condition_value": 10000, "xp_reward": 1500},
            
            # STREAK BADGES
            {"name": "Démarrage", "slug": "streak-3", "description": "Maintiens une série de 3 jours", "category": "streak", "icon": "🔥", "condition_type": "current_streak", "condition_value": 3, "xp_reward": 100},
            {"name": "Constance", "slug": "streak-7", "description": "Maintiens une série de 7 jours", "category": "streak", "icon": "🔥🔥", "condition_type": "current_streak", "condition_value": 7, "xp_reward": 250},
            {"name": "Discipline de Fer", "slug": "streak-14", "description": "Maintiens une série de 14 jours", "category": "streak", "icon": "🔥🔥🔥", "condition_type": "current_streak", "condition_value": 14, "xp_reward": 500},
            {"name": "Implacable", "slug": "streak-30", "description": "Maintiens une série de 30 jours", "category": "streak", "icon": "🌟", "condition_type": "current_streak", "condition_value": 30, "xp_reward": 1000},
            {"name": "Invincible", "slug": "streak-100", "description": "Maintiens une série de 100 jours", "category": "streak", "icon": "👑", "condition_type": "current_streak", "condition_value": 100, "xp_reward": 5000},
            
            # MILESTONE BADGES
            {"name": "Bienvenue", "slug": "welcome", "description": "Crée ton compte FitWell", "category": "milestone", "icon": "🎉", "condition_type": "account_created", "condition_value": 1, "xp_reward": 25},
            {"name": "Planificateur", "slug": "first-plan", "description": "Génère ton premier plan wellness", "category": "milestone", "icon": "🧠", "condition_type": "plan_count", "condition_value": 1, "xp_reward": 100},
            {"name": "Niveau 10", "slug": "level-10", "description": "Atteins le niveau 10", "category": "milestone", "icon": "⭐", "condition_type": "level", "condition_value": 10, "xp_reward": 500},
            {"name": "Niveau 25", "slug": "level-25", "description": "Atteins le niveau 25", "category": "milestone", "icon": "🌟", "condition_type": "level", "condition_value": 25, "xp_reward": 1500},
            {"name": "Niveau 50", "slug": "level-50", "description": "Atteins le niveau 50", "category": "milestone", "icon": "💫", "condition_type": "level", "condition_value": 50, "xp_reward": 5000},
            
            # SOCIAL BADGES
            {"name": "Contributeur", "slug": "first-comment", "description": "Poste ton premier commentaire", "category": "social", "icon": "💬", "condition_type": "comment_count", "condition_value": 1, "xp_reward": 50},
            {"name": "Engagé", "slug": "comments-10", "description": "Poste 10 commentaires", "category": "social", "icon": "📢", "condition_type": "comment_count", "condition_value": 10, "xp_reward": 200},
        ]

        self.stdout.write(self.style.SUCCESS(f"🏆 Seeding {len(badges)} Badges..."))
        created_count = 0
        updated_count = 0
        
        for data in badges:
            badge, created = Badge.objects.update_or_create(
                slug=data["slug"],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"   ✅ {badge.icon} {badge.name}"))
            else:
                updated_count += 1
                self.stdout.write(f"   🔄 {badge.icon} {badge.name}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Done! Created: {created_count} | Updated: {updated_count}"))
