#!/usr/bin/env python3
"""
Script pour tester toutes les pages et identifier celles qui ne s'affichent pas correctement.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from api.models import WellnessPlan

User = get_user_model()

# Créer un client de test
client = Client()

# Créer un utilisateur de test
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('testpass123')
    user.save()

# Se connecter
client.login(username='testuser', password='testpass123')

# Liste des URLs à tester
urls_to_test = [
    ('/', 'Home'),
    ('/fr/', 'Home FR'),
    ('/fr/login/', 'Login'),
    ('/fr/register/', 'Register'),
    ('/fr/blog/', 'Blog List'),
    ('/fr/profile/', 'Profile'),
    ('/fr/dashboard/', 'Dashboard'),
    ('/fr/planner/', 'Planner'),
    ('/fr/agenda/', 'Agenda'),
    ('/fr/exercises/', 'Exercise Library'),
    ('/fr/nutrition/', 'Recipe List'),
    ('/fr/workout/', 'Workout Session'),
    ('/fr/workout/setup/', 'Workout Setup'),
    ('/fr/workout/start/', 'Workout Start'),
    ('/fr/workout/history/', 'Workout History'),
    ('/fr/analytics/', 'Analytics'),
    ('/fr/leaderboard/', 'Leaderboard'),
    ('/fr/tools/', 'Tools'),
    ('/fr/legal/', 'Legal'),
]

print("\n" + "="*80)
print("TEST DES PAGES FITWELL")
print("="*80 + "\n")

errors = []
warnings = []
success = []

for url, name in urls_to_test:
    try:
        response = client.get(url, follow=True)
        
        if response.status_code == 200:
            # Vérifier si la réponse contient du HTML valide
            content = response.content.decode('utf-8')
            
            # Vérifier les signes d'erreur
            if 'Traceback' in content or 'Exception' in content:
                errors.append(f"❌ {name} ({url}) - Contient une erreur Python")
            elif '{% block' in content or '{% extends' in content:
                errors.append(f"❌ {name} ({url}) - Template non rendu (code Django visible)")
            elif len(content) < 100:
                warnings.append(f"⚠️  {name} ({url}) - Contenu très court ({len(content)} bytes)")
            else:
                success.append(f"✅ {name} ({url}) - OK")
        elif response.status_code == 302:
            warnings.append(f"↪️  {name} ({url}) - Redirection vers {response.url}")
        elif response.status_code == 404:
            errors.append(f"❌ {name} ({url}) - Page non trouvée (404)")
        else:
            errors.append(f"❌ {name} ({url}) - Status {response.status_code}")
            
    except Exception as e:
        errors.append(f"❌ {name} ({url}) - Exception: {str(e)}")

# Afficher les résultats
print("\n📊 RÉSULTATS:\n")

if success:
    print(f"✅ SUCCÈS ({len(success)}):")
    for msg in success:
        print(f"  {msg}")
    print()

if warnings:
    print(f"⚠️  AVERTISSEMENTS ({len(warnings)}):")
    for msg in warnings:
        print(f"  {msg}")
    print()

if errors:
    print(f"❌ ERREURS ({len(errors)}):")
    for msg in errors:
        print(f"  {msg}")
    print()

print("="*80)
print(f"Total: {len(success)} OK | {len(warnings)} Warnings | {len(errors)} Errors")
print("="*80 + "\n")

sys.exit(0 if len(errors) == 0 else 1)
