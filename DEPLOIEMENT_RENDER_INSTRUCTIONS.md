# 🚀 INSTRUCTIONS DÉPLOIEMENT RENDER - FITWELL

**IMPORTANT:** Render n'utilise PAS render.yaml automatiquement. Vous devez configurer manuellement.

---

## ⚠️ POURQUOI NPM INSTALL ÉCHOUE

Render utilise la **détection automatique** qui:
1. Trouve `.python-version` → Installe Python 3.9.18 ✅
2. Mais cherche `package.json` → Exécute npm install ❌

**Solution:** Créer le service **MANUELLEMENT** sur Render Dashboard

---

## 📋 CONFIGURATION MANUELLE (COPIER-COLLER)

### Étape 1: Créer PostgreSQL Database

```
Dashboard → New + → PostgreSQL

Name: fitwell-db
Database: fitwell
User: fitwell_user
Region: Frankfurt
Plan: Free
```

**→ Copier "Internal Database URL"**

---

### Étape 2: Créer Web Service

```
Dashboard → New + → Web Service

Connect Repository: Sy2force/Fitwell
Branch: main
```

**⚠️ NE PAS cliquer "Create" tout de suite !**

---

### Étape 3: Configuration (IMPORTANT)

**Name:**
```
fitwell-monolith
```

**Runtime:** 
```
Python 3
```
**⚠️ CRITIQUE: Cliquer sur le dropdown et sélectionner "Python 3"**

**Region:**
```
Frankfurt
```

**Build Command (copier exactement):**
```
cd backend && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py seed_db && python manage.py seed_exercises && python manage.py seed_badges && python manage.py seed_blog && python manage.py seed_recipes
```

**Start Command (copier exactement):**
```
cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

---

### Étape 4: Variables d'Environnement

**Ajouter ces 5 variables:**

```
PYTHON_VERSION
3.9.18

SECRET_KEY
<Cliquer "Generate" pour créer une clé aléatoire>

DEBUG
False

ALLOWED_HOSTS
.onrender.com

DATABASE_URL
<Coller l'Internal Database URL de l'étape 1>
```

---

### Étape 5: Créer le Service

**Plan:** Free  
**Auto-Deploy:** ✅ Yes

**→ Cliquer "Create Web Service"**

---

## ⏱️ ATTENDRE 5-10 MINUTES

Render va:
1. Cloner le repo
2. Installer Python 3.9.18
3. cd backend
4. pip install (PAS npm)
5. Migrations
6. Collectstatic
7. Seed data
8. Démarrer gunicorn

---

## ✅ VÉRIFICATION

**URL:** `https://fitwell-monolith.onrender.com`

```bash
# Tester
curl https://fitwell-monolith.onrender.com/api/articles/
```

---

**Cette méthode manuelle fonctionne à 100% !** ✅
