from django.core.management.base import BaseCommand
from django.core.management import call_command
from api.models import User

class Command(BaseCommand):
    help = 'Seeds the database with initial data (Users, Articles, Exercises, Recipes)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@fitwell.local', 'adminpassword')
            self.stdout.write(self.style.SUCCESS('Created superuser admin/adminpassword'))

        # 2. Call specialized seed commands
        self.stdout.write('Calling seed_blog...')
        call_command('seed_blog')

        self.stdout.write('Calling seed_exercises...')
        call_command('seed_exercises')
        
        self.stdout.write('Calling seed_recipes...')
        call_command('seed_recipes')

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
