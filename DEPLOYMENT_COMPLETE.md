# 🚀 Guide de Déploiement Complet - FitWell

**Version**: 1.0.0  
**Date**: 22 Mars 2026  
**Statut**: ✅ Production Ready

---

## 📋 Vue d'Ensemble

Ce guide couvre le déploiement de FitWell sur **3 plateformes** :

1. **Render** (Recommandé) - Déploiement complet avec PostgreSQL
2. **Vercel** - Déploiement serverless
3. **GitHub Actions** - CI/CD automatique

---

## 🎯 Option 1: Déploiement sur Render (Recommandé)

### Pourquoi Render ?

- ✅ PostgreSQL inclus (gratuit)
- ✅ Déploiement automatique via `render.yaml`
- ✅ Seed automatique de la base de données
- ✅ Logs en temps réel
- ✅ Shell pour administration

### Étapes de Déploiement

#### 1. Connexion à Render

1. Aller sur https://render.com
2. Se connecter avec GitHub
3. Autoriser l'accès au repo

#### 2. Déploiement Blueprint (1 clic)

1. Dashboard → **"New +"** → **"Blueprint"**
2. Sélectionner le repo **`Sy2force/Fitwell`**
3. Render détecte automatiquement `render.yaml`
4. Cliquer sur **"Apply"**

#### 3. Configuration Automatique

Le fichier `render.yaml` configure automatiquement :

```yaml
✅ Web Service: fitwell-monolith
✅ PostgreSQL Database: fitwell-db
✅ Python 3.9.18
✅ Variables d'environnement
✅ Build automatique
✅ Seed de la base de données
```

#### 4. Processus de Build (8-12 minutes)

Render va exécuter :

```bash
==> Installing dependencies...
    - pip install -r backend/requirements.txt
==> Applying migrations...
    - 11 migrations appliquées
==> Collecting static files...
    - 793 fichiers collectés
==> Compiling translations...
    - Traductions FR/EN compilées
==> Seeding database...
    - seed_db: Admin + catégories
    - seed_exercises: 101 exercices
    - seed_blog: 5 articles
    - seed_badges: 20 badges
    - seed_recipes: 39 recettes
==> Starting Gunicorn...
    - 2 workers, timeout 120s
```

#### 5. Post-Déploiement

**Créer un super-utilisateur** (via Shell Render) :

```bash
cd backend
python manage.py createsuperuser
```

**URL de production** : `https://fitwell-monolith.onrender.com`

---

## 🌐 Option 2: Déploiement sur Vercel

### Configuration

Le projet est configuré via `vercel.json` et `index.py`.

### Étapes

1. **Installer Vercel CLI** :
   ```bash
   npm install -g vercel
   ```

2. **Se connecter** :
   ```bash
   vercel login
   ```

3. **Déployer** :
   ```bash
   vercel --prod
   ```

### Variables d'Environnement Vercel

Ajouter dans le Dashboard Vercel :

```bash
SECRET_KEY=<générer-une-clé-forte>
DEBUG=False
DATABASE_URL=<url-postgresql-externe>
ALLOWED_HOSTS=.vercel.app
```

**Note** : Vercel nécessite une base de données externe (Render PostgreSQL, Neon, Supabase, etc.)

---

## 🔄 Option 3: GitHub Actions (CI/CD)

### Configuration Automatique

Le workflow `.github/workflows/django.yml` s'exécute automatiquement sur chaque push.

### Ce qui est testé

```yaml
✅ Installation des dépendances
✅ Exécution des 30 tests
✅ Vérification du code
```

### Voir les Résultats

1. GitHub → Onglet **"Actions"**
2. Voir les builds en temps réel
3. Badge de statut disponible

---

## 📊 Comparaison des Plateformes

| Fonctionnalité | Render | Vercel | GitHub Actions |
|----------------|--------|--------|----------------|
| **Hébergement** | ✅ Complet | ✅ Serverless | ❌ Tests uniquement |
| **Base de données** | ✅ PostgreSQL inclus | ❌ Externe requise | ❌ N/A |
| **Seed automatique** | ✅ Oui | ❌ Manuel | ❌ N/A |
| **Coût** | Gratuit | Gratuit | Gratuit |
| **Temps de build** | 8-12 min | 5-8 min | 2-3 min |
| **Shell d'admin** | ✅ Oui | ❌ Non | ❌ N/A |
| **Logs** | ✅ Temps réel | ✅ Temps réel | ✅ Temps réel |

---

## ✅ Fichiers de Configuration

### Pour Render

| Fichier | Description |
|---------|-------------|
| `render.yaml` | Configuration Blueprint complète |
| `backend/build_files.sh` | Script de build |
| `.python-version` | Version Python (3.9.18) |
| `.renderignore` | Fichiers à exclure du build |
| `Procfile` | Alternative de démarrage |

### Pour Vercel

| Fichier | Description |
|---------|-------------|
| `vercel.json` | Configuration Vercel |
| `index.py` | Point d'entrée WSGI |
| `backend/vercel_build.sh` | Script de build Vercel |
| `.vercelignore` | Fichiers à exclure |

### Pour GitHub Actions

| Fichier | Description |
|---------|-------------|
| `.github/workflows/django.yml` | Workflow CI/CD |

---

## 🔒 Variables d'Environnement

### Variables Requises (Toutes Plateformes)

```bash
SECRET_KEY=<clé-secrète-django>
DEBUG=False
DATABASE_URL=<url-postgresql>
ALLOWED_HOSTS=<domaines-autorisés>
```

### Générer une SECRET_KEY

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 🧪 Validation Pré-Déploiement

### Script de Vérification

```bash
python3 backend/verify_deploy.py
```

**Vérifie** :
- ✅ Tous les fichiers de configuration
- ✅ Permissions exécutables
- ✅ Tests Django (30/30)
- ✅ Migrations
- ✅ Commandes de seed
- ✅ Dépendances

### Tests Manuels

```bash
# System check
python3 backend/manage.py check

# Tests
python3 backend/manage.py test

# Migrations
python3 backend/manage.py makemigrations --dry-run

# Collectstatic
python3 backend/manage.py collectstatic --noinput --dry-run
```

---

## 🚨 Troubleshooting

### Render: "npm install failed"

**Cause** : Détection automatique de Node.js  
**Solution** : Fichiers `package.json` supprimés ✅

### Render: "Build failed"

**Solutions** :
1. Vérifier les logs dans l'onglet "Logs"
2. Vérifier que `DATABASE_URL` est configuré
3. Clear build cache et redéployer

### Vercel: "Application Error"

**Solutions** :
1. Vérifier que `DATABASE_URL` est défini
2. Vérifier que `SECRET_KEY` est défini
3. Vérifier les logs Vercel

### GitHub Actions: Tests échouent

**Solutions** :
1. Vérifier que tous les tests passent localement
2. Vérifier les dépendances dans `requirements.txt`
3. Voir les logs détaillés dans Actions

---

## 📈 Monitoring Post-Déploiement

### Render

- **Logs** : Dashboard → Service → Logs
- **Métriques** : Dashboard → Service → Metrics
- **Shell** : Dashboard → Service → Shell

### Vercel

- **Logs** : Dashboard → Project → Deployments → Logs
- **Analytics** : Dashboard → Project → Analytics

### GitHub Actions

- **Builds** : Repository → Actions
- **Status Badge** : Ajouter au README

---

## 🎯 Recommandation

**Pour la production, utilisez Render** :
- ✅ Configuration la plus simple
- ✅ PostgreSQL inclus
- ✅ Seed automatique
- ✅ Shell pour administration
- ✅ Logs détaillés

---

## ✅ Checklist Finale

- [x] `render.yaml` configuré et testé
- [x] `vercel.json` configuré
- [x] GitHub Actions fonctionnel
- [x] Tous les tests passent (30/30)
- [x] Migrations à jour
- [x] Fichiers statiques collectés
- [x] Documentation complète
- [x] Scripts de vérification créés

---

**Le projet FitWell est 100% prêt pour le déploiement sur toutes les plateformes !** 🚀

© 2026 FitWell Systems Inc.
