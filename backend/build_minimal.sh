#!/bin/bash
set -e

echo "==> Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "==> Applying migrations..."
python3 manage.py migrate --noinput

echo "==> Collecting static files..."
python3 manage.py collectstatic --noinput --clear

echo "==> Build completed successfully!"
