# 🔧 CORRECTION DATABASE_URL RENDER

## Problème Identifié

L'erreur `OperationalError: no such table: api_category` sur Render indique que:
- Render utilise **SQLite** au lieu de **PostgreSQL**
- La variable `DATABASE_URL` est mal configurée

## Solution

### Sur Render Dashboard:

1. **Aller dans Service "fitwell" → Environment**

2. **Vérifier DATABASE_URL**
   - Actuellement: `https://fitwell-monolith.onrender.com` ❌
   - Doit être: `postgresql://fitwell_user:password@dpg-xxxxx...` ✅

3. **Obtenir la bonne URL:**
   - Aller dans PostgreSQL Database (fitwell-db)
   - Section "Connections"
   - Copier "Internal Database URL"
   - Format: `postgresql://fitwell_user:password@dpg-xxxxx.frankfurt-postgres.render.com:5432/fitwell`

4. **Modifier DATABASE_URL:**
   - Retourner dans Web Service → Environment
   - Cliquer sur DATABASE_URL
   - Supprimer l'ancienne valeur
   - Coller l'Internal Database URL
   - Save Changes

5. **Render redéploiera automatiquement**
   - Build avec PostgreSQL
   - Migrations appliquées
   - Seeds exécutés
   - Interface fonctionnelle

## Vérification

Après correction, tester:
- https://fitwell-izy6.onrender.com/fr/blog/ (devrait fonctionner)
- https://fitwell-izy6.onrender.com/api/articles/ (devrait retourner des articles)

## URL Finale

**Projet:** https://fitwell-izy6.onrender.com/fr/

**Comptes:**
- Admin: admin / adminpassword
- Demo: demo / demopass123
