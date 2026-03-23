#!/bin/bash
set -e

echo "==> Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "==> Applying migrations..."
python3 manage.py migrate --noinput

echo "==> Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "==> Compiling translations..."
python3 manage.py compilemessages || echo "No translations to compile"

echo "==> Seeding database (non-blocking)..."
python3 manage.py seed_db || echo "Seed DB skipped (may already exist)"
python3 manage.py seed_exercises || echo "Seed exercises skipped"
python3 manage.py seed_blog || echo "Seed blog skipped"
python3 manage.py seed_badges || echo "Seed badges skipped"
python3 manage.py seed_recipes || echo "Seed recipes skipped"

echo "==> Build completed successfully!"
