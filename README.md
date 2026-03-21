# FitWell - Système d'Optimisation de Performance Humaine

FitWell est une plateforme SaaS complète dédiée à la santé, au fitness et à l'optimisation biologique (Bio-Hacking). Elle combine un planificateur intelligent (IA), des outils de suivi métabolique et une base de connaissances communautaire.

## 🚀 Fonctionnalités Clés

### 1. 🎓 Onboarding Intelligent (NOUVEAU)
- Flow guidé en 4 étapes pour nouveaux utilisateurs
- Sélection objectif (Perte poids / Prise masse / Maintien)
- Configuration niveau d'activité (Sédentaire → Élite)
- Collecte données biométriques (Age, Genre, Taille, Poids)
- Génération automatique du premier plan
- Attribution badges de bienvenue
- Middleware de redirection automatique

### 2. 🏆 Badges & Achievements (NOUVEAU)
- 20 badges débloquables dans 4 catégories :
  - **Workout** : Première Séance, Guerrier (10), Spartiate (25), Titan (50), Légende (100)
  - **Volume** : Force Montante (1000kg), Powerlifter (5000kg), Hercule (10000kg)
  - **Streak** : Démarrage (3j), Constance (7j), Discipline de Fer (14j), Implacable (30j), Invincible (100j)
  - **Milestones** : Bienvenue, Planificateur, Niveau 10/25/50
  - **Social** : Contributeur, Engagé
- Attribution automatique après chaque action
- Récompenses XP (50-5000 XP)
- Affichage sur profil avec animations

### 3. 📊 Analytics Avancées (NOUVEAU)
- Page dédiée `/analytics/` avec :
  - Évolution du poids (30 derniers jours)
  - Volume par groupe musculaire (répartition complète)
  - Personal Records (PR) - Top 10 exercices
  - Fréquence d'entraînement (7 derniers jours)
  - Consistency Score (pourcentage sur 30 jours)
  - Progression XP (graphique temporel)
- 6 graphiques interactifs Chart.js

### 4. 🏆 Leaderboard Global (NOUVEAU)
- Classement des meilleurs athlètes FitWell
- 3 catégories : Top XP, Top Streaks, Top Workouts
- Position personnelle dans chaque classement
- Top 10 pour chaque catégorie

### 5. 🏋️ Workout Tracking Complet (NOUVEAU)
- Démarrer séance avec timer en temps réel
- Ajouter sets (exercice, reps, poids, repos) en Ajax
- Rest timer avec notification sonore
- Calcul automatique volume total et durée
- Attribution XP automatique (50 base + 10 par 10min)
- Historique complet avec graphiques
- Détails par séance avec breakdown exercices
- Statistiques globales

### 6. 🧠 Planificateur IA ("Protocoles")
- Génération de programmes d'entraînement et de nutrition sur mesure basés sur :
  - Biométrie (Âge, Poids, Taille, Genre)
  - Objectif (Perte de gras, Prise de masse, Maintien)
  - Niveau d'activité
- Calcul automatique des macros (Protéines, Glucides, Lipides) et calories.
- Analyse de santé avec scoring (0-100) et répartition (Fitness, Récupération, Lifestyle).
- Historique complet des anciens plans ("Archives").

### 2. 👤 Système Utilisateur Avancé
- **Gamification** : Système de Niveaux (LVL), Points d'Expérience (XP) et Séries (Streaks) pour encourager la constance.
- **Profil Opérateur** : Bio personnalisable, Avatar (URL), et statistiques visibles.
- **Sécurité** : Gestion complète (Inscription, Connexion, Édition Profil, Changement Mot de Passe, Récupération par Email).

### 3. ⚡️ Outils "Intel"
- **Calculateur IMC** : Évaluation de la composition corporelle.
- **Profil Métabolique** : Estimation du BMR et TDEE (Dépense Énergétique Journalière).

### 4. 🎛️ Centre de Commandement (Dashboard)
- **Suivi Quotidien (Daily Log)** : Enregistrez vos métriques vitales (Eau, Sommeil, Humeur, Poids).
- **Gamification** : Gagnez de l'XP à chaque mise à jour du journal (+20 XP).
- **Vue d'ensemble** : Statistiques hebdomadaires et agenda du jour en un coup d'œil.

### 5. 📅 Agenda Tactique
- **Planification Hebdomadaire** : Organisez vos blocs Sport, Travail et Vie Perso.
- **Gestion des Tâches** : Priorisez vos activités (Haute/Moyenne/Faible).
- **Récompenses** : Cochez vos tâches pour gagner de l'XP et monter de niveau.

### 6. 🏋️ Bibliothèque Tactique
- **Base de Données** : Catalogue complet d'exercices classés par groupe musculaire.
- **Fiches Techniques** : Instructions, difficulté et équipement requis pour chaque mouvement.

### 7. 🥗 Laboratoire Nutrition
- **Recettes Performance** : Bibliothèque de repas optimisés (Petit-déj, Déjeuner, Dîner, Shakes).
- **Profil Macro** : Détail précis des protéines, glucides et lipides pour chaque recette.
- **Filtrage Intelligent** : Tri par catégorie et niveau de difficulté.

### 8. ⏱️ Outils Tactiques
- **Chronomètre** : Mesure précise pour vos temps de repos ou circuits.
- **Minuteur** : Compte à rebours pour la gestion du temps d'effort (Tabata, EMOM).

### 9. 🤖 Coach Tactique IA
- **Mode J.A.R.V.I.S.** : Assistant vocal interactif pour guider vos séances.
- **HUD Immersif** : Interface futuriste temps réel avec compte à rebours et suivi de séquence.
- **Guidage Vocal** : Synthèse vocale (TTS) pour annoncer les exercices, temps de repos et encouragements.

### 10. 📚 Blog & Communauté
- Articles éducatifs sur la nutrition, l'entraînement et le bio-hacking.
- Système de Likes et Commentaires pour l'interaction.
- Filtrage par catégories et recherche textuelle.

### 8. 🌍 Internationalisation
- **Support Bilingue** : Français (défaut) et Anglais.
- **Interface Adaptative** : Traduction intégrale (Menus, Formulaires, Plans IA).
- **Accessible** : Sélecteur de langue optimisé pour Desktop et Mobile.

---

## 🛠 Installation & Démarrage

### Pré-requis
- Python 3.9+
- pip

### 1. Configuration de l'environnement
```bash
# Cloner le projet (si applicable)
# git clone ...

# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r backend/requirements.txt
```

### 📂 Structure du Projet

```
fitwell/
├── backend/               # Application Django Monolithe
│   ├── api/               # Modèles, Logique Métier, API REST
│   │   ├── models/        # Modèles organisés par domaine
│   │   ├── services/      # Logique métier
│   │   ├── views/         # Vues API REST
│   │   └── management/    # Commandes Django (seed_*)
│   ├── web/               # Vues & Templates (Frontend)
│   │   ├── views/         # Vues organisées par domaine
│   │   └── templates/     # Templates HTML
│   ├── config/            # Settings & URLs
│   ├── static/            # CSS, JS, Images
│   └── manage.py          # CLI Django
├── docs/                  # Documentation
│   ├── DEPLOY.md          # Guide de déploiement
│   ├── CONTRIBUTING.md    # Guide de contribution
│   └── SECURITY.md        # Politique de sécurité
├── tests/                 # Tests E2E Playwright
├── vercel.json            # Config déploiement Vercel
├── render.yaml            # Config déploiement Render
└── README.md              # Documentation principale
```

### 2. Base de Données
```bash
# Appliquer les migrations
python3 backend/manage.py migrate

# Peupler la base de données avec du contenu complet
python3 backend/manage.py seed_db          # Admin + catégories de base
python3 backend/manage.py seed_exercises   # 101 exercices avec images
python3 backend/manage.py seed_blog        # 25 articles professionnels
python3 backend/manage.py seed_badges      # 20 badges débloquables
python3 backend/manage.py seed_recipes     # Recettes nutritionnelles
```
> **Note**: Le script `seed_db` crée un super-utilisateur : `admin` / `adminpassword`.

### 3. Lancer le Serveur
```bash
python3 backend/manage.py runserver
```
Accédez à l'application sur `http://127.0.0.1:8000`.

### 4. Tests
Une suite de tests complète (30 tests) couvre l'API, les Vues et la Logique Métier.
```bash
python3 backend/manage.py test api web
```
Tous les tests passent avec succès (30/30) ✅

---

## 📚 Documentation API

L'API REST est entièrement documentée via Swagger/OpenAPI.
Accès : `http://127.0.0.1:8000/swagger/`

### Endpoints Principaux
- **Auth** : `/api/token/`, `/api/register/`
- **Blog** : `/api/articles/`, `/api/comments/`, `/api/categories/`
- **Utilisateurs** : `/api/users/`

### Permissions
- **Lecture** : Ouvert à tous (Articles), Authentifié (Profils).
- **Écriture (Articles)** : **Administrateurs uniquement**.
- **Commentaires** : Authentifié.

---

## 🏗 Architecture Technique

- **Architecture** : Monolithe Django (Python 3.9+).
- **Backend** : Django 4.2 + Django REST Framework.
- **Frontend** : Django Templates (DTL) + TailwindCSS (via CDN).
- **Design** : Thème "Dark Mode" / Glassmorphism futuriste.
- **Base de Données** : SQLite (Dev) / PostgreSQL (Prod ready via `dj-database-url`).
- **Sécurité** : CSRF Protection, Hashage des mots de passe (PBKDF2), Validateurs Django.

---

## 🔒 Comptes de Démonstration

Si vous avez lancé `seed_db` :
- **Admin** : `admin` / `adminpassword`

---

© 2026 FitWell Systems Inc.
