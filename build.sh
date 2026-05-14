#!/usr/bin/env bash
set -o errexit

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
cd backend
python manage.py collectstatic --noinput

echo "==> Compiling translations..."
python manage.py compilemessages || echo "Info: compilemessages skipped"

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Seeding database..."
python manage.py seed_db || echo "Info: seed_db skipped"
python manage.py seed_badges || echo "Info: seed_badges skipped"
python manage.py seed_assignment || echo "Info: seed_assignment skipped"
python manage.py fix_unique_images || echo "Info: fix_unique_images skipped"

echo "==> Build complete!"
