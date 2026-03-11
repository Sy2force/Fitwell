from django.core.management.base import BaseCommand
from api.models import Recipe

class Command(BaseCommand):
    help = 'Seeds the database with initial recipes'

    def handle(self, *args, **kwargs):
        recipes = [
            {
                "title": "Bowl Flocons d'Avoine Protéiné",
                "category": "breakfast",
                "difficulty": "easy",
                "prep_time_minutes": 10,
                "calories": 450,
                "protein_g": 30,
                "carbs_g": 55,
                "fats_g": 12,
                "ingredients": "80g Flocons d'avoine\n1 scoop Whey Protéine Vanille\n1 Banane\n10g Beurre de cacahuète\n200ml Lait d'amande",
                "instructions": "1. Faire chauffer le lait d'amande.\n2. Mélanger avec les flocons d'avoine et laisser gonfler 2 min.\n3. Incorporer la whey protéine.\n4. Ajouter la banane coupée en rondelles et le beurre de cacahuète sur le dessus.",
                "image_url": "https://images.unsplash.com/photo-1517673132405-a56a62b18caf?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Poulet Rôti & Patates Douces",
                "category": "lunch",
                "difficulty": "easy",
                "prep_time_minutes": 35,
                "calories": 600,
                "protein_g": 45,
                "carbs_g": 60,
                "fats_g": 15,
                "ingredients": "150g Blanc de poulet\n200g Patate douce\n100g Brocolis\n1 c.à.s Huile d'olive\nPaprika, Sel, Poivre",
                "instructions": "1. Préchauffer le four à 200°C.\n2. Couper les patates douces en dés et le poulet en morceaux.\n3. Disposer sur une plaque, arroser d'huile et épicer.\n4. Cuire 25-30 min jusqu'à ce que le poulet soit doré.",
                "image_url": "https://images.unsplash.com/photo-1588166524941-3bf61a9c41db?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Saumon Grillé & Asperges",
                "category": "dinner",
                "difficulty": "medium",
                "prep_time_minutes": 20,
                "calories": 520,
                "protein_g": 35,
                "carbs_g": 10,
                "fats_g": 35,
                "ingredients": "1 Pavé de saumon (150g)\n200g Asperges vertes\nCitron\nAneth\n15g Amandes effilées",
                "instructions": "1. Cuire les asperges à la vapeur ou à l'eau 8 min.\n2. Poêler le saumon côté peau pendant 6 min, puis retourner 2 min.\n3. Servir avec un filet de citron, l'aneth et les amandes.",
                "image_url": "https://images.unsplash.com/photo-1467003909585-2f8a7270028d?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Shake Post-Workout Récup",
                "category": "shake",
                "difficulty": "easy",
                "prep_time_minutes": 5,
                "calories": 350,
                "protein_g": 35,
                "carbs_g": 40,
                "fats_g": 5,
                "ingredients": "1 scoop Whey Protéine Chocolat\n1 Banane surgelée\n200ml Eau ou Lait\n5g Créatine (optionnel)",
                "instructions": "1. Mettre tous les ingrédients dans un blender.\n2. Mixer jusqu'à obtention d'une texture lisse.\n3. Boire immédiatement après l'entraînement.",
                "image_url": "https://images.unsplash.com/photo-1577805947697-b9843892555d?auto=format&fit=crop&w=800&q=80"
            },
            {
                "title": "Avocado Toast & Œufs Mollets",
                "category": "breakfast",
                "difficulty": "medium",
                "prep_time_minutes": 15,
                "calories": 480,
                "protein_g": 20,
                "carbs_g": 35,
                "fats_g": 28,
                "ingredients": "2 tranches Pain complet\n1/2 Avocat mûr\n2 Œufs\nPiment d'Espelette",
                "instructions": "1. Faire griller le pain.\n2. Écraser l'avocat sur le pain.\n3. Cuire les œufs 6 min dans l'eau bouillante (mollets).\n4. Écaler et poser sur les tartines. Saupoudrer de piment.",
                "image_url": "https://images.unsplash.com/photo-1588137372308-15f75323a51d?auto=format&fit=crop&w=800&q=80"
            }
        ]

        self.stdout.write(self.style.SUCCESS("🥗 Seeding Recipes..."))
        for data in recipes:
            recipe, created = Recipe.objects.update_or_create(
                title=data["title"], 
                defaults=data
            )
            if created:
                self.stdout.write(f"   Created: {recipe.title}")
            else:
                self.stdout.write(f"   Updated: {recipe.title}")
        
        self.stdout.write(self.style.SUCCESS("✅ Done!"))
