# RENDER SETUP - FITWELL

## PostgreSQL Database
Name: fitwell-db
Database: fitwell
Plan: Free
→ Copier "Internal Database URL"

## Web Service (NOUVEAU - pas redeploy)
Repository: Sy2force/Fitwell
Branch: main
Runtime: Python 3 (dropdown)
Root Directory: backend

Build Command:
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput

Start Command:
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

Variables:
PYTHON_VERSION=3.9.18
SECRET_KEY=<Generate>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<Internal Database URL>

## Après déploiement (Shell Render):
cd backend
python manage.py seed_db
python manage.py seed_exercises
python manage.py seed_badges
python manage.py seed_blog
python manage.py seed_recipes
