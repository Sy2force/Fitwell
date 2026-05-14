#!/usr/bin/env python3
"""
Entry point pour Vercel - Django ASGI Application
"""
import os
import sys

# Ajouter le répertoire backend au path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Importer et configurer Django
import django
django.setup()

# Importer l'application ASGI
from config.asgi import application

# Exposer l'application pour Vercel
app = application
