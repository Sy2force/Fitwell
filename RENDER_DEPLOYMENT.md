# 🚀 Guide de Déploiement sur Render - FitWell

**Date**: 22 Mars 2026  
**Version**: 1.0.0  
**Durée estimée**: 10-15 minutes

---

## 📋 Prérequis

- ✅ Compte GitHub avec le repo FitWell
- ✅ Compte Render (gratuit) : https://render.com
- ✅ Le projet est déjà configuré et prêt

---

## 🎯 Architecture de Déploiement

```
┌─────────────────────────────────────────┐
│         Render Platform                 │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────────┐  ┌─────────────┐ │
│  │   Web Service    │  │  PostgreSQL │ │
│  │   (FitWell)      │──│  Database   │ │
│  │   Python 3.9     │  │  (Free)     │ │
│  │   Gunicorn       │  │             │ │
│  └──────────────────┘  └─────────────┘ │
│                                         │
└─────────────────────────────────────────┘
```

---

## 📝 ÉTAPE 1 : Connexion à Render

1. **Aller sur** https://render.com
2. **Cliquer** sur "Get Started" ou "Sign In"
3. **Se connecter** avec GitHub
4. **Autoriser** Render à accéder à tes repos

---

## 📝 ÉTAPE 2 : Déploiement Automatique via render.yaml

### Option A : Déploiement en 1 clic (Recommandé)

Le fichier `render.yaml` est déjà configuré dans le projet !

1. **Dans le Dashboard Render**, cliquer sur **"New +"**
2. Sélectionner **"Blueprint"**
3. **Connecter** ton repo GitHub `Sy2force/Fitwell`
4. Render va **détecter automatiquement** le fichier `render.yaml`
5. Cliquer sur **"Apply"**

✨ **C'est tout !** Render va automatiquement :
- ✅ Créer la base de données PostgreSQL
- ✅ Créer le service web
- ✅ Installer les dépendances
- ✅ Appliquer les migrations
- ✅ Peupler la base de données (101 exercices, 39 recettes, 20 badges, 5 articles)
- ✅ Collecter les fichiers statiques
- ✅ Démarrer l'application

### Option B : Déploiement Manuel

Si tu préfères configurer manuellement :

#### 2.1 Créer la Base de Données

1. **Dashboard Render** → **"New +"** → **"PostgreSQL"**
2. **Nom** : `fitwell-db`
3. **Database** : `fitwell`
4. **User** : `fitwell_user`
5. **Region** : `Frankfurt` (ou le plus proche)
6. **Plan** : `Free`
7. Cliquer sur **"Create Database"**
8. **Copier** l'URL de connexion (Internal Database URL)

#### 2.2 Créer le Web Service

1. **Dashboard Render** → **"New +"** → **"Web Service"**
2. **Connecter** ton repo `Sy2force/Fitwell`
3. **Configurer** :

| Paramètre | Valeur |
|-----------|--------|
| **Name** | `fitwell-monolith` |
| **Region** | `Frankfurt` |
| **Branch** | `main` |
| **Root Directory** | `.` (racine) |
| **Runtime** | `Python 3` |
| **Build Command** | Voir ci-dessous |
| **Start Command** | `cd backend && gunicorn config.wsgi:application` |

**Build Command** :
```bash
chmod +x backend/build_files.sh && ./backend/build_files.sh && cd backend && python manage.py seed_exercises && python manage.py seed_blog && python manage.py seed_badges && python manage.py seed_recipes
```

---

## 🔐 ÉTAPE 3 : Variables d'Environnement

### Variables Automatiques (render.yaml)

Si tu as utilisé l'Option A, ces variables sont déjà configurées :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `PYTHON_VERSION` | `3.9.0` | Version Python |
| `SECRET_KEY` | *Auto-généré* | Clé secrète Django |
| `DEBUG` | `False` | Mode production |
| `ALLOWED_HOSTS` | `*` | Hosts autorisés |
| `DATABASE_URL` | *Auto-lié* | URL PostgreSQL |

### Variables Manuelles (Option B)

Si tu as utilisé l'Option B, ajoute ces variables dans **Environment** :

1. **Dans ton Web Service** → **Environment**
2. **Ajouter** les variables suivantes :

```bash
PYTHON_VERSION=3.9.0
SECRET_KEY=<générer-une-clé-forte>
DEBUG=False
ALLOWED_HOSTS=*
DATABASE_URL=<url-de-ta-base-de-données>
```

**Générer une SECRET_KEY** :
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## ⏱️ ÉTAPE 4 : Attendre le Déploiement

Le déploiement prend environ **5-10 minutes**.

**Render va :**
1. ✅ Cloner le repo
2. ✅ Installer les dépendances Python
3. ✅ Appliquer les migrations
4. ✅ Peupler la base de données
5. ✅ Collecter les fichiers statiques
6. ✅ Démarrer Gunicorn

**Suivre les logs** :
- Dans ton service → **Logs**
- Tu verras les étapes en temps réel

---

## ✅ ÉTAPE 5 : Vérification

### 5.1 Accéder à l'Application

Ton URL sera : `https://fitwell-monolith.onrender.com`

### 5.2 Vérifier les Pages

| Page | URL | Statut Attendu |
|------|-----|----------------|
| **Home** | `/` | ✅ 200 OK |
| **API Articles** | `/api/articles/` | ✅ 200 OK |
| **Swagger** | `/swagger/` | ✅ 200 OK |
| **Admin** | `/admin/` | ✅ 200 OK |
| **Dashboard** | `/dashboard/` | ✅ 302 (redirect login) |

### 5.3 Créer un Super-Utilisateur

**Via le Shell Render** :

1. **Dans ton Web Service** → **Shell**
2. **Exécuter** :

```bash
cd backend
python manage.py createsuperuser
```

3. **Entrer** :
   - Username : `admin`
   - Email : `admin@fitwell.com`
   - Password : *ton-mot-de-passe-sécurisé*

### 5.4 Vérifier les Données

```bash
python manage.py shell -c "from api.models import Exercise, Article, Badge, Recipe; print(f'Exercices: {Exercise.objects.count()}'); print(f'Articles: {Article.objects.count()}'); print(f'Badges: {Badge.objects.count()}'); print(f'Recettes: {Recipe.objects.count()}')"
```

**Résultat attendu** :
```
Exercices: 101
Articles: 5
Badges: 20
Recettes: 39
```

---

## 🔧 ÉTAPE 6 : Configuration Post-Déploiement

### 6.1 Domaine Personnalisé (Optionnel)

1. **Dans ton Web Service** → **Settings** → **Custom Domain**
2. **Ajouter** ton domaine
3. **Configurer** les DNS selon les instructions

### 6.2 HTTPS

✅ **Automatique !** Render fournit un certificat SSL gratuit.

### 6.3 Variables Additionnelles (Optionnel)

**Email (pour reset password)** :
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=FitWell <noreply@fitwell.com>
```

---

## 📊 Monitoring et Maintenance

### Logs

**Accéder aux logs** :
- Dashboard → Ton service → **Logs**
- Logs en temps réel
- Filtrage par niveau (INFO, ERROR, etc.)

### Métriques

**Voir les métriques** :
- Dashboard → Ton service → **Metrics**
- CPU, Mémoire, Requêtes
- Temps de réponse

### Redéploiement

**Déploiement automatique** :
- Chaque push sur `main` déclenche un redéploiement
- Ou manuellement : **Manual Deploy** → **Deploy latest commit**

### Backup Base de Données

**Render Free Plan** :
- Pas de backup automatique
- Exporter manuellement via le Shell :

```bash
pg_dump $DATABASE_URL > backup.sql
```

---

## 🐛 Troubleshooting

### Erreur : "Application Error"

**Solution** :
1. Vérifier les logs : **Logs** tab
2. Vérifier que `DATABASE_URL` est défini
3. Vérifier que les migrations sont appliquées

### Erreur : "Static files not found"

**Solution** :
```bash
cd backend
python manage.py collectstatic --noinput
```

### Erreur : "CSRF verification failed"

**Solution** :
Ajouter dans les variables d'environnement :
```bash
CSRF_TRUSTED_ORIGINS=https://fitwell-monolith.onrender.com
```

### Base de Données Vide

**Solution** :
Relancer les seeds via le Shell :
```bash
cd backend
python manage.py seed_exercises
python manage.py seed_blog
python manage.py seed_badges
python manage.py seed_recipes
```

### Service Lent (Free Plan)

**Note** : Le plan gratuit Render met le service en veille après 15 min d'inactivité.
- Premier chargement peut prendre 30-60 secondes
- Considérer un plan payant pour production

---

## 💰 Plans Render

| Plan | Prix | Specs |
|------|------|-------|
| **Free** | $0/mois | 512 MB RAM, Veille après 15 min |
| **Starter** | $7/mois | 512 MB RAM, Toujours actif |
| **Standard** | $25/mois | 2 GB RAM, Auto-scaling |

---

## ✅ Checklist de Déploiement

- [ ] Compte Render créé
- [ ] Repo GitHub connecté
- [ ] Blueprint appliqué (render.yaml)
- [ ] Base de données créée
- [ ] Service web déployé
- [ ] Variables d'environnement configurées
- [ ] Migrations appliquées
- [ ] Données seedées
- [ ] Super-utilisateur créé
- [ ] Application accessible
- [ ] Tests de fonctionnalités OK

---

## 🎉 Félicitations !

Ton application FitWell est maintenant **déployée en production sur Render** !

**URL de production** : `https://fitwell-monolith.onrender.com`

### Prochaines Étapes

1. ✅ Tester toutes les fonctionnalités
2. ✅ Créer des utilisateurs de test
3. ✅ Configurer un domaine personnalisé (optionnel)
4. ✅ Mettre en place le monitoring
5. ✅ Partager avec tes utilisateurs !

---

## 📞 Support

**Documentation Render** : https://render.com/docs  
**Support Render** : https://render.com/support  
**Repo GitHub** : https://github.com/Sy2force/Fitwell

---

© 2026 FitWell Systems Inc.
