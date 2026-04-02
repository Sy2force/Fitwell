# 🚀 DÉPLOIEMENT FINAL - FITWELL (PROJET HACKERU)

**Date**: 2 Avril 2026, 22:20 UTC+03:00  
**Plateforme recommandée**: **RENDER** (pas Vercel)  
**Statut**: ✅ **PRÊT POUR DÉPLOIEMENT**

---

## ⚠️ VERCEL vs RENDER

### Pourquoi PAS Vercel pour ce projet:

❌ **Vercel:**
- Serverless (limites de temps d'exécution)
- Pas de PostgreSQL inclus
- Problèmes avec Python 3.9 vs 3.12
- Pas adapté pour Django complet
- Pas de commandes seed automatiques

✅ **Render (RECOMMANDÉ):**
- Serveur dédié (pas de limites)
- PostgreSQL inclus (gratuit)
- Support Python 3.9.18 natif
- Parfait pour Django
- Seed data automatique
- Migrations automatiques

---

## 🎯 DÉPLOIEMENT SUR RENDER (MÉTHODE BLUEPRINT)

### Étape 1: Supprimer Service Existant (si échec précédent)

```
1. Dashboard Render → https://dashboard.render.com
2. Aller dans le service qui a échoué
3. Settings → Delete Service
```

### Étape 2: Créer via Blueprint

```
1. Dashboard → New + → Blueprint
2. Repository: Sy2force/Fitwell
3. Branch: main
4. Apply
```

**Render va lire `render.yaml` et créer automatiquement:**
- PostgreSQL Database (fitwell-db)
- Web Service (fitwell)
- Variables d'environnement

---

## 📋 CONFIGURATION MANUELLE (SI BLUEPRINT ÉCHOUE)

### Étape 1: PostgreSQL Database

```
New + → PostgreSQL

Name: fitwell-db
Database: fitwell
User: fitwell_user
Region: Frankfurt
Plan: Free
```

**→ Copier "Internal Database URL"**

---

### Étape 2: Web Service

```
New + → Web Service

Repository: Sy2force/Fitwell
Branch: main
```

**Configuration:**

**Name:** `fitwell`

**Runtime:** `Python 3` ⚠️ **Sélectionner dans dropdown**

**Build Command:**
```
cd backend && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput && python manage.py seed_db && python manage.py seed_exercises && python manage.py seed_badges && python manage.py seed_blog && python manage.py seed_recipes
```

**Start Command:**
```
cd backend && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

**Variables d'environnement:**
```
PYTHON_VERSION=3.9.18
SECRET_KEY=hackeru-fitwell-demo-2026
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<Coller Internal Database URL>
```

---

## ✅ APRÈS DÉPLOIEMENT

**URL:** `https://fitwell.onrender.com`

**Vérifier:**
```bash
# API
curl https://fitwell.onrender.com/api/articles/

# Frontend
https://fitwell.onrender.com/fr/

# Admin
https://fitwell.onrender.com/fr/admin/
```

**Créer superuser (Shell Render):**
```bash
cd backend
python manage.py createsuperuser
```

---

## 📊 DONNÉES INSTALLÉES

**Après seed:**
- 2 Users (admin/adminpassword + demo/demopass123)
- 101 Exercices
- 20 Badges
- 39 Recettes
- 5 Articles
- 6 Catégories

---

## 🎓 POUR PROJET HACKERU

**Ce qu'il faut montrer:**
1. ✅ URL en ligne (Render)
2. ✅ Interface fonctionnelle
3. ✅ Inscription/Connexion
4. ✅ Dashboard avec données
5. ✅ API REST (/swagger/)
6. ✅ Admin Django
7. ✅ Tests passent (30/30)

---

## 🎯 RÉSUMÉ

**Plateforme:** Render (pas Vercel)  
**Méthode:** Blueprint (ou Manuel)  
**Temps:** 5-10 minutes  
**Coût:** Gratuit (Free plan)

**Le projet est 100% prêt pour déploiement Render !** ✅
