#!/bin/bash
set -e

echo "==> Vercel Build Script"
echo "==> Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "==> Applying migrations..."
cd backend
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "==> Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "==> Compiling translations..."
python manage.py compilemessages || echo "No translations to compile"

echo "==> Vercel build completed!"
