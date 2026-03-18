import os
import sys
from pathlib import Path

# Ajouter le dossier 'backend' au chemin Python
# Cela permet d'importer 'config.settings' comme si on était dans le dossier backend
current_path = Path(__file__).parent.resolve()
sys.path.append(str(current_path / "backend"))

# Définir le module de configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialiser l'application Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Vercel cherche souvent une variable nommée 'app'
app = application
