# 🚀 FitWell - Guide de Déploiement

Ce guide explique comment déployer FitWell, une application complète composée d'un Backend Django (API) et d'un Frontend React.

---

## 🏗️ Architecture de Déploiement

- **Backend (API Django)** : Peut être déployé sur **Vercel** (Serverless) ou **Render** (Docker/Python).
- **Frontend (React/Vite)** : Déployé sur **Vercel** (Recommandé).
- **Base de données** : **PostgreSQL** (Hébergé sur Render, Neon ou Supabase).
- **Fichiers Statiques (Backend)** : Gérés par **WhiteNoise**.

---

## 1️⃣ Déploiement Backend (API)

### Option A : Sur Vercel (Serverless - Recommandé pour le coût)

Le projet est configuré pour Vercel via `vercel.json` et `index.py`.

1. **Installer Vercel CLI** (ou lier via le dashboard GitHub).
2. **Configurer les variables d'environnement** :
   - `SECRET_KEY`: *Générer une clé forte*
   - `DEBUG`: `False`
   - `DATABASE_URL`: *Lien de connexion PostgreSQL*
   - `ALLOWED_HOSTS`: `.vercel.app,127.0.0.1,localhost`
3. **Déployer** :
   ```bash
   vercel --prod
   ```
   *(Assurez-vous que le Root Directory est bien la racine du projet)*

### Option B : Sur Render (Serveur Traditionnel)

1. **Créer un Web Service** sur Render.
2. **Root Directory** : `.` (Racine)
3. **Build Command** : `chmod +x backend/build_files.sh && ./backend/build_files.sh`
4. **Start Command** : `gunicorn config.wsgi:application`
5. **Variables** : Idem Vercel.

---

## 2️⃣ Déploiement Frontend (React)

Le frontend se trouve dans le dossier `frontend/`.

1. **Sur Vercel**, importer le projet.
2. **Framework Preset** : Vite.
3. **Root Directory** : `frontend`.
4. **Variables d'environnement** :
   - `VITE_API_URL` : L'URL de votre Backend déployé (ex: `https://fitwell-api.vercel.app/api`).
5. **Déployer**.

---

## 3️⃣ Initialisation de la Base de Données

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
├── backend/            # API Django (Django REST Framework)
│   ├── config/         # Settings & URLs
│   ├── api/            # Logique métier, Modèles, Vues
│   ├── web/            # Templates Legacy (si utilisé)
│   └── build_files.sh  # Script de build
├── frontend/           # Application React (Vite)
│   ├── src/            # Code source React
│   └── vercel.json     # Config de déploiement Frontend
├── vercel.json         # Config de déploiement Backend
├── index.py            # Entrypoint Vercel (Backend)
└── ...
```
