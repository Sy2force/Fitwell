#!/usr/bin/env bash
# ==============================================================================
# Script de build FitWell pour Render
# Exécuté avec rootDir=backend, donc le pwd est déjà /backend
# ==============================================================================
set -o errexit

echo "==> [1/5] Installation des dépendances..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "==> [2/5] Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

echo "==> [3/5] Compilation des traductions (si gettext disponible)..."
python manage.py compilemessages || echo "Info: compilemessages skipped (gettext absent)"

echo "==> [4/5] Migrations base de données..."
python manage.py migrate --noinput

echo "==> [5/5] Seeding (idempotent)..."
python manage.py seed_db || echo "Info: seed_db a échoué (peut-être déjà fait)"
python manage.py seed_badges || echo "Info: seed_badges a échoué"

echo "==> Build terminé avec succès."
