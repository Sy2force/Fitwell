from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Authentification via Username ou Email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        try:
            # On cherche par username OU email
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            # Si plusieurs users ont le même email (ne devrait pas arriver si unique),
            # on prend le premier pour éviter le crash, ou on refuse.
            # Ici on refuse par sécurité.
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
