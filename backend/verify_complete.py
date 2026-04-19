#!/usr/bin/env python3
"""
Script d'analyse complète du projet FitWell
Vérifie que tout est créé sans erreur
"""
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.management import call_command
from django.apps import apps
from django.db import connection
from api.models import Exercise, Recipe, Badge, Article, User, UserStats, WellnessPlan

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(80)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*80}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ️  {text}{Colors.END}")

# Compteurs globaux
errors = []
warnings = []
successes = []

def check_django_apps():
    """Vérifie que toutes les apps Django sont installées"""
    print_header("VÉRIFICATION DES APPS DJANGO")
    
    required_apps = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'rest_framework',
        'corsheaders',
        'api',
        'web',
    ]
    
    installed_apps = [app.name for app in apps.get_app_configs()]
    
    for app in required_apps:
        if app in installed_apps:
            print_success(f"App '{app}' installée")
            successes.append(f"App {app}")
        else:
            print_error(f"App '{app}' MANQUANTE")
            errors.append(f"App {app} manquante")

def check_models():
    """Vérifie que tous les modèles sont correctement définis"""
    print_header("VÉRIFICATION DES MODÈLES")
    
    models_to_check = {
        'User': User,
        'UserStats': UserStats,
        'Exercise': Exercise,
        'Recipe': Recipe,
        'Badge': Badge,
        'Article': Article,
        'WellnessPlan': WellnessPlan,
    }
    
    for model_name, model_class in models_to_check.items():
        try:
            count = model_class.objects.count()
            print_success(f"Modèle '{model_name}': {count} objets")
            successes.append(f"Modèle {model_name}")
        except Exception as e:
            print_error(f"Modèle '{model_name}': ERREUR - {str(e)}")
            errors.append(f"Modèle {model_name}: {str(e)}")

def check_database():
    """Vérifie la connexion et l'état de la base de données"""
    print_header("VÉRIFICATION DE LA BASE DE DONNÉES")
    
    try:
        # Test de connexion
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print_success("Connexion à la base de données OK")
        successes.append("Connexion DB")
        
        # Vérifier les migrations
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
        
        if plan:
            print_warning(f"{len(plan)} migrations en attente")
            warnings.append(f"{len(plan)} migrations en attente")
        else:
            print_success("Toutes les migrations sont appliquées")
            successes.append("Migrations à jour")
            
    except Exception as e:
        print_error(f"Erreur base de données: {str(e)}")
        errors.append(f"DB: {str(e)}")

def check_templates():
    """Vérifie que tous les templates existent"""
    print_header("VÉRIFICATION DES TEMPLATES")
    
    template_dir = Path(__file__).parent / 'web' / 'templates' / 'web'
    
    if not template_dir.exists():
        print_error(f"Dossier templates non trouvé: {template_dir}")
        errors.append("Dossier templates manquant")
        return
    
    templates = list(template_dir.rglob('*.html'))
    print_success(f"{len(templates)} templates HTML trouvés")
    successes.append(f"{len(templates)} templates")
    
    # Vérifier les templates critiques
    critical_templates = [
        'base.html',
        'home.html',
        'login.html',
        'register.html',
        'dashboard.html',
        'profile.html',
    ]
    
    for template_name in critical_templates:
        template_path = template_dir / template_name
        if template_path.exists():
            print_success(f"Template critique '{template_name}' présent")
        else:
            print_error(f"Template critique '{template_name}' MANQUANT")
            errors.append(f"Template {template_name} manquant")

def check_views():
    """Vérifie que tous les modules de vues existent"""
    print_header("VÉRIFICATION DES VUES")
    
    views_dir = Path(__file__).parent / 'web' / 'views'
    
    if not views_dir.exists():
        print_error(f"Dossier views non trouvé: {views_dir}")
        errors.append("Dossier views manquant")
        return
    
    view_files = list(views_dir.glob('*.py'))
    print_success(f"{len(view_files)} modules de vues trouvés")
    successes.append(f"{len(view_files)} modules vues")
    
    # Vérifier les modules critiques
    critical_views = [
        'auth.py',
        'dashboard.py',
        'planner.py',
        'workout.py',
        'static.py',
    ]
    
    for view_name in critical_views:
        view_path = views_dir / view_name
        if view_path.exists():
            print_success(f"Module vue '{view_name}' présent")
        else:
            print_error(f"Module vue '{view_name}' MANQUANT")
            errors.append(f"Module vue {view_name} manquant")

def check_static_files():
    """Vérifie les fichiers statiques"""
    print_header("VÉRIFICATION DES FICHIERS STATIQUES")
    
    static_dir = Path(__file__).parent / 'web' / 'static' / 'web'
    
    if not static_dir.exists():
        print_warning(f"Dossier static non trouvé: {static_dir}")
        warnings.append("Dossier static manquant")
        return
    
    css_files = list(static_dir.rglob('*.css'))
    js_files = list(static_dir.rglob('*.js'))
    
    print_success(f"{len(css_files)} fichiers CSS trouvés")
    print_success(f"{len(js_files)} fichiers JS trouvés")
    successes.append(f"{len(css_files)} CSS + {len(js_files)} JS")

def check_data_integrity():
    """Vérifie l'intégrité des données"""
    print_header("VÉRIFICATION DE L'INTÉGRITÉ DES DONNÉES")
    
    # Exercices
    exercise_count = Exercise.objects.count()
    if exercise_count >= 100:
        print_success(f"Exercices: {exercise_count} (objectif: 100+)")
        successes.append(f"{exercise_count} exercices")
    else:
        print_warning(f"Exercices: {exercise_count} (objectif: 100+)")
        warnings.append(f"Seulement {exercise_count} exercices")
    
    # Recettes
    recipe_count = Recipe.objects.count()
    if recipe_count >= 35:
        print_success(f"Recettes: {recipe_count} (objectif: 35+)")
        successes.append(f"{recipe_count} recettes")
    else:
        print_warning(f"Recettes: {recipe_count} (objectif: 35+)")
        warnings.append(f"Seulement {recipe_count} recettes")
    
    # Badges
    badge_count = Badge.objects.count()
    if badge_count >= 20:
        print_success(f"Badges: {badge_count} (objectif: 20+)")
        successes.append(f"{badge_count} badges")
    else:
        print_warning(f"Badges: {badge_count} (objectif: 20+)")
        warnings.append(f"Seulement {badge_count} badges")
    
    # Articles
    article_count = Article.objects.count()
    if article_count >= 5:
        print_success(f"Articles: {article_count} (objectif: 5+)")
        successes.append(f"{article_count} articles")
    else:
        print_warning(f"Articles: {article_count} (objectif: 5+)")
        warnings.append(f"Seulement {article_count} articles")

def check_urls():
    """Vérifie que les URLs sont configurées"""
    print_header("VÉRIFICATION DES URLs")
    
    from django.urls import get_resolver
    
    try:
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        print_success(f"{len(url_patterns)} patterns d'URL racine configurés")
        successes.append(f"{len(url_patterns)} URL patterns")
    except Exception as e:
        print_error(f"Erreur URLs: {str(e)}")
        errors.append(f"URLs: {str(e)}")

def check_i18n():
    """Vérifie l'internationalisation"""
    print_header("VÉRIFICATION DE L'INTERNATIONALISATION")
    
    locale_dir = Path(__file__).parent / 'locale'
    
    if not locale_dir.exists():
        print_warning("Dossier locale non trouvé")
        warnings.append("i18n non configuré")
        return
    
    # Vérifier les langues
    languages = ['fr', 'en']
    for lang in languages:
        lang_dir = locale_dir / lang / 'LC_MESSAGES'
        mo_file = lang_dir / 'django.mo'
        
        if mo_file.exists():
            print_success(f"Messages compilés pour '{lang}'")
            successes.append(f"i18n {lang}")
        else:
            print_warning(f"Messages non compilés pour '{lang}'")
            warnings.append(f"i18n {lang} non compilé")

def check_configuration():
    """Vérifie la configuration Django"""
    print_header("VÉRIFICATION DE LA CONFIGURATION")
    
    from django.conf import settings
    
    # Vérifier les settings critiques
    critical_settings = [
        'SECRET_KEY',
        'INSTALLED_APPS',
        'MIDDLEWARE',
        'DATABASES',
        'STATIC_URL',
        'TEMPLATES',
    ]
    
    for setting_name in critical_settings:
        if hasattr(settings, setting_name):
            print_success(f"Setting '{setting_name}' configuré")
        else:
            print_error(f"Setting '{setting_name}' MANQUANT")
            errors.append(f"Setting {setting_name} manquant")

def run_system_check():
    """Exécute le system check de Django"""
    print_header("DJANGO SYSTEM CHECK")
    
    try:
        from io import StringIO
        from django.core.management import call_command
        
        output = StringIO()
        call_command('check', stdout=output)
        result = output.getvalue()
        
        if "no issues" in result.lower() or "0 silenced" in result:
            print_success("System check: 0 erreurs")
            successes.append("System check OK")
        else:
            print_warning(f"System check: {result}")
            warnings.append("System check avec avertissements")
            
    except Exception as e:
        print_error(f"Erreur system check: {str(e)}")
        errors.append(f"System check: {str(e)}")

def generate_report():
    """Génère le rapport final"""
    print_header("RAPPORT FINAL D'ANALYSE")
    
    total_checks = len(successes) + len(warnings) + len(errors)
    
    print(f"\n{Colors.BOLD}Résumé:{Colors.END}")
    print(f"  {Colors.GREEN}✅ Succès: {len(successes)}{Colors.END}")
    print(f"  {Colors.YELLOW}⚠️  Avertissements: {len(warnings)}{Colors.END}")
    print(f"  {Colors.RED}❌ Erreurs: {len(errors)}{Colors.END}")
    print(f"  {Colors.BOLD}Total: {total_checks} vérifications{Colors.END}")
    
    # Score de complétude
    if total_checks > 0:
        score = (len(successes) / total_checks) * 100
        print(f"\n{Colors.BOLD}Score de complétude: {score:.1f}%{Colors.END}")
        
        if score >= 90:
            print(f"{Colors.GREEN}{Colors.BOLD}🎉 EXCELLENT - Projet complet et opérationnel !{Colors.END}")
        elif score >= 75:
            print(f"{Colors.YELLOW}{Colors.BOLD}👍 BON - Quelques ajustements mineurs nécessaires{Colors.END}")
        else:
            print(f"{Colors.RED}{Colors.BOLD}⚠️  ATTENTION - Des corrections sont nécessaires{Colors.END}")
    
    # Détails des erreurs
    if errors:
        print(f"\n{Colors.RED}{Colors.BOLD}Erreurs détectées:{Colors.END}")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    
    # Détails des avertissements
    if warnings:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}Avertissements:{Colors.END}")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    
    print(f"\n{Colors.BOLD}{'='*80}{Colors.END}\n")
    
    return len(errors) == 0

def main():
    """Fonction principale"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                              ║")
    print("║                   ANALYSE COMPLÈTE DU PROJET FITWELL                         ║")
    print("║                                                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Exécuter toutes les vérifications
    check_django_apps()
    check_models()
    check_database()
    check_templates()
    check_views()
    check_static_files()
    check_data_integrity()
    check_urls()
    check_i18n()
    check_configuration()
    run_system_check()
    
    # Générer le rapport
    success = generate_report()
    
    # Code de sortie
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
