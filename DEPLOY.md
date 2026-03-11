# 🚀 FitWell - Guide de Déploiement

Ce guide explique comment déployer FitWell (Application Monolithique Django).

- **Hébergeur** : **Render** (Recommandé) ou tout VPS Python.
- **Base de données** : **PostgreSQL** (Hébergé sur Render ou Supabase).
- **Fichiers Statiques** : Gérés par **WhiteNoise** (déjà configuré).

---

## 🛠️ Déploiement sur Render

1. **Créer un nouveau Web Service** sur [Render](https://dashboard.render.com/).
2. **Connecter votre dépôt GitHub/GitLab**.
3. **Paramètres de base** :
   - **Root Directory** : `backend`
   - **Runtime** : `Python 3`
   - **Build Command** : `pip install -r requirements.txt && python manage.py compilemessages && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command** : `gunicorn config.wsgi:application`

4. **Variables d'Environnement** :
   - `PYTHON_VERSION`: `3.9.0` (ou plus récent)
   - `SECRET_KEY`: *Générez une clé aléatoire forte*
   - `DEBUG`: `False`
   - `DATABASE_URL`: *Lien de connexion PostgreSQL (ex: postgres://user:pass@host/db)*
   - `ALLOWED_HOSTS`: `*` (ou votre domaine render, ex: `fitwell.onrender.com`)

5. **Déployer**.

---

## 📂 Structure du Projet

Le projet est maintenant entièrement contenu dans le dossier `backend` :

```text
/
├── backend/            # Application Django Complète
│   ├── manage.py
│   ├── requirements.txt
│   ├── config/         # Settings & URLs
│   ├── api/            # API REST & Modèles
│   ├── web/            # Frontend (Templates HTML/CSS)
│   └── ...
├── _dev_only/          # Scripts utilitaires
└── ...
```

---

## 🔄 Étapes Post-Déploiement

1. **Créer un Superutilisateur** :
   - Dans le Shell de Render (onglet "Connect") :
     ```bash
     python manage.py createsuperuser
     ```

2. **Charger des données de démo (Optionnel)** :
   - Dans le Shell de Render (onglet "Connect") :
     ```bash
     python manage.py seed_db
     ```
     *(Ceci peuplera la base de données avec des articles, exercices et recettes)*
