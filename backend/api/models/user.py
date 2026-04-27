from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------------------------------------------------------
# UTILISATEUR PERSONNALISÉ
# -----------------------------------------------------------------------------
class User(AbstractUser):
    """
    On étend l'utilisateur de base Django pour ajouter :
    - Profil : bio + avatar URL
    - Marketing / verification flags
    - Connection tracking : IP, user agent, login count (visibles dans le dashboard admin)
    - Soft delete : is_hidden (masquer sans supprimer)
    """
    bio = models.TextField(blank=True)
    avatar = models.CharField(max_length=500, blank=True, null=True)

    # Champs marketing / admin
    marketing_opt_in = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)

    # ----- Connection tracking (visible dans le dashboard admin custom) -----
    last_login_ip = models.GenericIPAddressField(blank=True, null=True, help_text="IP de la dernière connexion")
    last_user_agent = models.CharField(max_length=500, blank=True, default="", help_text="User-Agent de la dernière connexion")
    login_count = models.PositiveIntegerField(default=0, help_text="Nombre total de connexions")

    # ----- Soft delete (masquer sans supprimer) -----
    is_hidden = models.BooleanField(default=False, help_text="Masqué par l'admin (équivalent soft-delete)")

    def __str__(self):
        return self.username
