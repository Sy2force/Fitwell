#!/bin/bash

# FitWell Blog API - Script de démarrage rapide
# Ce script configure et lance l'application en mode développement

echo "🚀 Configuration de FitWell Blog API..."

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Copier le fichier .env.example si .env n'existe pas
if [ ! -f ".env" ]; then
    echo "📝 Création du fichier .env..."
    cp .env.example .env
    echo "⚠️  N'oubliez pas de configurer vos variables d'environnement dans .env"
fi

# Appliquer les migrations
echo "🗄️  Application des migrations..."
python manage.py migrate

# Créer un superutilisateur si demandé
read -p "Voulez-vous créer un superutilisateur ? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    python manage.py createsuperuser
fi

# Charger les fixtures (données de test)
read -p "Voulez-vous charger les données de test ? (o/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Oo]$ ]]; then
    echo "📊 Chargement des données de test..."
    python manage.py loaddata blog/fixtures/initial_data.json
    echo "⚠️  Note: Les mots de passe des utilisateurs de test doivent être réinitialisés"
fi

# Lancer le serveur
echo ""
echo "✅ Configuration Backend terminée !"
echo "🌐 Lancement du serveur Django..."
echo ""
echo "ℹ️  Pour lancer le Frontend React :"
echo "   Ouvrez un nouveau terminal et lancez :"
echo "   cd fitwell-frontend && npm install && npm run dev"
echo ""
echo "📚 Documentation API disponible sur:"
echo "   - Swagger UI: http://localhost:8000/api/docs/"
echo "   - Admin: http://localhost:8000/admin/"
echo ""
python manage.py runserver
