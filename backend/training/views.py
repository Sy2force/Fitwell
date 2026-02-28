from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Exercise, Program, WorkoutSession
from .serializers import ExerciseSerializer, ProgramSerializer, WorkoutSessionSerializer, WorkoutSetSerializer


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['muscle_group', 'difficulty', 'equipment']
    search_fields = ['name']


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.filter(is_public=True)
    serializer_class = ProgramSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Public programs + user's own programs
        return Program.objects.filter(is_public=True) | Program.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user).order_by('-date')

    @action(detail=True, methods=['post'])
    def add_set(self, request, pk=None):
        session = self.get_object()
        serializer = WorkoutSetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
