#!/bin/bash

echo "Building project..."
python3 -m pip install -r requirements.txt

echo "Make migrations..."
python3 backend/manage.py makemigrations
python3 backend/manage.py migrate

echo "Collect static..."
python3 backend/manage.py collectstatic --noinput --clear
