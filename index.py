#!/usr/bin/env python3
"""
Entry point pour Vercel - Django WSGI Application
"""
import os
import sys

# Ajouter le répertoire backend au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Importer et configurer Django
import django
django.setup()

# Importer l'application WSGI
from config.wsgi import application

# Exposer l'application pour Vercel
app = application

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
