# 🚀 DÉPLOIEMENT RENDER - CONFIGURATION MANUELLE

**Problème**: Render ignore render.yaml et essaie npm install  
**Solution**: Configuration manuelle du service

---

## ⚠️ IMPORTANT

**Render n'utilise PAS le Blueprint automatiquement.**  
Vous devez créer le service **manuellement** avec ces paramètres exacts.

---

## 📋 ÉTAPES DE DÉPLOIEMENT

### 1. Créer PostgreSQL Database

```
Dashboard Render → New + → PostgreSQL

Name: fitwell-db
Database Name: fitwell
User: fitwell_user
Region: Frankfurt (EU Central)
Plan: Free
```

**Copier l'Internal Database URL** (vous en aurez besoin)

---

### 2. Créer Web Service

```
Dashboard Render → New + → Web Service

Repository: Sy2force/Fitwell
Branch: main
```

**⚠️ NE PAS cliquer "Auto-Deploy" - Configurer d'abord !**

---

### 3. Configuration du Service

**Name:**
```
fitwell-monolith
```

**Runtime:**
```
Python 3
```
**⚠️ IMPORTANT: Sélectionner "Python 3" dans le dropdown, PAS "Node"**

**Region:**
```
Frankfurt (EU Central)
```

**Branch:**
```
main
```

**Build Command:**
```
cd backend && pip install --upgrade pip && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput --clear && python manage.py compilemessages && python manage.py seed_db && python manage.py seed_exercises && python manage.py seed_blog && python manage.py seed_badges && python manage.py seed_recipes
```

**Start Command:**
```
cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile -
```

---

### 4. Variables d'Environnement

**Ajouter ces variables:**

```
PYTHON_VERSION=3.9.18
SECRET_KEY=<cliquer "Generate" pour créer une clé aléatoire>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<coller l'Internal Database URL de l'étape 1>
```

**Pour DATABASE_URL:**
- Aller dans votre PostgreSQL Database
- Copier "Internal Database URL"
- Coller dans la variable DATABASE_URL

---

### 5. Plan et Déploiement

**Plan:**
```
Free
```

**Auto-Deploy:**
```
✅ Activé (déploie automatiquement à chaque push)
```

**Cliquer:** `Create Web Service`

---

## ⏱️ ATTENDRE LE BUILD (5-10 minutes)

Render va:
1. ✅ Cloner le repo
2. ✅ Installer Python 3.9.18
3. ✅ Exécuter `cd backend`
4. ✅ Installer dépendances (pip)
5. ✅ Appliquer migrations
6. ✅ Collecter static files
7. ✅ Seed data (101 exercices, 20 badges, 39 recettes)
8. ✅ Démarrer gunicorn

---

## ✅ VÉRIFICATION

**Une fois déployé:**

```bash
# Tester API
curl https://fitwell-monolith.onrender.com/api/articles/

# Tester Frontend
curl https://fitwell-monolith.onrender.com/fr/

# Admin
https://fitwell-monolith.onrender.com/fr/admin/
```

**Créer superuser (via Shell Render):**
```bash
cd backend
python manage.py createsuperuser
```

---

## 🎯 POURQUOI ÇA VA MARCHER

1. **Runtime: Python 3** - Force Python (pas Node.js)
2. **Build Command avec cd backend** - Va dans le bon dossier
3. **pip install** - Pas npm
4. **DATABASE_URL** - Connecte PostgreSQL
5. **gunicorn** - Démarre Django

---

**Cette configuration manuelle devrait fonctionner à 100% !** ✅
