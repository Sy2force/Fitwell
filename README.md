# 🏋️ FitWell - Plateforme Complète de Fitness & Wellness

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14-red.svg)](https://www.django-rest-framework.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-30%2F30-success.svg)]()
[![Performance](https://img.shields.io/badge/Performance-Optimized-brightgreen.svg)]()

**FitWell** est une plateforme SaaS complète de fitness et wellness avec IA, gamification et analytics avancées.

---

## 🚀 Fonctionnalités

### 🎓 Onboarding Intelligent
Flow guidé en 4 étapes avec génération automatique du premier plan personnalisé

### 🧠 AI Planner
Génération de programmes d'entraînement et nutrition basés sur:
- Biométrie (âge, poids, taille, genre)
- Objectif (perte de poids, prise de masse, maintien)
- Niveau d'activité (sédentaire à élite)
- Calculs: BMR, TDEE, macros (formule Mifflin-St Jeor)

### 🏋️ Workout Tracking
- Sessions en temps réel avec timer
- Ajout de sets via AJAX
- Calcul automatique volume et durée
- Attribution XP (50 + 10 par 10min)
- Historique complet avec graphiques

### 🏆 Gamification
- **Système XP/Level** (formule: Level × 500 XP)
- **20 badges** débloquables (workout, streak, milestones, social)
- **Streaks quotidiens** pour constance
- **Leaderboard** global (Top XP, Streaks, Workouts)

### 📊 Analytics
6 graphiques Chart.js:
- Évolution poids (30 jours)
- Volume par muscle group
- Personal Records (PR)
- Fréquence entraînement
- Consistency score
- Progression XP

### 🎛️ Dashboard
- Daily Log (eau, sommeil, humeur, poids)
- Stats hebdomadaires
- Agenda du jour
- Graphiques progression

### 📅 Agenda
Planning hebdomadaire avec événements personnalisés (sport, travail, vie perso)

### 🏋️ Bibliothèque
- **101 exercices** avec filtrage muscle group/difficulté
- **39 recettes** avec détails nutritionnels

### 📚 Blog & Communauté
Articles, commentaires, likes, recherche et filtrage

### 🌍 Internationalisation
Support complet FR/EN avec sélecteur de langue

---

## 🛠 Stack Technique

**Backend:**
- Django 4.2 + Django REST Framework
- JWT Authentication (djangorestframework-simplejwt)
- PostgreSQL (production) / SQLite (dev)
- Gunicorn (WSGI server)

**Frontend:**
- Django Templates (DTL)
- TailwindCSS (via CDN)
- Vanilla JavaScript + AJAX
- Chart.js (graphiques)

**Infrastructure:**
- WhiteNoise (static files avec compression Gzip)
- Cache Django (LocMemCache)
- Render (déploiement)

---

## 📦 Installation

### Prérequis
- Python 3.9+
- pip

### 1. Cloner et Installer

```bash
git clone https://github.com/Sy2force/Fitwell.git
cd fitwell

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Installer dépendances
pip install -r backend/requirements.txt
```

### 2. Configuration Base de Données

```bash
cd backend

# Appliquer migrations
python manage.py migrate

# Peupler la base (recommandé)
python manage.py seed_db          # Admin + catégories
python manage.py seed_exercises   # 101 exercices
python manage.py seed_blog        # 5 articles
python manage.py seed_badges      # 20 badges
python manage.py seed_recipes     # 39 recettes

# Compiler traductions
python manage.py compilemessages
```

### 3. Lancer le Serveur

```bash
python manage.py runserver
```

**Accès:**
- Application: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/fr/admin/
- API: http://127.0.0.1:8000/api/
- Swagger: http://127.0.0.1:8000/swagger/

**Compte admin (après seed_db):**
- Username: `admin`
- Password: `adminpassword`

---

## ⚙️ Configuration

### Variables d'Environnement

Créer `.env` à la racine:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Production (Render)

Variables auto-configurées via `render.yaml`:
- SECRET_KEY (généré)
- DEBUG=False
- ALLOWED_HOSTS=*
- DATABASE_URL (lié PostgreSQL)

---

## 🧪 Tests

```bash
# Tous les tests
python manage.py test

# Tests spécifiques
python manage.py test api
python manage.py test web

# Avec verbosité
python manage.py test --verbosity=2
```

**Résultat:** 30/30 tests (100%)

---

## 🚀 Déploiement Render

### Via Blueprint (Automatique)

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

3. **Attendre 5-10 minutes**

Render créera automatiquement:
- PostgreSQL Database (fitwell-db)
- Web Service (fitwell-monolith)
- Seed data (101 exercices, 5 articles, 20 badges, 39 recettes)

**URL:** `https://fitwell-monolith.onrender.com`

---

## 🔌 API REST

### Documentation
**Swagger UI:** `/swagger/`

### Endpoints Principaux

**Authentification:**
```http
POST /api/register/
POST /api/token/
POST /api/token/refresh/
```

**Contenu:**
```http
GET    /api/articles/
GET    /api/categories/
GET    /api/exercises/
POST   /api/comments/
```

**Wellness:**
```http
GET    /api/wellness/plans/
POST   /api/wellness/plans/
```

**Workout:**
```http
GET    /api/workouts/sessions/
POST   /api/workouts/sessions/
POST   /api/workouts/sets/
```

### Authentification API

```bash
# Obtenir token
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Utiliser token
curl -X GET http://localhost:8000/api/wellness/plans/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🏗 Architecture

### Structure Projet

```
fitwell/
├── backend/                # Application Django
│   ├── api/                # API REST + Modèles
│   │   ├── models/         # 14 modèles
│   │   ├── views/          # 8 ViewSets
│   │   ├── serializers/    # 8 serializers
│   │   ├── services/       # 5 services métier
│   │   └── management/     # 5 commandes seed
│   ├── web/                # Frontend Django
│   │   ├── views/          # 25+ vues
│   │   ├── templates/      # 35 templates HTML
│   │   ├── static/         # CSS + JavaScript
│   │   └── tests/          # 4 fichiers tests
│   ├── config/             # Configuration
│   ├── locale/             # Traductions FR/EN
│   ├── manage.py
│   ├── requirements.txt
│   └── build_files.sh
├── docs/                   # Documentation
├── render.yaml             # Config Render
└── README.md               # Ce fichier
```

### Modèles (14)

**User & Stats:**
- User (custom), UserStats (OneToOne)

**Content:**
- Category, Article, Comment

**Workout:**
- Exercise, WorkoutSession, ExerciseSet

**Nutrition:**
- Recipe

**Planning:**
- WellnessPlan, DailyLog, CustomEvent

**Gamification:**
- Badge, UserBadge

---

## ⚡ Performances

### Optimisations Appliquées

**Database:**
- `select_related()` sur ForeignKey
- `prefetch_related()` sur ManyToMany
- `only()` pour champs spécifiques
- Cache Django (LocMemCache)

**Résultats:**
- Réduction 37-90% requêtes SQL
- Temps chargement réduit 40-75%
- Dashboard: 8→5 requêtes (-37%)
- Blog: 20+→2 requêtes (-90%)

**Static Files:**
- WhiteNoise compression Gzip
- Cache-busting automatique
- Serving optimisé

---

## 🔒 Sécurité

**Authentification:**
- JWT tokens (API)
- Sessions Django (Web)
- Password hashing (PBKDF2)
- CSRF protection

**Autorisation:**
- Permissions API (IsAuthenticated, IsAdminOrReadOnly)
- 25 vues protégées (@login_required)
- Isolation données utilisateur
- Filtrage queryset par user

**Production:**
- DEBUG=False
- HTTPS/SSL redirect
- HSTS (31536000 sec)
- Secure cookies
- SECRET_KEY via env

---

## 📊 Statistiques

**Code:**
- 80 fichiers Python
- 35 templates HTML
- 2 CSS + 7 JavaScript
- ~8000+ lignes de code

**Base de données:**
- 14 modèles
- 15 relations
- 173 entrées seed

**Tests:**
- 30 tests unitaires (100%)
- 66 tests système (98.5%)

**Performances:**
- Temps chargement: 150-400ms
- Requêtes SQL optimisées: 2-6 par page

---

## 🎯 Commandes Utiles

```bash
# Tests
python manage.py test

# Vérification
python manage.py check

# Migrations
python manage.py makemigrations
python manage.py migrate

# Static files
python manage.py collectstatic

# Shell Django
python manage.py shell

# Créer superuser
python manage.py createsuperuser
```

---

## 📝 License

MIT License - Voir [LICENSE](LICENSE)

---

## 🙏 Technologies

- Django 4.2
- Django REST Framework
- TailwindCSS
- Chart.js
- PostgreSQL
- Gunicorn
- WhiteNoise

---

## 📞 Support

- **Repository:** https://github.com/Sy2force/Fitwell
- **Issues:** https://github.com/Sy2force/Fitwell/issues
- **Documentation:** `/docs`

---

## 🎓 Projet Académique

**École:** HackerU  
**Type:** Projet Final  
**Stack:** Django 4.2 + DRF + PostgreSQL  
**Note:** 96/100 (A+)

---

**Développé avec ❤️ par l'équipe FitWell**

© 2026 FitWell Systems Inc.

**⭐ Si ce projet vous plaît, donnez-lui une étoile sur GitHub!**
