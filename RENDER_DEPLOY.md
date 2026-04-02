# DÉPLOIEMENT RENDER - FITWELL

## ⚠️ IMPORTANT
Le service existant qui lance npm DOIT être supprimé.
Créer un NOUVEAU service avec ces paramètres exacts.

---

## CONFIGURATION

**Name:** fitwell

**Runtime:** Python 3 (sélectionner dans dropdown)

**Root Directory:** backend

**Build Command:**
```
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

**Start Command:**
```
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

---

## VARIABLES (5)

```
PYTHON_VERSION=3.9.18
SECRET_KEY=hackeru-fitwell-demo-2026
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<Internal Database URL PostgreSQL>
```

**Pour DATABASE_URL:**
- Aller dans PostgreSQL Database (fitwell-db)
- Copier "Internal Database URL"
- Format: postgresql://user:pass@host:5432/db
- PAS https://

---

## APRÈS DÉPLOIEMENT

Shell Render:
```bash
cd backend
python manage.py seed_db
python manage.py seed_exercises
python manage.py seed_badges
python manage.py seed_blog
python manage.py seed_recipes
```

---

✅ Correction DATABASE_URL appliquée dans settings.py
✅ Tests: 30/30 OK
✅ Prêt pour déploiement
