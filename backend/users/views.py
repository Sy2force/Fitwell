from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .serializers import UserSerializer, ProfileSerializer
import csv

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        # Handle profile updates specifically
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Update user fields
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Update profile fields if present
        if 'profile' in request.data:
            profile_serializer = ProfileSerializer(instance.profile, data=request.data['profile'], partial=True)
            if profile_serializer.is_valid():
                profile_serializer.save()

        return Response(serializer.data)


class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all().order_by('-date_joined')
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']


class AdminUserExportView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="fitwell_leads.csv"'

        writer = csv.writer(response)
        writer.writerow(['Username', 'Email', 'Date Joined', 'Marketing Opt-In', 'Level', 'Health Score'])

        users = User.objects.all().order_by('-date_joined')
        for user in users:
            level = user.profile.level if hasattr(user, 'profile') else 0
            health_score = user.profile.health_score if hasattr(user, 'profile') else 0

            writer.writerow([
                user.username,
                user.email,
                user.date_joined.strftime("%Y-%m-%d"),
                user.marketing_opt_in,
                level,
                health_score
            ])

        return response
