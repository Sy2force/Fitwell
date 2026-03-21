from django.db import models
from django.contrib.auth.models import AbstractUser

# -----------------------------------------------------------------------------
# UTILISATEUR PERSONNALISÉ
# -----------------------------------------------------------------------------
class User(AbstractUser):
    """
    On étend l'utilisateur de base Django pour ajouter :
    - Une bio
    - Une photo de profil (avatar) -> URL pour ce prototype
    """
    bio = models.TextField(blank=True)
    avatar = models.CharField(max_length=500, blank=True, null=True) # Changed from ImageField to CharField for URL support
    
    # Champs marketing / admin
    marketing_opt_in = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_onboarded = models.BooleanField(default=False)

    def __str__(self):
        return self.username
