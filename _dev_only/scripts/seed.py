import os
import sys
import django
from pathlib import Path

# Setup Django environment
# Current file is in /_dev_only/scripts/seed.py
# We want to add /backend to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
BACKEND_DIR = BASE_DIR / 'backend'
sys.path.append(str(BACKEND_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import User, Category, Article, Comment
from django.utils.text import slugify

def seed():
    print("🌱 Seeding database...")

    # Create Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@fitwell.local', 'admin123')
        print("✅ Superuser 'admin' created")

    # Create Demo Users
    alice, _ = User.objects.get_or_create(username='Alice_Elite', email='alice@fitwell.local')
    if not alice.check_password('password123'):
        alice.set_password('password123')
        alice.save()
    
    bob, _ = User.objects.get_or_create(username='Bob_Operator', email='bob@fitwell.local')
    if not bob.check_password('password123'):
        bob.set_password('password123')
        bob.save()

    print("✅ Users created")

    # Update User Stats for Demo
    if hasattr(alice, 'stats'):
        alice.stats.xp = 1250
        alice.stats.level = 5
        alice.stats.current_streak = 14
        alice.stats.health_score = 88
        alice.stats.fitness_score = 92
        alice.stats.recovery_score = 75
        alice.stats.lifestyle_score = 85
        alice.stats.consistency_score = 95
        alice.stats.save()
        print("   Updated Alice's stats")

    if hasattr(bob, 'stats'):
        bob.stats.xp = 450
        bob.stats.level = 2
        bob.stats.current_streak = 3
        bob.stats.health_score = 72
        bob.stats.fitness_score = 65
        bob.stats.recovery_score = 80
        bob.stats.lifestyle_score = 60
        bob.stats.consistency_score = 70
        bob.stats.save()
        print("   Updated Bob's stats")

    # Create Categories matching Frontend
    categories_data = [
        ('strength', 'Force'),
        ('nutrition', 'Nutrition'),
        ('mindset', 'Mental'),
        ('recovery', 'Récupération'),
        ('bio-hacking', 'Bio-Hacking')
    ]
    
    categories = {}
    for slug, name in categories_data:
        cat, created = Category.objects.get_or_create(slug=slug, defaults={'name': name})
        categories[slug] = cat
        if created:
            print(f"   Created category: {name}")

    print("✅ Categories created")

    # Create Sample Articles
    articles_data = [
        {
            'title': "La Science de l'Hypertrophie",
            'content': "Pour maximiser la croissance musculaire, il faut comprendre les trois mécanismes de l'hypertrophie : tension mécanique, stress métabolique et dommages musculaires. Une analyse approfondie de l'entraînement sous tension...",
            'category': 'strength',
            'author': alice,
            'image_url': 'https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=2070&auto=format&fit=crop'
        },
        {
            'title': 'Protocole d\'Adaptation Cétogène',
            'content': "Passer d'un moteur métabolique au glucose aux cétones nécessite une phase d'adaptation stricte. Voici le protocole de 14 jours pour optimiser votre flexibilité métabolique sans perte de performance...",
            'category': 'nutrition',
            'author': bob,
            'image_url': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Stoïcisme pour l\'Athlète Moderne',
            'content': "L'obstacle est le chemin. Comment la philosophie antique peut vous aider à traverser la barrière de la douleur lors des entraînements à haute intensité et forger un mental d'acier...",
            'category': 'mindset',
            'author': alice,
            'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Guide de l\'Immersion en Eau Froide',
            'content': "L'immersion en eau froide active les protéines de choc thermique et réduit l'inflammation systémique. Découvrez la durée et la température optimales pour une récupération maximale...",
            'category': 'recovery',
            'author': bob,
            'image_url': 'https://images.unsplash.com/photo-1544367563-12123d8965cd?q=80&w=2000&auto=format&fit=crop'
        },
        {
            'title': 'Optimisation de l\'Architecture du Sommeil',
            'content': "Le sommeil profond et les cycles REM sont là où la magie opère. Outils, suppléments et protocoles pour bio-hacker votre rythme circadien et booster votre production d'hormone de croissance...",
            'category': 'bio-hacking',
            'author': alice,
            'image_url': 'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?q=80&w=2000&auto=format&fit=crop'
        }
    ]

    for article_data in articles_data:
        cat = categories[article_data['category']]
        Article.objects.get_or_create(
            title=article_data['title'],
            defaults={
                'content': article_data['content'],
                'author': article_data['author'],
                'category': cat,
                'image': article_data['image_url'], # Corrected from image_url to image
                'is_published': True
            }
        )

    print("✅ Articles created")

    # Create Comments
    comments_data = [
        "Super article, très instructif !",
        "Merci pour ces conseils.",
        "Je ne suis pas d'accord sur le deuxième point.",
        "Excellent travail, continue comme ça !",
        "Est-ce que tu as des sources pour ça ?"
    ]

    import random

    for article in Article.objects.all():
        # Ensure at least 2 comments per article
        for i in range(2):
            Comment.objects.get_or_create(
                article=article,
                author=random.choice([alice, bob]),
                defaults={'content': comments_data[i % len(comments_data)]}
            )
            
    print("✅ Comments created (2 per article)")

    print("✨ Seeding completed!")

if __name__ == '__main__':
    seed()
