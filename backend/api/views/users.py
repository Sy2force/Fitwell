import csv
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from api.models import User
from api.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les utilisateurs.
    Permet de voir la liste, chercher par nom/email.
    L'inscription (register) est ouverte à tous.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_permissions(self):
        # N'importe qui peut s'inscrire, pas besoin d'être connecté.
        if self.action == 'register':
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['post'])
    def register(self, request):
        # Action personnalisée pour créer un compte facilement
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Endpoint pour récupérer ou mettre à jour son propre profil.
        URL: /api/users/me/
        """
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAdminUser])
    def export(self, request):
        """
        Export des utilisateurs en CSV (Admin seulement).
        URL: /api/users/export/
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="users_export.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Nom d\'utilisateur', 'Email', 'Staff', 'Date d\'inscription'])

        users = User.objects.all().values_list('id', 'username', 'email', 'is_staff', 'date_joined')
        for user in users:
            writer.writerow(user)

        return response
