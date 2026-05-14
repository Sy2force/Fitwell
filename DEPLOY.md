# 🚀 Déploiement FitWell sur Render

FitWell est une application Django monolithique. Elle se déploie sur **Render** via un Blueprint.

## Prérequis

- Compte GitHub avec accès au repo `Sy2force/Fitwell`
- Compte Render (plan gratuit suffisant) : https://render.com

## Déploiement via Blueprint (recommandé)

Render lit automatiquement `render.yaml` à la racine et crée tout ce qu'il faut.

### 1. S'assurer que le code est à jour

```bash
git push origin main
```

### 2. Créer le Blueprint sur Render

1. Aller sur https://dashboard.render.com
2. **New +** → **Blueprint**
3. Sélectionner le repo `Sy2force/Fitwell`, branche `main`
4. Render détecte `render.yaml` → cliquer **Apply**

Render va automatiquement :

- créer la base PostgreSQL `fitwell-db`
- créer le service web `fitwell-monolith` (Python 3.11.9, root dir `backend`)
- lier `DATABASE_URL` à l'Internal Connection String de la DB
- générer `SECRET_KEY`
- exécuter `./build_files.sh` (pip install, collectstatic, migrate, compilemessages, seed)
- démarrer `gunicorn config.wsgi:application`

### 3. Attendre

Le premier build prend 8 à 12 minutes sur le plan free.
Quand le statut passe à **Live** (point vert), l'URL est :
`https://fitwell-monolith.onrender.com/en/`

## Variables d'environnement

Toutes définies par `render.yaml` — ne pas les modifier manuellement sauf besoin :

| Variable | Source | Valeur |
|---|---|---|
| `SECRET_KEY` | générée par Render | aléatoire |
| `DEBUG` | render.yaml | `False` |
| `ALLOWED_HOSTS` | render.yaml | `.onrender.com` |
| `LANGUAGE_CODE` | render.yaml | `en` |
| `TIME_ZONE` | render.yaml | `UTC` |
| `PYTHON_VERSION` | render.yaml | `3.11.9` |
| `DATABASE_URL` | lié auto à `fitwell-db` | `postgresql://...` |

## Re-déploiement

À chaque push sur `main`, Render redéploie automatiquement.

Pour forcer un redeploy : Service → **Manual Deploy** → **Clear build cache & deploy**.

## Dépannage

### `dj_database_url.UnknownSchemeError`

`DATABASE_URL` ne commence pas par `postgresql://`. Vérifier dans Service → Environment que la variable est bien liée via "Add from Database" → `fitwell-db` → Internal Connection String.

### `ModuleNotFoundError`

Ajouter le paquet manquant dans `backend/requirements.txt` puis push.

### Page d'accueil 404

Vérifier que `healthCheckPath` (défaut `/en/`) est accessible et que `LANGUAGE_CODE=en`.

### Build n'exécute pas le script

Service → Settings : `Root Directory` doit être `backend`, `Build Command` = `./build_files.sh`.

## Compte admin

Créé via le seed. Identifiants par défaut (à changer en production) :

- username : `admin`
- password : `adminpassword`
- URL : `/admin/`

Pour changer le mot de passe :

```bash
python manage.py changepassword admin
```

## Lancer en local

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_db
python manage.py seed_badges
python manage.py runserver
```

Site disponible sur http://localhost:8000/en/
