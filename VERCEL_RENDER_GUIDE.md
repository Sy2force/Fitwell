# 🚀 GUIDE : CONNECTER VERCEL (APP) + RENDER (DB)

Ce guide explique comment héberger ton application Django sur **Vercel** tout en utilisant une base de données PostgreSQL hébergée sur **Render**.

---

## 🏗️ ARCHITECTURE

- **Vercel** : Héberge le code Django (le site web). C'est le "Moteur".
- **Render** : Héberge la base de données PostgreSQL. C'est la "Mémoire".

---

## 1️⃣ ÉTAPE 1 : RENDER (BASE DE DONNÉES)

1. Connecte-toi sur [Render Dashboard](https://dashboard.render.com/).
2. Clique sur **New +** -> **PostgreSQL**.
3. Nomme-le (ex: `fitwell-db`).
4. Choisis le plan (Free).
5. Une fois créé, cherche la section **Connections**.
6. Copie l'URL étiquetée **External Database URL**.
   - Elle ressemble à : `postgres://user:password@hostname.render.com/dbname`

> ⚠️ **IMPORTANT** : Assure-toi que ton IP n'est pas bloquée si Render a des restrictions d'accès, mais généralement l'URL externe est accessible publiquement (protégée par mot de passe).

---

## 2️⃣ ÉTAPE 2 : VERCEL (APPLICATION)

1. Connecte-toi sur [Vercel Dashboard](https://vercel.com/dashboard).
2. Clique sur **Add New...** -> **Project**.
3. Importe ton dépôt GitHub `Fitwell`.
4. Dans **Build & Development Settings**, Vercel détectera automatiquement la configuration grâce au fichier `vercel.json` que j'ai ajouté.
5. Ouvre la section **Environment Variables** et ajoute :

| Nom | Valeur |
|-----|--------|
| `DATABASE_URL` | L'URL copiée depuis Render (Step 1) |
| `SECRET_KEY` | Une longue chaîne aléatoire (ex: `django-insecure-...`) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.vercel.app` |

6. Clique sur **Deploy**.

---

## 3️⃣ ÉTAPE 3 : FINALISATION

Une fois déployé :
1. Vercel va installer les dépendances et construire le projet via `backend/build_files.sh`.
2. Ton site sera accessible sur une URL type `https://fitwell.vercel.app`.

### Commandes Utiles (Post-Déploiement)
Comme Vercel est "Serverless", tu ne peux pas facilement accéder à un shell. Pour gérer la base de données (créer un superuser), il est plus simple de le faire **depuis ton ordinateur** en te connectant à la base de données Render à distance :

```bash
# Sur ton PC, configure l'URL de la DB Render
export DATABASE_URL="postgres://..."

# Lance les commandes
python manage.py migrate
python manage.py createsuperuser
```

---

## ℹ️ NOTES IMPORTANTES

- **Fichiers Media** : Vercel ne stocke pas les fichiers uploadés par les utilisateurs (images de profil, etc.) de manière permanente. Pour un vrai site de production, il faudrait configurer **AWS S3** ou **Cloudinary** pour les fichiers media.
- **Limites Vercel** : Les fonctions serverless ont une limite de temps d'exécution (10s sur le plan gratuit). Les traitements longs (comme l'IA générative lourde) pourraient nécessiter d'être optimisés ou déportés.
