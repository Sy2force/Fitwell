# Fix Render Deployment - Configuration Manuelle

Le déploiement échoue car Render détecte automatiquement Node.js au lieu de Python.

## Solution : Configuration Manuelle sur Render Dashboard

### Étape 1 : Supprimer le service actuel
1. Allez sur https://dashboard.render.com
2. Sélectionnez le service `fitwell-monolith`
3. Settings → Delete Web Service

### Étape 2 : Créer un nouveau service MANUELLEMENT
1. Cliquez sur "New +" → "Web Service"
2. Connectez votre repo GitHub `Sy2force/Fitwell`
3. **NE PAS** utiliser le fichier `render.yaml`
4. Configurez manuellement :

**Configuration de base :**
- **Name** : `fitwell-monolith`
- **Region** : Frankfurt
- **Branch** : `main`
- **Root Directory** : `backend`
- **Environment** : `Python 3`
- **Build Command** : `bash build_files.sh`
- **Start Command** : `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile -`

**Variables d'environnement :**
```
PYTHON_VERSION=3.9.18
DEBUG=False
ALLOWED_HOSTS=*
SECRET_KEY=[Auto-généré par Render]
DATABASE_URL=[Lien vers votre PostgreSQL]
```

### Étape 3 : Créer la base de données PostgreSQL
1. "New +" → "PostgreSQL"
2. **Name** : `fitwell-db`
3. **Database** : `fitwell`
4. **User** : `fitwell_user`
5. **Region** : Frankfurt
6. **Plan** : Free

### Étape 4 : Lier la base de données
1. Retournez sur le service web
2. Environment → Add Environment Variable
3. **Key** : `DATABASE_URL`
4. **Value** : Copiez l'URL "Internal Database URL" depuis la page PostgreSQL

### Étape 5 : Déployer
Cliquez sur "Manual Deploy" → "Deploy latest commit"

## Alternative : Blueprint (render.yaml)

Si vous voulez absolument utiliser `render.yaml`, il faut :
1. Supprimer TOUT fichier qui pourrait déclencher Node.js
2. S'assurer qu'il n'y a AUCUN `package.json` dans le repo
3. Utiliser "New +" → "Blueprint" au lieu de "Web Service"

## Vérification
Une fois déployé, testez :
```bash
curl https://fitwell-monolith.onrender.com/
```

Vous devriez voir la page d'accueil FitWell.
