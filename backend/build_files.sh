#!/bin/bash
# ==============================================================================
# Script de Build FitWell (Optimisé pour Render)
# ==============================================================================
# Ce script peut être exécuté depuis la racine du repo ou depuis /backend.
# ==============================================================================
set -e

# Détection et bascule vers le dossier backend
if [ -d "backend" ]; then
    echo "==> Passage dans le répertoire backend..."
    cd backend
fi

echo "==> [1/6] Installation des dépendances..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "==> [2/6] Collecte des fichiers statiques..."
# Nécessaire avant tout pour WhiteNoise
python3 manage.py collectstatic --noinput --clear

echo "==> [3/6] Compilation des traductions (i18n)..."
python3 manage.py compilemessages || echo "Info: Aucune traduction à compiler ou gettext manquant."

echo "==> [4/6] Vérification des migrations en attente..."
python3 manage.py showmigrations

echo "==> [5/6] Application des migrations..."
python3 manage.py migrate --noinput

echo "==> [6/6] Peuplement de la base de données (Seeding)..."
# Les commandes de seed sont conçues pour être idempotentes (update_or_create)
python3 manage.py seed_db || echo "Attention: seed_db a rencontré un problème."
# Note: seed_db appelle déjà en interne seed_blog, seed_exercises et seed_recipes
# On s'assure que les badges sont là aussi
python3 manage.py seed_badges || echo "Attention: seed_badges a rencontré un problème."

echo "==> [SUCCÈS] Build terminé avec succès !"
