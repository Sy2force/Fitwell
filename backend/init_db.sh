#!/bin/bash
# Script pour initialiser la base de données sur Render
set -e

echo "==> Initialisation base de données..."
python manage.py migrate --noinput

echo "==> Seed data..."
python manage.py seed_db || echo "Seed DB déjà exécuté"
python manage.py seed_exercises || echo "Exercises déjà seeded"
python manage.py seed_badges || echo "Badges déjà seeded"
python manage.py seed_blog || echo "Blog déjà seeded"
python manage.py seed_recipes || echo "Recipes déjà seeded"

echo "==> Base de données initialisée ✅"
