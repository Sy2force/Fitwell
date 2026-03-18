#!/bin/bash

echo "Building project..."
python3 -m pip install -r requirements.txt

echo "Make migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

echo "Collect static..."
python3 manage.py collectstatic --noinput --clear
