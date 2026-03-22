#!/bin/bash

echo "Building project..."
python3 -m pip install -r backend/requirements.txt

echo "Make migrations..."
cd backend
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

echo "Collect static..."
python3 manage.py collectstatic --noinput --clear

echo "Compile translations..."
python3 manage.py compilemessages

echo "Build completed successfully!"
