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
                "equipment": "Poids du corps",
                "image_url": "https://images.unsplash.com/photo-1598971639058-211a74a96fb4?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Tractions (Pull-ups)",
                "muscle_group": "back",
                "difficulty": "intermediate",
                "description": "Exercice roi pour le dos. Tirez jusqu'à ce que le menton dépasse la barre.",
                "equipment": "Barre de traction",
                "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Squats",
                "muscle_group": "legs",
                "difficulty": "beginner",
                "description": "Flexion des jambes pour travailler les quadriceps et fessiers. Gardez le dos droit.",
                "equipment": "Poids du corps",
                "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Développé Militaire",
                "muscle_group": "shoulders",
                "difficulty": "intermediate",
                "description": "Poussez la charge au-dessus de la tête pour des épaules en béton.",
                "equipment": "Haltères ou Barre",
                "image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Curls Biceps",
                "muscle_group": "arms",
                "difficulty": "beginner",
                "description": "Flexion des bras pour isoler les biceps.",
                "equipment": "Haltères",
                "image_url": "https://images.unsplash.com/photo-1581009137042-c552e485697a?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Planche (Plank)",
                "muscle_group": "abs",
                "difficulty": "beginner",
                "description": "Gainage statique pour renforcer la sangle abdominale profonde.",
                "equipment": "Poids du corps",
                "image_url": "https://images.unsplash.com/photo-1566241142559-40e1dab266c6?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Burpees",
                "muscle_group": "cardio",
                "difficulty": "intermediate",
                "description": "Exercice complet métabolique. Enchaînez squat, pompe et saut.",
                "equipment": "Poids du corps",
                "image_url": "https://images.unsplash.com/photo-1599058945522-28d584b6f0ff?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Soulevé de Terre (Deadlift)",
                "muscle_group": "back",
                "difficulty": "advanced",
                "description": "Exercice polyarticulaire puissant pour toute la chaîne postérieure.",
                "equipment": "Barre",
                "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Dips",
                "muscle_group": "chest",
                "difficulty": "intermediate",
                "description": "Poussée verticale pour le bas des pectoraux et les triceps.",
                "equipment": "Barres parallèles",
                "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917affc?auto=format&fit=crop&w=800&q=80"
            },
            {
                "name": "Fentes (Lunges)",
                "muscle_group": "legs",
                "difficulty": "beginner",
                "description": "Un pas en avant pour travailler l'équilibre et les jambes unilatéralement.",
                "equipment": "Poids du corps",
                "image_url": "https://images.unsplash.com/photo-1574680096145-d05b474e2155?auto=format&fit=crop&w=800&q=80"
            }
        ]

        self.stdout.write(self.style.SUCCESS("🌱 Seeding Exercises..."))
        for data in exercises:
            # Update or create to ensure images are added
            ex, created = Exercise.objects.update_or_create(
                name=data["name"], 
                defaults=data
            )
            if created:
                self.stdout.write(f"   Created: {ex.name}")
            else:
                self.stdout.write(f"   Updated: {ex.name}")
        
        self.stdout.write(self.style.SUCCESS("✅ Done!"))
