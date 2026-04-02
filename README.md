# 🏋️ FitWell - Plateforme Complète de Fitness & Wellness

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

**FitWell** est une plateforme SaaS complète dédiée à la santé, au fitness et à l'optimisation de la performance humaine. Elle combine un planificateur intelligent basé sur l'IA, des outils de suivi d'entraînement, une gamification avancée, et une base de connaissances communautaire.

---

## 📋 Table des Matières

- [Fonctionnalités](#-fonctionnalités-principales)
- [Technologies](#-stack-technique)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [API REST](#-api-rest)
- [Déploiement](#-déploiement)
- [Tests](#-tests)
- [Architecture](#-architecture)
- [Sécurité](#-sécurité)
- [Contribution](#-contribution)
- [License](#-license)

---

## 🚀 Fonctionnalités Principales

### 🎓 Onboarding Intelligent
- Flow guidé en 4 étapes pour nouveaux utilisateurs
- Sélection objectif (Perte poids / Prise masse / Maintien)
- Configuration niveau d'activité (Sédentaire → Élite)
- Collecte données biométriques (Age, Genre, Taille, Poids)
- Génération automatique du premier plan personnalisé
- Attribution badges de bienvenue

### 🧠 AI Planner - Protocoles Personnalisés
- **Génération automatique** de programmes d'entraînement et nutrition
- **Calcul intelligent** des macros (Protéines, Glucides, Lipides) et calories
- **Analyse de santé** avec scoring (0-100) et breakdown détaillé
- **Historique complet** des anciens plans ("Archives")
- **Pré-remplissage** automatique du formulaire avec les données précédentes

**Basé sur:**
- Biométrie (Âge, Poids, Taille, Genre)
- Objectif (Perte de gras, Prise de masse, Maintien)
- Niveau d'activité (Sédentaire, Modéré, Actif, Élite)

### 🏋️ Workout Tracking Complet
- **Démarrage de session** avec timer en temps réel
- **Ajout de sets** (exercice, reps, poids, repos) en AJAX
- **Rest timer** avec notification sonore
- **Calcul automatique** du volume total et de la durée
- **Attribution XP** automatique (50 base + 10 par 10min)
- **Historique complet** avec graphiques détaillés
- **Statistiques globales** par muscle group

### 🏆 Gamification Avancée
- **20 badges débloquables** dans 4 catégories:
  - Workout (Première Séance, Guerrier, Spartiate, Titan, Légende)
  - Volume (Force Montante, Powerlifter, Hercule)
  - Streak (Démarrage, Constance, Discipline de Fer, Implacable, Invincible)
  - Milestones (Bienvenue, Planificateur, Niveau 10/25/50)
  - Social (Contributeur, Engagé)
- **Système XP/Level** avec formule: Level N = N × 500 XP
- **Streaks quotidiens** pour encourager la constance
- **Leaderboard global** (Top XP, Top Streaks, Top Workouts)

### 📊 Analytics Avancées
Page dédiée `/analytics/` avec 6 graphiques interactifs:
- Évolution du poids (30 derniers jours)
- Volume par groupe musculaire (répartition complète)
- Personal Records (PR) - Top 10 exercices
- Fréquence d'entraînement (7 derniers jours)
- Consistency Score (pourcentage sur 30 jours)
- Progression XP (graphique temporel)

### 🎛️ Dashboard - Centre de Commandement
- **Suivi Quotidien (Daily Log)**: Eau, Sommeil, Humeur, Poids
- **Gamification**: Gagnez de l'XP à chaque mise à jour (+20 XP)
- **Vue d'ensemble**: Statistiques hebdomadaires et agenda du jour
- **Graphiques**: Visualisation des tendances

### 📅 Agenda Tactique
- **Planification Hebdomadaire**: Organisez vos blocs Sport, Travail, Vie Perso
- **Gestion des Tâches**: Priorisez vos activités (Haute/Moyenne/Faible)
- **Récompenses**: Cochez vos tâches pour gagner de l'XP

### 🏋️ Bibliothèque Tactique
- **101 exercices** avec images Unsplash
- **Fiches Techniques**: Instructions, difficulté, équipement
- **Filtrage**: Par groupe musculaire et difficulté

### 🥗 Laboratoire Nutrition
- **39 recettes** optimisées (Petit-déj, Déjeuner, Dîner, Shakes)
- **Profil Macro**: Détail précis des protéines, glucides et lipides
- **Filtrage**: Par catégorie et niveau de difficulté

### 📚 Blog & Communauté
- Articles éducatifs sur nutrition, entraînement, bio-hacking
- Système de **Likes** et **Commentaires**
- Filtrage par catégories et recherche textuelle
- Articles reliés automatiques

### 🌍 Internationalisation
- **Support Bilingue**: Français (défaut) et Anglais
- **Interface Adaptative**: Traduction intégrale (Menus, Formulaires, Plans IA)
- **Sélecteur de langue** optimisé Desktop et Mobile

---

## 🛠 Stack Technique

### Backend
- **Framework**: Django 4.2 (Python 3.9+)
- **API REST**: Django REST Framework
- **Authentification**: JWT (djangorestframework-simplejwt) + Sessions Django
- **Base de données**: 
  - SQLite (développement)
  - PostgreSQL (production)
- **ORM**: Django ORM avec migrations
- **Documentation API**: Swagger/OpenAPI (drf-yasg)

### Frontend
- **Templates**: Django Templates (DTL)
- **Styling**: TailwindCSS (via CDN)
- **JavaScript**: Vanilla JS + AJAX
- **Charts**: Chart.js pour analytics
- **Icons**: Lucide Icons

### Infrastructure
- **Server**: Gunicorn (WSGI)
- **Static Files**: WhiteNoise
- **CORS**: django-cors-headers
- **Déploiement**: Render (Backend + PostgreSQL) / Vercel (optionnel)

### Outils de Développement
- **Tests**: Django TestCase (30 tests, 100% réussite)
- **Linting**: Python standards
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions (optionnel)

---

## 📦 Installation

### Pré-requis
- Python 3.9 ou supérieur
- pip (gestionnaire de packages Python)
- Git

### 1. Cloner le Projet

```bash
git clone https://github.com/Sy2force/Fitwell.git
cd fitwell
```

### 2. Créer un Environnement Virtuel

```bash
# Créer l'environnement
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate  # Mac/Linux
# OU
venv\Scripts\activate     # Windows
```

### 3. Installer les Dépendances

```bash
pip install -r backend/requirements.txt
```

### 4. Configuration de la Base de Données

```bash
cd backend

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### 5. Peupler la Base de Données (Optionnel)

```bash
# Seed complet (recommandé)
python manage.py seed_db          # Admin + catégories
python manage.py seed_exercises   # 101 exercices
python manage.py seed_blog        # 5 articles
python manage.py seed_badges      # 20 badges
python manage.py seed_recipes     # 39 recettes
```

**Données créées:**
- 2 utilisateurs (admin + demo)
- 101 exercices avec images
- 5 articles de blog professionnels
- 20 badges débloquables
- 39 recettes nutritionnelles
- 6 catégories

### 6. Compiler les Traductions

```bash
python manage.py compilemessages
```

### 7. Lancer le Serveur

```bash
python manage.py runserver
```

**Accès:**
- Application: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/fr/admin/
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/swagger/

---

## ⚙️ Configuration

### Variables d'Environnement

Créer un fichier `.env` à la racine du projet:

```bash
# Copier le template
cp .env.example .env
```

**Variables principales:**

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Production)
DATABASE_URL=postgresql://user:password@host:port/dbname

# CORS
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# Email (Optionnel)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AWS S3 (Optionnel)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=eu-west-3
```

### Settings Production

Le fichier `backend/config/settings.py` détecte automatiquement l'environnement:

```python
# Développement
DEBUG = True
DATABASES = SQLite

# Production (avec DATABASE_URL)
DEBUG = False
DATABASES = PostgreSQL (via dj-database-url)
STATIC_ROOT = configuré
STATICFILES_STORAGE = WhiteNoise
```

---

## 🎮 Utilisation

### Comptes de Démonstration

Si vous avez exécuté `seed_db`:

**Admin:**
- Username: `admin`
- Password: `adminpassword`

**Demo User:**
- Username: `demo`
- Password: `demopass123`

### Workflow Utilisateur

1. **Inscription** → `/fr/register/`
2. **Onboarding** → Flow 4 étapes automatique
3. **Dashboard** → Vue d'ensemble personnalisée
4. **Planner** → Générer un protocole personnalisé
5. **Workout** → Démarrer une session d'entraînement
6. **Analytics** → Visualiser vos progrès

### Commandes Utiles

```bash
# Tests
python manage.py test api web

# Vérification système
python manage.py check

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Créer des migrations
python manage.py makemigrations

# Shell Django
python manage.py shell

# Vérifier les données
python manage.py shell -c "from api.models import Exercise, Article, Badge; print(f'Exercices: {Exercise.objects.count()}'); print(f'Articles: {Article.objects.count()}'); print(f'Badges: {Badge.objects.count()}')"
```

---

## 🔌 API REST

### Documentation Interactive

**Swagger UI**: http://127.0.0.1:8000/swagger/

### Endpoints Principaux

#### Authentification

```http
POST /api/register/
POST /api/token/
POST /api/token/refresh/
```

#### Contenu

```http
GET    /api/articles/
GET    /api/articles/{id}/
POST   /api/articles/          # Admin uniquement
GET    /api/categories/
GET    /api/comments/
POST   /api/comments/
DELETE /api/comments/{id}/     # Auteur uniquement
```

#### Utilisateurs

```http
GET    /api/users/
GET    /api/users/{id}/
PUT    /api/users/{id}/        # Propriétaire uniquement
```

#### Wellness

```http
GET    /api/wellness/plans/
POST   /api/wellness/plans/
GET    /api/wellness/plans/{id}/
```

#### Workout

```http
GET    /api/workouts/sessions/
POST   /api/workouts/sessions/
GET    /api/workouts/sessions/{id}/
POST   /api/workouts/sets/
GET    /api/exercises/
```

### Authentification API

**JWT Token:**

```bash
# Obtenir le token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Utiliser le token
curl -X GET http://localhost:8000/api/wellness/plans/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Permissions

- **Lecture publique**: Articles, Catégories, Exercices
- **Authentifié**: Plans, Workouts, Profil
- **Auteur uniquement**: Édition/Suppression commentaires
- **Admin uniquement**: Création/Édition articles

---

## 🚀 Déploiement

### Déploiement sur Render (Recommandé)

#### Option 1: Blueprint (Automatique)

1. **Aller sur Render**: https://dashboard.render.com
2. **New +** → **Blueprint**
3. **Connecter repo**: `Sy2force/Fitwell`
4. **Branch**: `main`
5. **Apply** → Render détecte `render.yaml` automatiquement

**Créé automatiquement:**
- PostgreSQL Database (Free)
- Web Service (Free)
- Variables d'environnement
- Build + Seed automatique

#### Option 2: Manuel

**1. Créer PostgreSQL Database**
- Name: `fitwell`
- Plan: Free
- Region: Frankfurt

**2. Créer Web Service**
- Name: `fitwell-monolith`
- Environment: Python 3
- Build Command: `./backend/build_files.sh`
- Start Command: `cd backend && gunicorn config.wsgi:application`

**3. Variables d'Environnement**
```
SECRET_KEY=<générer-une-clé>
DEBUG=False
DATABASE_URL=<auto-lié-depuis-postgresql>
PYTHON_VERSION=3.9.18
```

**4. Déployer**
- Connecter GitHub repo
- Branch: `main`
- Create Web Service

### Déploiement sur Vercel (Frontend uniquement)

```bash
# Installer Vercel CLI
npm install -g vercel

# Déployer
vercel --prod
```

### Post-Déploiement

**Vérifier les endpoints:**
```bash
# API
curl https://your-app.onrender.com/api/articles/

# Frontend
curl https://your-app.onrender.com/fr/

# Admin
https://your-app.onrender.com/fr/admin/
```

**Créer un superutilisateur:**
```bash
# Via Render Shell
python manage.py createsuperuser
```

---

## 🧪 Tests

### Exécuter les Tests

```bash
# Tous les tests
python manage.py test

# Tests spécifiques
python manage.py test api
python manage.py test web

# Avec verbosité
python manage.py test --verbosity=2

# Tests parallèles
python manage.py test --parallel
```

### Couverture des Tests

**30 tests automatisés (100% réussite):**

- **API Tests** (9 tests)
  - Authentification
  - CRUD Articles
  - Logique métier

- **Web Forms** (4 tests)
  - Validation formulaires
  - Données invalides

- **Web Views** (11 tests)
  - Dashboard
  - Planner
  - Profile
  - Blog

- **Flows** (6 tests)
  - Workout complet
  - Filtrage exercices/recettes

**Résultat:**
```
Ran 30 tests in 4.858s
OK
```

---

## 🏗 Architecture

### Structure du Projet

```
fitwell/
├── backend/                    # Application Django
│   ├── api/                    # API REST + Logique Métier
│   │   ├── models/             # Modèles (14 modèles)
│   │   │   ├── user.py
│   │   │   ├── content.py
│   │   │   ├── plan.py
│   │   │   ├── workout.py
│   │   │   ├── nutrition.py
│   │   │   └── gamification.py
│   │   ├── views/              # ViewSets API
│   │   ├── serializers/        # Serializers DRF
│   │   ├── services/           # Logique métier
│   │   │   ├── wellness.py
│   │   │   ├── workout.py
│   │   │   ├── nutrition.py
│   │   │   ├── scoring.py
│   │   │   └── gamification.py
│   │   ├── management/         # Commandes Django
│   │   │   └── commands/
│   │   │       ├── seed_db.py
│   │   │       ├── seed_exercises.py
│   │   │       ├── seed_blog.py
│   │   │       ├── seed_badges.py
│   │   │       └── seed_recipes.py
│   │   ├── migrations/         # Migrations DB
│   │   ├── tests.py            # Tests API
│   │   ├── urls.py
│   │   └── admin.py
│   ├── web/                    # Frontend Django
│   │   ├── views/              # Vues Web (8 modules)
│   │   ├── templates/          # Templates HTML (35 fichiers)
│   │   │   └── web/
│   │   │       ├── base.html
│   │   │       ├── home.html
│   │   │       ├── dashboard.html
│   │   │       ├── onboarding/
│   │   │       └── workout/
│   │   ├── static/             # CSS + JS
│   │   │   └── web/
│   │   │       ├── css/
│   │   │       │   ├── main.css
│   │   │       │   └── workout.css
│   │   │       └── js/
│   │   │           ├── agenda.js
│   │   │           ├── dashboard.js
│   │   │           ├── workout.js
│   │   │           └── ...
│   │   ├── tests/              # Tests Web (4 fichiers)
│   │   ├── forms.py
│   │   ├── middleware.py
│   │   └── urls.py
│   ├── config/                 # Configuration Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── locale/                 # Traductions i18n
│   │   ├── fr/
│   │   └── en/
│   ├── manage.py
│   ├── requirements.txt
│   ├── runtime.txt
│   └── build_files.sh
├── docs/                       # Documentation
│   ├── API.md
│   ├── DEPLOY.md
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   ├── deployment/
│   └── validation/
├── validation_scripts/         # Scripts de validation
├── archives/                   # Anciens rapports
├── .gitignore
├── render.yaml                 # Config Render
├── vercel.json                 # Config Vercel
├── LICENSE
└── README.md                   # Ce fichier
```

### Modèles de Données (14 modèles)

**User & Stats:**
- `User` (Custom) - Utilisateur avec bio, avatar
- `UserStats` (OneToOne) - XP, Level, Streaks, Scores

**Content:**
- `Category` - Catégories blog
- `Article` - Articles blog
- `Comment` - Commentaires

**Workout:**
- `Exercise` - Bibliothèque exercices (101)
- `WorkoutSession` - Sessions d'entraînement
- `ExerciseSet` - Sets individuels

**Nutrition:**
- `Recipe` - Recettes (39)

**Planning:**
- `WellnessPlan` - Plans IA générés
- `DailyLog` - Logs quotidiens
- `CustomEvent` - Événements agenda

**Gamification:**
- `Badge` - Badges (20)
- `UserBadge` - Badges débloqués

---

## 🔒 Sécurité

### Authentification
- **Sessions Django** pour Web
- **JWT Tokens** pour API
- **Password Hashing**: PBKDF2
- **CSRF Protection**: Activé

### Autorisation
- **Permissions API**: IsAuthenticated, IsAdminOrReadOnly, IsAuthorOrReadOnly
- **Décorateurs Web**: @login_required (25 vues)
- **Filtrage Queryset**: `filter(user=request.user)`

### Protection des Données
- Chaque utilisateur voit uniquement ses données
- Isolation complète: Plans, Workouts, Logs, Événements, Badges
- Commentaires modifiables par auteur uniquement
- Articles modifiables par admin uniquement

### Configuration Production
```python
DEBUG = False
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = ['yourdomain.com']
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📊 Statistiques du Projet

### Code
- **Fichiers Python**: 81+
- **Templates HTML**: 35
- **Fichiers CSS**: 2
- **Fichiers JavaScript**: 7
- **Lignes de code**: ~8000+
- **Migrations**: 11

### Base de Données
- **Modèles**: 14
- **Relations**: 15 (13 FK + 1 OneToOne + 1 M2M)
- **Seed Data**: 173 entrées

### Tests
- **Tests**: 30
- **Taux de réussite**: 100%
- **Couverture**: API, Views, Forms, Flows

### Documentation
- **Fichiers**: 16+
- **README**: Complet
- **API Docs**: Swagger
- **Guides**: Déploiement, Contribution, Sécurité

---

## 🤝 Contribution

### Guidelines

1. **Fork** le projet
2. **Créer** une branche (`git checkout -b feature/AmazingFeature`)
3. **Commit** vos changements (`git commit -m 'Add AmazingFeature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrir** une Pull Request

### Standards de Code

- **Python**: PEP 8
- **Django**: Best practices
- **Commits**: Messages clairs et descriptifs
- **Tests**: Ajouter des tests pour nouvelles fonctionnalités

### Développement Local

```bash
# Créer une branche
git checkout -b feature/ma-feature

# Faire vos modifications
# ...

# Tester
python manage.py test

# Vérifier
python manage.py check

# Commit
git add .
git commit -m "feat: ajouter ma feature"

# Push
git push origin feature/ma-feature
```

---

## 📝 License

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **Django** - Framework web Python
- **Django REST Framework** - API REST
- **TailwindCSS** - Framework CSS
- **Chart.js** - Graphiques
- **Unsplash** - Images
- **Lucide** - Icons

---

## 📞 Support

### Documentation
- **README**: Ce fichier
- **API Docs**: `/swagger/`
- **Guides**: `docs/`

### Liens
- **Repository**: https://github.com/Sy2force/Fitwell
- **Issues**: https://github.com/Sy2force/Fitwell/issues
- **Discussions**: https://github.com/Sy2force/Fitwell/discussions

### Contact
- **Email**: contact@fitwell.local
- **Website**: https://fitwell.onrender.com

---

## 🎯 Roadmap

### Version 1.0 (Actuelle) ✅
- [x] Authentification complète
- [x] AI Planner
- [x] Workout Tracking
- [x] Gamification (XP, Badges, Streaks)
- [x] Analytics
- [x] Blog & Communauté
- [x] Internationalisation (FR/EN)
- [x] Déploiement Render

### Version 1.1 (Prochaine)
- [ ] Application mobile (React Native)
- [ ] Intégration wearables (Fitbit, Apple Watch)
- [ ] Coach IA vocal avancé
- [ ] Programmes d'entraînement prédéfinis
- [ ] Marketplace de plans

### Version 2.0 (Future)
- [ ] Social features (amis, défis)
- [ ] Vidéos d'exercices
- [ ] Nutrition tracking avancé
- [ ] Intégration nutritionniste
- [ ] API publique

---

## 📈 Statut du Projet

| Aspect | Statut |
|--------|--------|
| **Développement** | ✅ Complet |
| **Tests** | ✅ 30/30 (100%) |
| **Documentation** | ✅ Complète |
| **Déploiement** | ✅ Production Ready |
| **Sécurité** | ✅ Validée |
| **Performance** | ✅ Optimisée |

---

**Développé avec ❤️ par l'équipe FitWell**

© 2026 FitWell Systems Inc. Tous droits réservés.

---

**⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile sur GitHub!**
