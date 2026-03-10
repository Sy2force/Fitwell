from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Gestionnaire d'erreur 404 personnalisé
handler404 = 'web.views.custom_404'
handler500 = 'web.views.custom_500'

# -----------------------------------------------------------------------------
# DOCUMENTATION API (Swagger)
# -----------------------------------------------------------------------------
schema_view = get_schema_view(
   openapi.Info(
      title="FitWell API",
      default_version='v1',
      description="Documentation technique de l'API FitWell",
      contact=openapi.Contact(email="contact@fitwell.local"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# -----------------------------------------------------------------------------
# ROUTES PRINCIPALES
# -----------------------------------------------------------------------------
urlpatterns = [
    # Documentation interactive (très utile pour tester) - Hors i18n pour l'instant ou inclus, au choix.
    # On le laisse accessible sans préfixe ou on le met dedans. 
    # Généralement API docs sont en anglais, mais on peut les laisser globales.
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Route pour changer de langue (set_language)
    path('i18n/', include('django.conf.urls.i18n')),

    # API (Hors i18n_patterns pour éviter les préfixes /fr/api/ ou /en/api/)
    path('api/', include('api.urls')),
]

urlpatterns += i18n_patterns(
    # Panneau d'administration Django
    path('admin/', admin.site.urls),

    # Frontend Django
    path('', include('web.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# On sert les fichiers médias (images) automatiquement en mode développement
