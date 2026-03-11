from django.core.management.base import BaseCommand
from api.models import Exercise

class Command(BaseCommand):
    help = 'Seeds the database with initial exercises'

    def handle(self, *args, **kwargs):
        exercises = [
            {
                "name": "Pompes (Push-ups)",
                "muscle_group": "chest",
                "difficulty": "beginner",
                "description": "Un classique pour le développement des pectoraux et des triceps. Maintenez le corps droit.",
                "equipment": "Poids du corps"
            },
            {
                "name": "Tractions (Pull-ups)",
                "muscle_group": "back",
                "difficulty": "intermediate",
                "description": "Exercice roi pour le dos. Tirez jusqu'à ce que le menton dépasse la barre.",
                "equipment": "Barre de traction"
            },
            {
                "name": "Squats",
                "muscle_group": "legs",
                "difficulty": "beginner",
                "description": "Flexion des jambes pour travailler les quadriceps et fessiers. Gardez le dos droit.",
                "equipment": "Poids du corps"
            },
            {
                "name": "Développé Militaire",
                "muscle_group": "shoulders",
                "difficulty": "intermediate",
                "description": "Poussez la charge au-dessus de la tête pour des épaules en béton.",
                "equipment": "Haltères ou Barre"
            },
            {
                "name": "Curls Biceps",
                "muscle_group": "arms",
                "difficulty": "beginner",
                "description": "Flexion des bras pour isoler les biceps.",
                "equipment": "Haltères"
            },
            {
                "name": "Planche (Plank)",
                "muscle_group": "abs",
                "difficulty": "beginner",
                "description": "Gainage statique pour renforcer la sangle abdominale profonde.",
                "equipment": "Poids du corps"
            },
            {
                "name": "Burpees",
                "muscle_group": "cardio",
                "difficulty": "intermediate",
                "description": "Exercice complet métabolique. Enchaînez squat, pompe et saut.",
                "equipment": "Poids du corps"
            },
            {
                "name": "Soulevé de Terre (Deadlift)",
                "muscle_group": "back",
                "difficulty": "advanced",
                "description": "Exercice polyarticulaire puissant pour toute la chaîne postérieure.",
                "equipment": "Barre"
            },
            {
                "name": "Dips",
                "muscle_group": "chest",
                "difficulty": "intermediate",
                "description": "Poussée verticale pour le bas des pectoraux et les triceps.",
                "equipment": "Barres parallèles"
            },
            {
                "name": "Fentes (Lunges)",
                "muscle_group": "legs",
                "difficulty": "beginner",
                "description": "Un pas en avant pour travailler l'équilibre et les jambes unilatéralement.",
                "equipment": "Poids du corps"
            }
        ]

        self.stdout.write(self.style.SUCCESS("🌱 Seeding Exercises..."))
        for data in exercises:
            ex, created = Exercise.objects.get_or_create(name=data["name"], defaults=data)
            if created:
                self.stdout.write(f"   Created: {ex.name}")
            else:
                self.stdout.write(f"   Exists: {ex.name}")
        
        self.stdout.write(self.style.SUCCESS("✅ Done!"))
