from django.core.management.base import BaseCommand
from api.models import User, Category, Article, UserStats
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Categories
        categories_data = ['Nutrition', 'Entraînement', 'Récupération', 'Mental', 'Bio-Hacking']
        for cat_name in categories_data:
            Category.objects.get_or_create(name=cat_name)
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories_data)} categories'))

        # Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@fitwell.local', 'adminpassword')
            self.stdout.write(self.style.SUCCESS('Created superuser admin/adminpassword'))

        # Get admin user for articles
        admin_user = User.objects.get(username='admin')

        # Articles
        articles_data = [
            {
                'title': 'Les 5 Piliers de l\'Hypertrophie',
                'category': 'Entraînement',
                'content': 'L\'hypertrophie musculaire repose sur la tension mécanique, le stress métabolique et les dommages musculaires. Voici comment optimiser chaque facteur...',
                'image': 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=2070'
            },
            {
                'title': 'Sommeil Profond : Le Secret de la Performance',
                'category': 'Récupération',
                'content': 'Sans un sommeil de qualité, votre taux de testostérone chute et votre cortisol grimpe. Découvrez le protocole 10-3-2-1-0 pour des nuits réparatrices.',
                'image': 'https://images.unsplash.com/photo-1511895426328-dc8714191300?q=80&w=2070'
            },
            {
                'title': 'Jeûne Intermittent et Flexibilité Métabolique',
                'category': 'Nutrition',
                'content': 'Le jeûne n\'est pas qu\'une restriction calorique, c\'est un outil pour réapprendre à votre corps à utiliser ses graisses comme carburant.',
                'image': 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?q=80&w=2070'
            },
            {
                'title': 'Dopamine Detox : Reprenez le Contrôle',
                'category': 'Mental',
                'content': 'Dans un monde hyper-connecté, votre système de récompense est saturé. Une détox de dopamine peut restaurer votre motivation et votre concentration.',
                'image': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=2070'
            },
            {
                'title': 'Froid : Pourquoi prendre des douches glacées ?',
                'category': 'Bio-Hacking',
                'content': 'L\'exposition volontaire au froid augmente la noradrénaline de 530%, booste l\'immunité et améliore la résilience mentale.',
                'image': 'https://images.unsplash.com/photo-1520206183501-b80df610434f?q=80&w=2070'
            }
        ]

        for art in articles_data:
            cat = Category.objects.get(name=art['category'])
            Article.objects.get_or_create(
                title=art['title'],
                defaults={
                    'author': admin_user,
                    'category': cat,
                    'content': art['content'],
                    'image': art['image'],
                    'is_published': True
                }
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(articles_data)} articles'))
        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
