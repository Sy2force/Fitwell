from rest_framework_simplejwt.views import TokenObtainPairView
from api.serializers import EmailTokenObtainPairSerializer

class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Vue de login qui utilise l'email au lieu du username.
    """
    serializer_class = EmailTokenObtainPairSerializer
