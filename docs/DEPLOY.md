# 🚀 FitWell - Guide de Déploiement

Ce guide explique comment déployer FitWell, une application **Monolithe Django** complète (Backend + Frontend intégré).

---

## 🏗️ Architecture de Déploiement

- **Application** : Déployée sur **Vercel** (Serverless) ou **Render** (Django + Gunicorn). Sert à la fois l'API et les pages HTML.
- **Base de données** : **PostgreSQL** (Hébergé sur Render, Neon ou Supabase).
- **Fichiers Statiques** : Gérés par **WhiteNoise** et servis par l'application.

---

## 1️⃣ Déploiement Sur Vercel (Recommandé)

Le projet est configuré pour Vercel via `vercel.json` et `index.py`.

### Déploiement via Vercel CLI

1. **Installer Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Configurer les variables d'environnement**
   - `SECRET_KEY`: *Générer une clé forte*
   - `DEBUG`: `False`
   - `DATABASE_URL`: *Lien de connexion PostgreSQL*
   - `ALLOWED_HOSTS`: `.vercel.app,127.0.0.1,localhost`
   - `LANGUAGE_CODE`: `en`

3. **Déployer**
   ```bash
   vercel --prod
   ```

   *(Assurez-vous que le Root Directory est bien la racine du projet)*

4. **Attendre 2-5 minutes**

**URL Production** : `https://votre-projet.vercel.app/en/`

### Déploiement via Dashboard Vercel

1. **Connecter GitHub**
   - https://vercel.com/new
   - Importer le repository `Sy2force/Fitwell`
   - Framework Preset: Other
   - Root Directory: `.` (racine)

2. **Configuration**
   - Build Command: `python3 -m pip install -r backend/requirements.txt && cd backend && python3 manage.py collectstatic --noinput && python3 manage.py compilemessages`
   - Start Command: `python3 index.py`
   - Environment Variables: Ajouter les variables ci-dessus

3. **Deploy** → Attendre le build

---

## 2️⃣ Déploiement Sur Render (Alternative)

Le projet est configuré pour Render via `render.yaml` (Blueprint automatique).

### Déploiement via Blueprint (Automatique)

1. **Push sur GitHub**
   ```bash
   git push origin main
   ```

2. **Render Dashboard**
   - https://dashboard.render.com
   - New + → Blueprint
   - Repository: `Sy2force/Fitwell`
   - Branch: `main`
   - Apply

Render créera automatiquement :
- PostgreSQL Database (`fitwell-db`)
- Web Service (`fitwell-monolith`)
- Lien automatique `DATABASE_URL`
- Seed data automatique

3. **Attendre 5-10 minutes**

**URL Production** : `https://fitwell-monolith.onrender.com/en/`

### Configuration Variables (Auto-configurées)

- `SECRET_KEY` (généré automatiquement)
- `DEBUG=False`
- `ALLOWED_HOSTS=.onrender.com`
- `LANGUAGE_CODE=en`
- `DATABASE_URL` (lié automatiquement à PostgreSQL)

---

## 2️⃣ Initialisation de la Base de Données

Une fois le Backend en ligne, vous devez initialiser la BDD.

Si vous êtes sur **Render** (via Shell) ou en local connecté à la BDD de prod :

```bash
# Appliquer les migrations
python3 backend/manage.py migrate

# Créer un superutilisateur
python3 backend/manage.py createsuperuser

# Peupler la base de données (Essentiel !)
python3 backend/manage.py seed_db        # Données de base
python3 backend/manage.py seed_exercises # 100+ Exercices
python3 backend/manage.py seed_blog      # Articles
python3 backend/manage.py seed_badges    # Badges de gamification
python3 backend/manage.py seed_recipes   # Recettes
```

---

## 📂 Structure du Projet

```text
/
├── backend/            # API & Web App Django (Monolithe)
│   ├── config/         # Settings & URLs
│   ├── api/            # Logique métier, Modèles (DRF)
│   ├── web/            # Vues et Templates Django (Frontend)
│   └── build_files.sh  # Script de build (Render)
├── vercel.json         # Config de déploiement Vercel
├── index.py            # Entrypoint Vercel (WSGI)
├── render.yaml         # Config de déploiement Render (Blueprint)
├── DEPLOY.md           # Guide de déploiement (ce fichier)
└── ...
```
