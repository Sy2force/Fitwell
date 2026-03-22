#!/usr/bin/env python3
"""
Script de vérification pré-déploiement pour FitWell
Vérifie que tous les composants sont prêts pour Render
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Vérifie qu'un fichier existe"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MANQUANT: {filepath}")
        return False

def check_command(command, description):
    """Exécute une commande et vérifie le résultat"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd='backend')
        if result.returncode == 0:
            print(f"✅ {description}")
            return True
        else:
            print(f"❌ {description} ÉCHOUÉ")
            print(f"   Erreur: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"❌ {description} ERREUR: {e}")
        return False

def main():
    print("=" * 60)
    print("🔍 VÉRIFICATION PRÉ-DÉPLOIEMENT RENDER - FITWELL")
    print("=" * 60)
    print()
    
    errors = []
    
    # 1. Fichiers de configuration
    print("📁 Vérification des fichiers de configuration...")
    if not check_file_exists("render.yaml", "Configuration Render"):
        errors.append("render.yaml manquant")
    if not check_file_exists("backend/build_files.sh", "Script de build"):
        errors.append("build_files.sh manquant")
    if not check_file_exists("backend/requirements.txt", "Dépendances Python"):
        errors.append("requirements.txt manquant")
    if not check_file_exists("backend/runtime.txt", "Version Python"):
        errors.append("runtime.txt manquant")
    if not check_file_exists("backend/config/wsgi.py", "WSGI"):
        errors.append("wsgi.py manquant")
    print()
    
    # 2. Permissions
    print("🔐 Vérification des permissions...")
    build_script = Path("backend/build_files.sh")
    if build_script.exists():
        is_executable = os.access(build_script, os.X_OK)
        if is_executable:
            print("✅ build_files.sh est exécutable")
        else:
            print("❌ build_files.sh n'est PAS exécutable")
            errors.append("build_files.sh permissions")
    print()
    
    # 3. Tests Django
    print("🧪 Exécution des tests Django...")
    if not check_command("python3 manage.py check", "Django system check"):
        errors.append("System check échoué")
    if not check_command("python3 manage.py test --verbosity=0", "Tests unitaires"):
        errors.append("Tests échoués")
    print()
    
    # 4. Migrations
    print("🗄️ Vérification des migrations...")
    if not check_command("python3 manage.py makemigrations --dry-run --check", "Migrations à jour"):
        print("⚠️  Des migrations sont en attente")
    print()
    
    # 5. Commandes de seed
    print("🌱 Vérification des commandes de seed...")
    seed_commands = ['seed_db', 'seed_exercises', 'seed_blog', 'seed_badges', 'seed_recipes']
    for cmd in seed_commands:
        cmd_file = Path(f"backend/api/management/commands/{cmd}.py")
        if cmd_file.exists():
            print(f"✅ Commande {cmd} existe")
        else:
            print(f"❌ Commande {cmd} MANQUANTE")
            errors.append(f"Commande {cmd} manquante")
    print()
    
    # 6. Fichiers statiques
    print("📦 Vérification des fichiers statiques...")
    if not check_command("python3 manage.py collectstatic --noinput --dry-run", "Collecte statiques"):
        errors.append("Collectstatic échoué")
    print()
    
    # 7. Dépendances
    print("📚 Vérification des dépendances...")
    required_packages = [
        'Django', 'djangorestframework', 'gunicorn', 'psycopg2-binary',
        'whitenoise', 'dj-database-url', 'python-decouple'
    ]
    with open('backend/requirements.txt', 'r') as f:
        requirements = f.read()
        for package in required_packages:
            if package.lower() in requirements.lower():
                print(f"✅ {package}")
            else:
                print(f"❌ {package} MANQUANT")
                errors.append(f"{package} manquant dans requirements.txt")
    print()
    
    # Résumé
    print("=" * 60)
    if errors:
        print(f"❌ ÉCHEC - {len(errors)} erreur(s) détectée(s):")
        for error in errors:
            print(f"   - {error}")
        print()
        print("⚠️  Corrigez les erreurs avant de déployer sur Render")
        sys.exit(1)
    else:
        print("✅ SUCCÈS - Tous les composants sont validés!")
        print()
        print("🚀 Le projet est prêt pour le déploiement sur Render")
        print()
        print("Prochaines étapes:")
        print("1. Aller sur https://render.com")
        print("2. New + → Blueprint")
        print("3. Connecter le repo Sy2force/Fitwell")
        print("4. Cliquer Apply")
        sys.exit(0)

if __name__ == '__main__':
    main()
