# FitWell - Sport, Santé & Bien-être

Une plateforme complète comprenant une API REST Django et un Frontend React moderne, conçue pour un blog de fitness et bien-être.

## 📌 Présentation

**FitWell** est une application full-stack permettant de gérer des articles, des catégories et des commentaires, avec un système d'authentification sécurisé et une interface utilisateur élégante.

### Fonctionnalités principales
- **Authentification JWT** : Inscription, Connexion, Refresh Token.
- **Gestion des Articles** : CRUD complet avec catégories et images.
- **Système de Commentaires** : Interaction utilisateur sur les articles.
- **Recherche et Filtrage** : Recherche textuelle et filtres avancés (catégorie, auteur).
- **Documentation API** : Swagger UI intégrée.
- **Frontend React** : Interface responsive avec Vite, Tailwind CSS et Lucide Icons.

---

## 🛠 Installation et Développement Local

### 1. Backend (Django)

**Prérequis** : Python 3.10+

```bash
# Installation des dépendances
pip install -r requirements.txt

# Migrations et Base de données
python manage.py migrate

# (Optionnel) Peupler la base de données avec des données de test
python scripts/populate_db.py

# Lancer le serveur
python manage.py runserver
```
L'API sera accessible sur `http://localhost:8000`. Documentation Swagger : `http://localhost:8000/api/docs/`.

### 2. Frontend (React)

**Prérequis** : Node.js 18+

```bash
cd fitwell-frontend
npm install
npm run dev
```
L'application sera accessible sur `http://localhost:5173`.

---

## 🚀 Déploiement

Le projet est pré-configuré pour un déploiement sur **Render** (Backend) et **Vercel** (Frontend).

### Backend sur Render
1. Créez un **Web Service** sur Render lié à votre repo.
2. Le fichier `render.yaml` et `build.sh` configureront automatiquement l'environnement.
3. Variables d'env à configurer : `SECRET_KEY`, `ALLOWED_HOSTS`, `DATABASE_URL`, `CSRF_TRUSTED_ORIGINS`.

### Frontend sur Vercel
1. Importez le projet sur Vercel.
2. Définissez `fitwell-frontend` comme **Root Directory**.
3. Variable d'env à configurer : `VITE_API_URL` (URL de votre API Render).

---

## 📖 Guide de l'API (Endpoints)

### Authentification
- `POST /api/register/` : Inscription.
- `POST /api/token/` : Connexion (Obtenir token).
- `POST /api/token/refresh/` : Rafraîchir le token.

### Articles & Commentaires
- `GET /api/articles/` : Liste des articles (Filtres: `?category=`, `?search=`).
- `POST /api/articles/` : Créer un article (Auth requis).
- `GET /api/articles/{id}/` : Détails + Commentaires.
- `POST /api/articles/{id}/comments/` : Ajouter un commentaire.

---

## 🧪 Tests E2E (Playwright)

Le projet inclut une suite de tests End-to-End avec Playwright.

```bash
cd fitwell-frontend
# Lancer les tests en mode headless
npm run test:e2e

# Lancer les tests avec l'interface UI (recommandé pour le dev)
npm run test:e2e:ui
```

Les tests couvrent :
- Le chargement de la page d'accueil et du Hero section.
- La navigation vers les pages Login et Register.
- Les fonctionnalités de recherche.
- `blog/` : Logique métier Django (Modèles, Views, Serializers).
- `config/` : Configuration Django (Settings dev/prod).
- `fitwell-frontend/` : Application React (Vite, Tailwind).
- `scripts/` : Scripts d'administration et de test.
- `render.yaml` & `build.sh` : Configuration du déploiement.
