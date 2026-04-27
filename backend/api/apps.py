from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        # Brancher les signaux (tracking IP/UserAgent au login)
        from . import signals  # noqa: F401
