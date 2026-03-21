from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from api.models import WorkoutSession, ExerciseSet, Exercise
from api.serializers import (WorkoutSessionSerializer, WorkoutSessionCreateSerializer, 
                            ExerciseSetSerializer, ExerciseSetCreateSerializer, ExerciseSerializer)

class WorkoutSessionViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les séances d'entraînement.
    - POST: Démarrer une nouvelle session
    - GET: Récupérer l'historique des sessions
    - PATCH: Mettre à jour une session (notes)
    - DELETE: Supprimer une session
    - Custom actions: complete_session, add_set
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return WorkoutSessionCreateSerializer
        return WorkoutSessionSerializer
    
    def get_queryset(self):
        return WorkoutSession.objects.filter(user=self.request.user).prefetch_related('sets__exercise').order_by('-started_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Marquer une session comme terminée.
        Calcule automatiquement la durée, le volume total et attribue l'XP.
        """
        session = self.get_object()
        
        if session.status == 'completed':
            return Response({'error': 'Session déjà terminée'}, status=status.HTTP_400_BAD_REQUEST)
        
        session.complete_session()
        
        serializer = self.get_serializer(session)
        return Response({
            'message': 'Séance terminée avec succès',
            'xp_earned': 50 + (session.duration_minutes // 10) * 10,
            'session': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def add_set(self, request, pk=None):
        """
        Ajouter un set à une session active.
        """
        session = self.get_object()
        
        if session.status != 'active':
            return Response({'error': 'La session n\'est pas active'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = ExerciseSetCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(session=session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """
        Récupérer la session active de l'utilisateur (s'il y en a une).
        """
        active_session = WorkoutSession.objects.filter(
            user=request.user, 
            status='active'
        ).prefetch_related('sets__exercise').first()
        
        if active_session:
            serializer = self.get_serializer(active_session)
            return Response(serializer.data)
        return Response({'message': 'Aucune session active'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Statistiques globales des entraînements de l'utilisateur.
        """
        sessions = WorkoutSession.objects.filter(user=request.user, status='completed')
        
        total_sessions = sessions.count()
        total_volume = sum(s.total_volume for s in sessions)
        total_duration = sum(s.duration_minutes for s in sessions)
        
        return Response({
            'total_sessions': total_sessions,
            'total_volume_kg': round(total_volume, 2),
            'total_duration_minutes': total_duration,
            'average_duration': round(total_duration / total_sessions, 2) if total_sessions > 0 else 0,
            'average_volume': round(total_volume / total_sessions, 2) if total_sessions > 0 else 0,
        })

class ExerciseSetViewSet(viewsets.ModelViewSet):
    """
    API pour gérer les sets individuels.
    Principalement en lecture seule, la création se fait via WorkoutSession.add_set
    """
    serializer_class = ExerciseSetSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return ExerciseSet.objects.filter(session__user=self.request.user).select_related('exercise', 'session')

class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API pour la bibliothèque d'exercices (lecture seule pour les utilisateurs).
    """
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['muscle_group', 'difficulty']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'difficulty']
