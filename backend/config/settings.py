import os
from pathlib import Path
from decouple import config
from datetime import timedelta
import dj_database_url

# -----------------------------------------------------------------------------
# CONFIGURATION DE BASE
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Clé secrète (à garder secrète en production !)
SECRET_KEY = config('SECRET_KEY', default='django-insecure-core-setup')

# Mode Debug : True pour le dév, False pour la prod
DEBUG = config('DEBUG', default=True, cast=bool)

# Qui a le droit d'accéder au site ?
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*,.vercel.app,.now.sh,127.0.0.1,localhost').split(',')

# CSRF Configuration - Ports dynamiques du browser preview
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

# En développement, ajouter les ports du proxy (64800-65000)
if DEBUG:
    for port in range(64800, 65000):
        CSRF_TRUSTED_ORIGINS.append(f'http://127.0.0.1:{port}')
        CSRF_TRUSTED_ORIGINS.append(f'http://localhost:{port}')

# CORS Configuration (pour les requêtes cross-origin)
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Permissif en dev, strict en prod

# -----------------------------------------------------------------------------
# APPLICATIONS INSTALLÉES
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Outils tiers
    'rest_framework',           # Pour créer l'API
    'rest_framework_simplejwt', # Pour l'authentification sécurisée
    'corsheaders',              # Pour autoriser le Frontend à nous parler
    'django_filters',           # Pour filtrer les résultats
    'drf_yasg',                 # Pour la documentation Swagger
    'whitenoise',               # Pour gérer les fichiers statiques

    # Notre application
    'api',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'web.middleware.OnboardingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# -----------------------------------------------------------------------------
# BASE DE DONNÉES
# -----------------------------------------------------------------------------
# Utilise SQLite en local, ou PostgreSQL si DATABASE_URL est défini (ex: sur Render)
DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        cast=dj_database_url.parse
    )
}

# -----------------------------------------------------------------------------
# MOTS DE PASSE & SÉCURITÉ
# -----------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'api.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ('fr', _('Français')),
    ('en', _('English')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]


# -----------------------------------------------------------------------------
# FICHIERS STATIQUES & MÉDIAS
# -----------------------------------------------------------------------------
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'api.User'

# -----------------------------------------------------------------------------
# REDIRECTIONS & URLs
# -----------------------------------------------------------------------------
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# -----------------------------------------------------------------------------
# CONFIGURATION REST FRAMEWORK (API)
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
}

# -----------------------------------------------------------------------------
# CONFIGURATION JWT (Tokens)
# -----------------------------------------------------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60), # Le token dure 1h
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Le refresh dure 24h
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# -----------------------------------------------------------------------------
# CONFIGURATION CORS (Qui peut nous parler ?)
# -----------------------------------------------------------------------------
# En mode monolithique, CORS est moins critique sauf si on ouvre l'API à des apps mobiles
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,http://127.0.0.1:54069').split(',')

# CSRF Protection
# Important pour que les formulaires Django marchent derrière un proxy https (Render)
CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,http://127.0.0.1:54069').split(',')

# Support automatique pour Render
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
    CSRF_TRUSTED_ORIGINS.append(f'https://{RENDER_EXTERNAL_HOSTNAME}')



# -----------------------------------------------------------------------------
# EMAIL CONFIGURATION
# -----------------------------------------------------------------------------
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # En production, utiliser un vrai service (SendGrid, Mailgun, etc.)
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.sendgrid.net')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = 'FitWell <noreply@fitwell.local>'

# -----------------------------------------------------------------------------
# SÉCURITÉ EN PRODUCTION
# -----------------------------------------------------------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 an
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True


