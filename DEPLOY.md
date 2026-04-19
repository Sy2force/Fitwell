# 🚀 Guide de Déploiement FitWell - Render

## Problème Actuel
FitWell est actuellement déployé sur **Vercel** (`fitwell-moche.vercel.app`) qui provoque une erreur 404 car Vercel est conçu pour les applications frontend (React, Next.js, etc.).

**FitWell est une application Django monolithique** qui doit être déployée sur **Render**.

## Solution : Migration vers Render

### 1. Prérequis
- Compte GitHub avec le repo FitWell
- Compte Render (gratuit) : https://render.com

### 2. Déploiement Automatique via Blueprint

#### Étape 1 : Push du fichier render.yaml
```bash
git add render.yaml
git commit -m "Add Render deployment configuration"
git push origin main
```

#### Étape 2 : Déployer sur Render
1. Aller sur https://dashboard.render.com
2. Cliquer **"New +"** → **"Blueprint"**
3. Connecter le repository GitHub : `Sy2force/Fitwell`
4. Branch : `main`
5. Cliquer **"Apply"**

#### Étape 3 : Attendre le Déploiement (5-10 minutes)
Render va automatiquement :
- Créer la base PostgreSQL (`fitwell-db`)
- Créer le service web (`fitwell-monolith`) 
- Exécuter `build_files.sh`
- Peupler la base avec les données de seed
- Démarrer l'application

### 3. URLs de Production

**Application :** `https://fitwell-monolith.onrender.com`

**Accès Admin :**
- URL : `https://fitwell-monolith.onrender.com/fr/admin/`
- Username : `admin`
- Password : `adminpassword`

### 4. Nettoyer Vercel

#### Supprimer le Projet Vercel
1. Aller sur https://vercel.com/dashboard
2. Sélectionner le projet `fitwell-moche`
3. Settings → Advanced → Delete Project

### 5. Variables d'Environnement (Auto-configurées)

Le fichier `render.yaml` configure automatiquement :
```env
SECRET_KEY=<généré automatiquement>
DEBUG=False
ALLOWED_HOSTS=*
LANGUAGE_CODE=fr-fr
TIME_ZONE=Europe/Paris
DATABASE_URL=<lié à PostgreSQL>
```

### 6. Vérification du Déploiement

Une fois déployé, vérifier :
- ✅ Page d'accueil : `/fr/`
- ✅ Login : `/fr/login/`
- ✅ Admin : `/fr/admin/`
- ✅ API : `/api/`
- ✅ Swagger : `/swagger/`

### 7. Avantages de Render vs Vercel

| Feature | Render | Vercel |
|---------|--------|--------|
| Django Support | ✅ Natif | ❌ Non supporté |
| PostgreSQL | ✅ Intégré | ❌ Externe requis |
| Build Scripts | ✅ Bash supporté | ❌ Limité |
| Static Files | ✅ WhiteNoise | ❌ Configuration complexe |
| Free Tier | ✅ 500h/mois | ❌ Fonction serverless seulement |

## Résolution de Problèmes

### Build Failed
```bash
# Vérifier localement
cd backend
./build_files.sh
python manage.py runserver
```

### Database Issues
Les commandes seed sont idempotentes. En cas d'erreur, Render va retry automatiquement.

### Logs de Déploiement
Dans Render Dashboard → Service → Logs pour voir les détails du build.

## Support
- **Repository :** https://github.com/Sy2force/Fitwell
- **Issues :** https://github.com/Sy2force/Fitwell/issues
- **Render Docs :** https://render.com/docs/django

---

**Note :** Une fois migré vers Render, l'URL `fitwell-moche.vercel.app` cessera de fonctionner. La nouvelle URL sera `fitwell-monolith.onrender.com`.
