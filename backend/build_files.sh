#!/bin/bash
set -e

echo "==> Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r backend/requirements.txt

echo "==> Applying migrations..."
cd backend
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "==> Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "==> Compiling translations..."
python3 manage.py compilemessages || echo "No translations to compile"

echo "==> Build completed successfully!"
