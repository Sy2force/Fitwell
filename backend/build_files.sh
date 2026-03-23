#!/bin/bash
set -e

echo "==> Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "==> Applying migrations..."
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "==> Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "==> Compiling translations..."
python3 manage.py compilemessages || echo "No translations to compile"

echo "==> Seeding database..."
python3 manage.py seed_db
python3 manage.py seed_exercises
python3 manage.py seed_blog
python3 manage.py seed_badges
python3 manage.py seed_recipes

echo "==> Build completed successfully!"
