import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from api.models import User, Article, Category, Comment

class Command(BaseCommand):
    help = 'Seed the database with initial blog posts and categories'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('🌱 Seeding Blog Content...'))

        # 1. Create Categories
        categories_data = [
            "Entraînement Tactique",
            "Nutrition & Carburant",
            "Mental & Discipline",
            "Récupération & Bio-Hacking"
        ]
        
        categories = {}
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_name)
            categories[cat_name] = cat
            if created:
                self.stdout.write(f"   Created Category: {cat_name}")

        # 2. Get or Create Admin User for Author
        author, _ = User.objects.get_or_create(username="jarvis_admin")
        if not author.check_password("admin123"):
            author.set_password("admin123")
            author.save()

        # 3. Create Articles
        articles_data = [
            {
                "title": "Les 5 Piliers de l'Hypertrophie Fonctionnelle",
                "category": "Entraînement Tactique",
                "image": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2070&auto=format&fit=crop",
                "content": """
                <p>L'hypertrophie ne sert à rien si elle ne se traduit pas par une performance accrue sur le terrain. Voici comment construire du muscle qui compte.</p>
                <h3>1. Tension Mécanique</h3>
                <p>C'est le facteur principal de la croissance. Soulevez lourd, avec une forme parfaite.</p>
                <h3>2. Stress Métabolique</h3>
                <p>Le "pump" n'est pas juste pour l'ego. L'accumulation de métabolites signale au corps de s'adapter.</p>
                <h3>3. Dommages Musculaires</h3>
                <p>Contrôlés, ils stimulent la réparation et la croissance. Attention au surentraînement.</p>
                """
            },
            {
                "title": "Sommeil : L'Arme Secrète de la Récupération",
                "category": "Récupération & Bio-Hacking",
                "image": "https://images.unsplash.com/photo-1511972844302-9c10cc32b9c4?q=80&w=2070&auto=format&fit=crop",
                "content": """
                <p>Vous pouvez vous entraîner comme une bête, si vous dormez comme un bébé, vous ne grandirez pas. Le sommeil est le moment où la magie opère.</p>
                <p>Optimisez votre environnement : noir total, température fraîche (18°C), et pas d'écrans 1h avant.</p>
                """
            },
            {
                "title": "La Discipline est une Liberté",
                "category": "Mental & Discipline",
                "image": "https://images.unsplash.com/photo-1552674605-46945596497c?q=80&w=2070&auto=format&fit=crop",
                "content": """
                <p>Jocko Willink l'a dit le mieux. La discipline n'est pas une punition, c'est ce qui vous permet d'atteindre vos objectifs.</p>
                <p>Commencez par faire votre lit. C'est la première victoire de la journée.</p>
                """
            },
            {
                "title": "Carburant : Protéines et Timing",
                "category": "Nutrition & Carburant",
                "image": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2053&auto=format&fit=crop",
                "content": """
                <p>Mangez pour la fonction, pas pour le plaisir. La fenêtre anabolique est un mythe, mais l'apport total journalier est roi.</p>
                <p>Visez 2g de protéines par kg de poids de corps pour une récupération optimale.</p>
                """
            },
            {
                "title": "HIIT vs LISS : Quel Cardio pour Vous ?",
                "category": "Entraînement Tactique",
                "image": "https://images.unsplash.com/photo-1434596922112-19c563067271?q=80&w=2070&auto=format&fit=crop",
                "content": """
                <p>Haute intensité ou basse intensité ? La réponse dépend de votre niveau de stress global.</p>
                <p>Le HIIT est efficace mais taxant pour le SNC. Le LISS (marche, vélo lent) aide à la récupération active.</p>
                """
            }
        ]

        for data in articles_data:
            cat = categories.get(data["category"])
            article, created = Article.objects.get_or_create(
                title=data["title"],
                defaults={
                    "author": author,
                    "category": cat,
                    "content": data["content"],
                    "image": data["image"],
                    "is_published": True
                }
            )
            if created:
                self.stdout.write(f"   Created Article: {data['title']}")
            else:
                # Update content if needed (optional)
                article.content = data["content"]
                article.image = data["image"]
                article.category = cat
                article.save()
                self.stdout.write(f"   Updated Article: {data['title']}")

        self.stdout.write(self.style.SUCCESS('✅ Blog Content Seeded!'))
